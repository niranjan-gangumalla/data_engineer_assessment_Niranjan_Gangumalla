from pydantic import BaseModel, Field
from typing import Optional

class PropertyModel(BaseModel):
    property_id: int
    property_title: Optional[str] = Field(None, alias="Property_Title")
    address: Optional[str] = Field(None, alias="Address")
    market: Optional[str] = Field(None, alias="Market")
    flood: Optional[str] = Field(None, alias="Flood")
    street_address: Optional[str] = Field(None, alias="Street_Address")
    city: Optional[str] = Field(None, alias="City")
    state: Optional[str] = Field(None, alias="State")
    zip: Optional[str] = Field(None, alias="Zip")
    property_type: Optional[str] = Field(None, alias="Property_Type")
    highway: Optional[str] = Field(None, alias="Highway")
    train: Optional[str] = Field(None, alias="Train")
    tax_rate: Optional[float] = Field(None, alias="Tax_Rate")
    sqft_basement: Optional[int] = Field(None, alias="SQFT_Basement")
    htw: Optional[str] = Field(None, alias="HTW")
    pool: Optional[str] = Field(None, alias="Pool")
    commercial: Optional[str] = Field(None, alias="Commercial")
    water: Optional[str] = Field(None, alias="Water")
    sewage: Optional[str] = Field(None, alias="Sewage")
    year_built: Optional[int] = Field(None, alias="Year_Built")
    sqft_mu: Optional[int] = Field(None, alias="SQFT_MU")
    sqft_total: Optional[int] = Field(None, alias="SQFT_Total")
    parking: Optional[str] = Field(None, alias="Parking")
    bed: Optional[int] = Field(None, alias="Bed")
    bath: Optional[int] = Field(None, alias="Bath")
    basementyesno: Optional[str] = Field(None, alias="BasementYesNo")
    layout: Optional[str] = Field(None, alias="Layout")
    rent_restricted: Optional[str] = Field(None, alias="Rent_Restricted")
    neighborhood_rating: Optional[int] = Field(None, alias="Neighborhood_Rating")
    latitude: Optional[float] = Field(None, alias="Latitude")
    longitude: Optional[float] = Field(None, alias="Longitude")
    subdivision: Optional[str] = Field(None, alias="Subdivision")
    school_average: Optional[float] = Field(None, alias="School_Average")

    model_config = {
        "validate_by_name": True
    }

    @classmethod
    def validate_lenient(cls, data: dict):
        d = dict(data)  # copy input dict

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

        # Fields to convert to int
        for k in [
            "Property_ID", "SQFT_Basement", "Year_Built", "SQFT_MU","SQFT_Total", "Bed", "Bath", "Neighborhood_Rating"
        ]:
            if k in d:
                d[k] = try_int(d.get(k))

        # Fields to convert to float
        for k in [
            "Tax_Rate", "Latitude", "Longitude", "School_Average"
        ]:
            if k in d:
                d[k] = try_float(d.get(k))

        # Coerce zip to string if present and not None or empty
        if "Zip" in d:
            if d["Zip"] in (None, ""):
                d["Zip"] = None
            else:
                d["Zip"] = str(d["Zip"])

        return cls(**d)
