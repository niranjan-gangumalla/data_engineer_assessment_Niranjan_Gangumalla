from pydantic import BaseModel
from typing import Optional

class ValuationModel(BaseModel):
    valuation_id: Optional[int] = None
    property_id: int
    list_price: Optional[float] = None
    previous_rent: Optional[float] = None
    arv: Optional[float] = None
    rent_zestimate: Optional[float] = None
    expected_rent: Optional[float] = None
    low_fmr: Optional[float] = None
    high_fmr: Optional[float] = None
    zestimate: Optional[float] = None
    redfin_value: Optional[float] = None

    @classmethod
    def validate_lenient(cls, data: dict):
        d = dict(data)
        for k in ["valuation_id", "property_id"]:
            if k in d:
                try:
                    d[k] = int(float(d[k]))
                except Exception:
                    d[k] = None
        for k in ["list_price", "previous_rent", "arv", "rent_zestimate", "expected_rent", "low_fmr", "high_fmr", "zestimate", "redfin_value"]:
            if k in d:
                try:
                    d[k] = None if d[k] in (None, "") else float(d[k])
                except Exception:
                    d[k] = None
        return cls(**d)
