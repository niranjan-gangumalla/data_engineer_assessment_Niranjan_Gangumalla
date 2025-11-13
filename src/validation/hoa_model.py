from pydantic import BaseModel
from typing import Optional

class HOAModel(BaseModel):
    hoa_id: Optional[int] = None
    property_id: int
    hoa: Optional[float] = None
    hoa_flag: Optional[str] = None

    @classmethod
    def validate_lenient(cls, data: dict):
        d = dict(data)
        for k in ["hoa_id", "property_id"]:
            if k in d:
                try:
                    d[k] = int(float(d[k]))
                except Exception:
                    d[k] = None
        if "hoa" in d:
            try:
                d["hoa"] = None if d["hoa"] in (None, "") else float(d["hoa"])
            except Exception:
                d["hoa"] = None
        return cls(**d)
