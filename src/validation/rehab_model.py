from pydantic import BaseModel
from typing import Optional

class RehabModel(BaseModel):
    rehab_id: Optional[int] = None
    property_id: int
    underwriting_rehab: Optional[float] = None
    rehab_calculation: Optional[float] = None
    paint: Optional[str] = None
    flooring_flag: Optional[str] = None
    foundation_flag: Optional[str] = None
    roof_flag: Optional[str] = None
    hvac_flag: Optional[str] = None
    kitchen_flag: Optional[str] = None
    bathroom_flag: Optional[str] = None
    appliances_flag: Optional[str] = None
    windows_flag: Optional[str] = None
    landscaping_flag: Optional[str] = None
    trashout_flag: Optional[str] = None

    @classmethod
    def validate_lenient(cls, data: dict):
        d = dict(data)
        for k in ["rehab_id", "property_id"]:
            if k in d:
                try:
                    d[k] = int(float(d[k]))
                except Exception:
                    d[k] = None
        for k in ["underwriting_rehab", "rehab_calculation"]:
            if k in d:
                try:
                    d[k] = None if d[k] in (None, "") else float(d[k])
                except Exception:
                    d[k] = None
        return cls(**d)
