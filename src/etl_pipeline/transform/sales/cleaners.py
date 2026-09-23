# transform/sales/cleaners
import pandas as pd

# given the schema of sales csv, we can normalise the data:

def normalise_dates(df: pd.DataFrame) -> pd.DataFrame:
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce", format="mixed")
    return df

def normalise_sku(df: pd.DataFrame) -> pd.DataFrame:
    df["sku"] = df["sku"].str.strip().str.upper()
    return df

def drop_invalid_quantities(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["quantity"] > 0]

def normalise_region(df: pd.DataFrame) -> pd.DataFrame:
    df["region"] = df["region"].str.strip().str.title().replace({"N/A": pd.NA, "": pd.NA})
    return df

def normalise_channel(df: pd.DataFrame) -> pd.DataFrame:
    df["channel"] = df["channel"].str.strip().str.lower()
    return df

def coerce_price(df: pd.DataFrame) -> pd.DataFrame:
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    return df

def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates()