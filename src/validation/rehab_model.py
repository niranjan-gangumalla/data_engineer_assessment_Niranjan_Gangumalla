from pydantic import BaseModel, Field
from typing import Optional

class RehabModel(BaseModel):
    rehab_id: Optional[int] = None
    property_id: int
    underwriting_rehab: Optional[float] = Field(None, alias="Underwriting_Rehab")
    rehab_calculation: Optional[float] = Field(None, alias="Rehab_Calculation")
    paint: Optional[str] = Field(None, alias="Paint")
    flooring_flag: Optional[str] = Field(None, alias="Flooring_Flag")
    foundation_flag: Optional[str] = Field(None, alias="Foundation_Flag")
    roof_flag: Optional[str] = Field(None, alias="Roof_Flag")
    hvac_flag: Optional[str] = Field(None, alias="HVAC_Flag")
    kitchen_flag: Optional[str] = Field(None, alias="Kitchen_Flag")
    bathroom_flag: Optional[str] = Field(None, alias="Bathroom_Flag")
    appliances_flag: Optional[str] = Field(None, alias="Appliances_Flag")
    windows_flag: Optional[str] = Field(None, alias="Windows_Flag")
    landscaping_flag: Optional[str] = Field(None, alias="Landscaping_Flag")
    trashout_flag: Optional[str] = Field(None, alias="Trashout_Flag")

    model_config = {
        "validate_by_name": True
    }

    @classmethod
    def validate_lenient(cls, data: dict):
        d = dict(data)
        # Convert IDs to int safely
        for k in ["rehab_id", "property_id"]:
            if k in d:
                try:
                    d[k] = int(float(d[k]))
                except Exception:
                    d[k] = None
        # Convert numeric fields to float safely
        for field in ["Underwriting_Rehab", "Rehab_Calculation"]:
            if field in d:
                try:
                    d[field] = None if d[field] in (None, "") else float(d[field])
                except Exception:
                    d[field] = None
        return cls(**d)
