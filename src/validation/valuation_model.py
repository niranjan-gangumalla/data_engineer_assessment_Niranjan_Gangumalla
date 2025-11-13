from pydantic import BaseModel, Field
from typing import Optional

class ValuationModel(BaseModel):
    valuation_id: Optional[int] = None
    property_id: int
    list_price: Optional[float] = Field(None, alias="List_Price")
    previous_rent: Optional[float] = Field(None, alias="Previous_Rent")
    arv: Optional[float] = Field(None, alias="ARV")
    rent_zestimate: Optional[float] = Field(None, alias="Rent_Zestimate")
    expected_rent: Optional[float] = Field(None, alias="Expected_Rent")
    low_fmr: Optional[float] = Field(None, alias="Low_FMR")
    high_fmr: Optional[float] = Field(None, alias="High_FMR")
    zestimate: Optional[float] = Field(None, alias="Zestimate")
    redfin_value: Optional[float] = Field(None, alias="Redfin_Value")

    class Config:
        allow_population_by_field_name = True

    @classmethod
    def validate_lenient(cls, data: dict):
        d = dict(data)

        # Convert IDs to int safely
        for k in ["valuation_id", "property_id"]:
            if k in d:
                try:
                    d[k] = int(float(d[k]))
                except Exception:
                    d[k] = None

        # Convert numeric fields to float safely
        for field in [
            "List_Price", "Previous_Rent", "ARV", "Rent_Zestimate", 
            "Expected_Rent", "Low_FMR", "High_FMR", "Zestimate", "Redfin_Value"
        ]:
            if field in d:
                try:
                    d[field] = None if d[field] in (None, "") else float(d[field])
                except Exception:
                    d[field] = None

        return cls(**d)
