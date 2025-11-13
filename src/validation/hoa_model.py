from pydantic import BaseModel, Field
from typing import Optional

class HOAModel(BaseModel):
    hoa_id: Optional[int] = None
    property_id: int
    hoa: Optional[float] = Field(None, alias="HOA")
    hoa_flag: Optional[str] = Field(None, alias="HOA_Flag")

    model_config = {
        "validate_by_name": True
    }

    @classmethod
    def validate_lenient(cls, data: dict):
        d = dict(data)
        # Convert IDs to int safely
        for k in ["hoa_id", "property_id"]:
            if k in d:
                try:
                    d[k] = int(float(d[k]))
                except Exception:
                    d[k] = None
        # Convert HOA to float safely
        if "HOA" in d:
            try:
                d["HOA"] = None if d["HOA"] in (None, "") else float(d["HOA"])
            except Exception:
                d["HOA"] = None
        return cls(**d)
