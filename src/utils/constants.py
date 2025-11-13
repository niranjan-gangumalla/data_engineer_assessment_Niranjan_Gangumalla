PROPERTY_DTYPE = {
    "property_id": "Int64",
    "Property_Title": "string",
    "Address": "string",
    "Reviewed_Status": "string",
    "Most_Recent_Status": "string",
    "Source": "string",
    "Market": "string",
    "Occupancy": "string",
    "Flood": "string",
    "Street_Address": "string",
    "City": "string",
    "State": "string",
    "Zip": "string",
    "Property_Type": "string",
    "Highway": "string",
    "Train": "string",
    "Tax_Rate": "float64",
    "SQFT_Basement": "Int64",
    "HTW": "string",
    "Pool": "string",
    "Commercial": "string",
    "Water": "string",
    "Sewage": "string",
    "Year_Built": "Int64",
    "SQFT_MU": "Int64",
    "SQFT_Total": "string",
    "Parking": "string",
    "Bed": "Int64",
    "Bath": "Int64",
    "BasementYesNo": "string",
    "Layout": "string",
    "Rent_Restricted": "string",
    "Neighborhood_Rating": "Int64",
    "Latitude": "float64",
    "Longitude": "float64",
    "Subdivision": "string",
    "School_Average": "float64",
}


VALUATION_DTYPE = {
    "valuation_id": "Int64",
    "property_id": "Int64",
    "List_Price": "float64",
    "Previous_Rent": "float64",
    "Zestimate": "float64",
    "ARV": "float64",
    "Expected_Rent": "float64",
    "Rent_Zestimate": "float64",
    "Low_FMR": "float64",
    "High_FMR": "float64",
    "Redfin_Value": "float64",
}


HOA_DTYPE = {
    "hoa_id": "Int64",
    "property_id": "Int64",
    "HOA": "float64",
    "HOA_Flag": "string",
}


REHAB_DTYPE = {
    "rehab_id": "Int64",
    "property_id": "Int64",
    "Underwriting_Rehab": "float64",
    "Rehab_Calculation": "float64",
    "Paint": "string",
    "Flooring_Flag": "string",
    "Foundation_Flag": "string",
    "Roof_Flag": "string",
    "HVAC_Flag": "string",
    "Kitchen_Flag": "string",
    "Bathroom_Flag": "string",
    "Appliances_Flag": "string",
    "Windows_Flag": "string",
    "Landscaping_Flag": "string",
    "Trashout_Flag": "string",
}


LEADS_DTYPE = {
    "id": "Int64",
    "property_id": "Int64",
    "Reviewed_Status": "string",
    "Most_Recent_Status": "string",
    "Source": "string",
    "Net_Yield": "float64",
    "IRR": "float64",
    "Selling_Reason": "string",
    "Seller_Retained_Broker": "string",
    "Final_Reviewer": "string",
}


TAXES_DTYPE = {
    "id": "Int64",
    "property_id": "Int64",
    "Taxes": "float64",
}


TABLE_DTYPE_MAP = {
    "property": PROPERTY_DTYPE,
    "valuation": VALUATION_DTYPE,
    "hoa": HOA_DTYPE,
    "rehab": REHAB_DTYPE,
    "leads": LEADS_DTYPE,
    "taxes": TAXES_DTYPE,
}