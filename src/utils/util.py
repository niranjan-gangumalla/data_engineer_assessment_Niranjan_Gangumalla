import pandas as pd

"""
    Safely cast each column in df to the target dtype defined in dtype_map.
    Missing columns are created with NaN.
    Numeric conversion is safely coerced.
"""
def cast_df_types(df: pd.DataFrame, dtype_map: dict) -> pd.DataFrame:
    for col, dtype in dtype_map.items():
        # Add missing columns with null values
        if col not in df.columns:
            df[col] = pd.NA
        # Numeric types
        if dtype in ("float64", "Int64"):
            df[col] = pd.to_numeric(df[col], errors="coerce")
            if dtype == "Int64":
                df[col] = df[col].astype("Int64")
        else:
            df[col] = df[col].astype(dtype)

    return df
