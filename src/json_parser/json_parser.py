from typing import List, Dict

class JSONParser:

    @staticmethod
    def extract_nested(records: List[Dict], key: str, property_id: int) -> List[Dict]:
        extracted = []

        for record in records:
            nested = record.get(key, [])
            if isinstance(nested, list):
                for child in nested:
                    # Attach foreign key for relational integrity
                    child["property_id"] = property_id
                    extracted.append(child)

        return extracted
