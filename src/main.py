from json_parser.json_reader import JSONReader
from json_parser.json_parser import JSONParser
from services.db_factory import DBFactory
from services.db_service import DBService
from utils.config import JSON_FILE_PATH, MALFORMED_PATH, BATCH_SIZE, DB_CONFIG
from utils.logger_service import get_logger
from utils.field_config_loader import FieldConfig
# Pydantic validators
from validation.property_model import PropertyModel
from validation.valuation_model import ValuationModel
from validation.hoa_model import HOAModel
from validation.rehab_model import RehabModel
from validation.leads_model import LeadsModel
from validation.taxes_model import TaxesModel

class BatchManager:
    def __init__(self, batch_size: int):
        self.batch_size = batch_size
        self.items = []

    def add(self, item) -> bool:
        self.items.append(item)
        return len(self.items) >= self.batch_size

    def clear(self):
        self.items = []

    def get(self):
        return self.items


class PropertyETL:
    def __init__(self, db_type="sqlite", sqlite_path="database/home_db.sqlite"):
        self.logger = get_logger(self.__class__.__name__)

        engine = DBFactory.create_engine(
            db_type=db_type,
            config=DB_CONFIG,
            sqlite_path=sqlite_path
        )

        self.db_service = DBService(engine)
        self.batch_manager = BatchManager(BATCH_SIZE)

        # Internal counters
        self.inserted_count = 0
        self.property_id_start = 1

        # Load Field Config mapping (non-blocking)
        try:
            self.field_config = FieldConfig.load_from_excel("data/Field Config.xlsx")
            self.logger.info("Field Config loaded.")
        except Exception:
            # loader already logs; continue with empty mapping
            self.field_config = FieldConfig.TABLE_TO_FIELDS or {}
            self.logger.info("No Field Config loaded.")

        # Build quick reverse lookup: field_lower -> table (lower)
        self.field_to_table = {}
        for table, fields in (FieldConfig.TABLE_TO_FIELDS or {}).items():
            for f in fields:
                self.field_to_table[f.strip().lower()] = table.strip().lower()

    def _split_records_by_table(self, batch, start_id):

        property_rows = []
        valuation_rows = []
        hoa_rows = []
        rehab_rows = []
        leads_rows = []
        taxes_rows = []

        for index, item in enumerate(batch, start=start_id):
            property_id = index

            # Extract nested lists (these are lists under nested keys)
            nested_vals = JSONParser.extract_nested([item], "Valuation", property_id)
            nested_hoas = JSONParser.extract_nested([item], "HOA", property_id)
            nested_rehabs = JSONParser.extract_nested([item], "Rehab", property_id)

            # Add nested results to respective lists (they will be validated later)
            valuation_rows += nested_vals
            hoa_rows += nested_hoas
            rehab_rows += nested_rehabs

            # Prepare dictionaries for root-level routed fields
            base = {"property_id": property_id}
            leads_obj = {"property_id": property_id}
            taxes_obj = {"property_id": property_id}
            # If root has valuation-specific fields (not nested), collect per-property
            root_valuation_obj = {"property_id": property_id}
            root_hoa_obj = {"property_id": property_id}
            root_rehab_obj = {"property_id": property_id}

            for k, v in item.items():
                # Skip JSON nested sections entirely as they are handled above
                if k in ["Valuation", "HOA", "Rehab"]:
                    continue

                key_lower = str(k).strip().lower()
                # Determine target table for this field using loaded FieldConfig
                target_table = self.field_to_table.get(key_lower)

                # If no mapping present, default to 'property' (lenient)
                if not target_table:
                    target_table = "property"

                if target_table == "property":
                    base[k] = v
                elif target_table == "leads":
                    leads_obj[k] = v
                elif target_table == "taxes":
                    taxes_obj[k] = v
                elif target_table == "valuation":
                    # Put into a single root-level valuation row (in addition to nested lists)
                    root_valuation_obj[k] = v
                elif target_table == "hoa":
                    root_hoa_obj[k] = v
                elif target_table == "rehab":
                    root_rehab_obj[k] = v
                else:
                    # Unknown target: treat as property
                    base[k] = v

            # If root-level valuation fields exist (besides property_id), append as a valuation row
            if len([x for x in root_valuation_obj.keys() if x != "property_id"]) > 0:
                valuation_rows.append(root_valuation_obj)

            if len([x for x in root_hoa_obj.keys() if x != "property_id"]) > 0:
                hoa_rows.append(root_hoa_obj)

            if len([x for x in root_rehab_obj.keys() if x != "property_id"]) > 0:
                rehab_rows.append(root_rehab_obj)

            # Property
            try:
                validated_prop = PropertyModel.validate_lenient(base).model_dump()
            except Exception as e:
                self.logger.warning(f"Property validation failed for id {property_id}: {e}")
                continue
            property_rows.append(validated_prop)

            # Leads
            if len([k for k in leads_obj.keys() if k != "property_id"]) > 0:
                try:
                    validated_leads = LeadsModel.validate_lenient(leads_obj).model_dump()
                    leads_rows.append(validated_leads)
                except Exception:
                    self.logger.debug(f"Skipping malformed leads for property {property_id}")

            # Taxes
            if len([k for k in taxes_obj.keys() if k != "property_id"]) > 0:
                try:
                    validated_taxes = TaxesModel.validate_lenient(taxes_obj).model_dump()
                    taxes_rows.append(validated_taxes)
                except Exception:
                    self.logger.debug(f"Skipping malformed taxes for property {property_id}")

        # Validate child rows (valuation/hoa/rehab)
        validated_valuation = []
        for v in valuation_rows:
            try:
                validated_v = ValuationModel.validate_lenient(v).model_dump()
                validated_valuation.append(validated_v)
            except Exception:
                self.logger.debug("Skipping malformed valuation record")

        validated_hoa = []
        for h in hoa_rows:
            try:
                validated_h = HOAModel.validate_lenient(h).model_dump()
                validated_hoa.append(validated_h)
            except Exception:
                self.logger.debug("Skipping malformed HOA record")

        validated_rehab = []
        for r in rehab_rows:
            try:
                validated_r = RehabModel.validate_lenient(r).model_dump()
                validated_rehab.append(validated_r)
            except Exception:
                self.logger.debug("Skipping malformed Rehab record")

        return {
            "property": property_rows,
            "valuation": validated_valuation,
            "hoa": validated_hoa,
            "rehab": validated_rehab,
            "leads": leads_rows,
            "taxes": taxes_rows
        }

    def _process_batch(self, batch):
        batch_data = self._split_records_by_table(
            batch=batch,
            start_id=self.property_id_start
        )

        # Insert into DB
        self.db_service.insert_batch(batch_data)

        # Update counters
        inserted = len(batch)
        self.inserted_count += inserted
        self.property_id_start = self.inserted_count + 1

        self.logger.info(f"Inserted batch of {inserted} records and total {self.inserted_count} records are inserted.")

    def run(self):

        # Expand truncate list to include leads & taxes
        truncate_tables = ["valuation", "hoa", "rehab", "leads", "taxes", "property"]
        self.logger.info("Truncating tables before load...")
        try:
            self.db_service.truncate_tables(truncate_tables)
        except Exception as e:
            self.logger.warning(f"Truncate failed or skipped: {e}")

        self.logger.info("Starting ETL Pipeline")

        reader = JSONReader(
            file_path=JSON_FILE_PATH,
            malformed_path=MALFORMED_PATH
        )

        # Stream records
        for record in reader.read_stream():
            if self.batch_manager.add(record):
                self._process_batch(self.batch_manager.get())
                self.batch_manager.clear()

        # Process remaining records
        remaining = self.batch_manager.get()
        if remaining:
            self._process_batch(remaining)

        # Log summary
        self.logger.info("ETL Completed Successfully")
        self.logger.info(f"Total JSON Records Read     : {reader.total_records}")
        self.logger.info(f"Successfully Inserted       : {self.inserted_count}")
        self.logger.info(f"Malformed JSON Records      : {len(reader.malformed_records)}")

        # Show DB row counts (include leads & taxes)
        self.db_service.log_table_counts(["property", "valuation", "hoa", "rehab", "leads", "taxes"])


if __name__ == "__main__":
    etl = PropertyETL(db_type="mysql", sqlite_path=None)
    etl.run()
