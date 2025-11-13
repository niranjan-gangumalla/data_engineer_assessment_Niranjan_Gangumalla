import pandas as pd
from utils.logger_service import get_logger


class FieldConfig:
    TABLE_TO_FIELDS = {}
    FIELDS_LOWER = set()
    logger = get_logger("FieldConfig")

    @classmethod
    def load_from_excel(cls, path: str):
        try:
            df = pd.read_excel(path)
            if {"Column Name", "Target Table"}.issubset(df.columns):
                field_col = "Column Name"
                table_col = "Target Table"
            elif {"field", "table"}.issubset(df.columns):
                field_col = "field"
                table_col = "table"
            else:
                cls.logger.warning(
                    "Field Config.xlsx does not include expected column formats "
                    "(Expected: 'Column Name'+'Target Table' OR 'field'+'table')"
                )
                return

            cls.TABLE_TO_FIELDS = {}
            cls.FIELDS_LOWER = set()

            for _, row in df.iterrows():
                table = str(row[table_col]).strip().lower()
                field = str(row[field_col]).strip()

                cls.TABLE_TO_FIELDS.setdefault(table, []).append(field)
                cls.FIELDS_LOWER.add(field.lower())

            cls.logger.info(f"Loaded {len(cls.FIELDS_LOWER)} fields from Field Config.xlsx")

        except Exception as e:
            cls.logger.warning(f"Could not read Field Config at {path}: {e}")
