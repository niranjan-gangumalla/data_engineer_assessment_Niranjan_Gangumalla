from pydantic import BaseModel, validator
from typing import Optional

class PropertyModel(BaseModel):
    property_id: int
    property_title: Optional[str] = None
    address: Optional[str] = None
    reviewed_status: Optional[str] = None
    most_recent_status: Optional[str] = None
    source: Optional[str] = None
    market: Optional[str] = None
    occupancy: Optional[str] = None
    flood: Optional[str] = None
    street_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    property_type: Optional[str] = None
    highway: Optional[str] = None
    train: Optional[str] = None
    tax_rate: Optional[float] = None
    sqft_basement: Optional[int] = None
    htw: Optional[str] = None
    pool: Optional[str] = None
    commercial: Optional[str] = None
    water: Optional[str] = None
    sewage: Optional[str] = None
    year_built: Optional[int] = None
    sqft_mu: Optional[int] = None
    sqft_total: Optional[str] = None
    parking: Optional[str] = None
    bed: Optional[int] = None
    bath: Optional[int] = None
    basementyesno: Optional[str] = None
    layout: Optional[str] = None
    net_yield: Optional[float] = None
    irr: Optional[float] = None
    rent_restricted: Optional[str] = None
    neighborhood_rating: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    subdivision: Optional[str] = None
    taxes: Optional[float] = None
    selling_reason: Optional[str] = None
    seller_retained_broker: Optional[str] = None
    final_reviewer: Optional[str] = None
    school_average: Optional[float] = None

    @validator("zip", pre=True, always=True)
    def coerce_zip(cls, v):
        if v in (None, ""):
            return None
        return str(v)

    @classmethod
    def validate_lenient(cls, data: dict):
        def try_int(x):
            try:
                if x is None or x == "":
                    return None
                return int(float(x))
            except Exception:
                return None

        def try_float(x):
            try:
                if x is None or x == "":
                    return None
                return float(x)
            except Exception:
                return None

        data = dict(data)
        for k in ["property_id", "sqft_basement", "year_built", "sqft_mu", "bed", "bath", "neighborhood_rating"]:
            if k in data:
                data[k] = try_int(data.get(k))

        for k in ["tax_rate", "net_yield", "irr", "latitude", "longitude", "taxes", "school_average"]:
            if k in data:
                data[k] = try_float(data.get(k))

        return cls(**data)
