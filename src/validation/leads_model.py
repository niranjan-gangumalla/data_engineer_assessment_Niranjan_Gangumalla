# src/validation/leads_model.py
from pydantic import BaseModel
from typing import Optional

class LeadsModel(BaseModel):
    property_id: int
    Reviewed_Status: Optional[str] = None
    Most_Recent_Status: Optional[str] = None
    Source: Optional[str] = None
    Net_Yield: Optional[float] = None
    IRR: Optional[float] = None
    Selling_Reason: Optional[str] = None
    Seller_Retained_Broker: Optional[str] = None
    Final_Reviewer: Optional[str] = None

    @classmethod
    def validate_lenient(cls, data: dict):
        d = dict(data)
        # Numeric coercion
        for k in ["Net_Yield", "IRR"]:
            if k in d:
                try:
                    d[k] = None if d[k] in (None, "") else float(d[k])
                except Exception:
                    d[k] = None
        # Ensure property_id int
        try:
            if "property_id" in d:
                d["property_id"] = int(float(d["property_id"]))
        except Exception:
            d["property_id"] = None
        return cls(**d)
