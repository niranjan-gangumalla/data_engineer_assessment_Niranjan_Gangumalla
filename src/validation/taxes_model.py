from pydantic import BaseModel
from typing import Optional

class TaxesModel(BaseModel):
    property_id: int
    Taxes: Optional[float] = None

    @classmethod
    def validate_lenient(cls, data: dict):
        d = dict(data)
        try:
            if "Taxes" in d:
                d["Taxes"] = None if d["Taxes"] in (None, "") else float(d["Taxes"])
        except Exception:
            d["Taxes"] = None
        try:
            if "property_id" in d:
                d["property_id"] = int(float(d["property_id"]))
        except Exception:
            d["property_id"] = None
        return cls(**d)
