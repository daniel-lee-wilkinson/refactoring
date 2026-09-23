# transform/sales/pipeline.py
import pandas as pd
from etl_pipeline.transform.sales.cleaners import (
    normalise_dates,
    normalise_sku,
    drop_invalid_quantities,
    normalise_region,
    normalise_channel,
    coerce_price,
    drop_duplicates,
)

def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the sales data by applying a series of transformations.
    Transformed data stored as a Pandas dataframe.
    """
    df = df.copy()
    df = normalise_dates(df)
    df = normalise_sku(df)
    df = coerce_price(df)
    df = drop_invalid_quantities(df)
    df = normalise_region(df)
    df = normalise_channel(df)
    df = drop_duplicates(df)
    return df

if __name__ == "__main__":
    df = clean_sales_data(pd.read_csv("../extract/sales/sales.csv"))
    print(df.head())