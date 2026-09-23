# src/etl_pipeline/pipelines/daily_sales_pipeline.py
from datetime import date
from pathlib import Path
from etl_pipeline.extract.sales.sales_csv_extractor import extract_sales_data
from etl_pipeline.transform.sales.pipeline import clean_sales_data

def run(sales_csv_path: str):
    raw_df = extract_sales_data(sales_csv_path)   # reads from data/raw/sales/...

    clean_df = clean_sales_data(raw_df)
    today = date.today().strftime("%Y%m%d")
    clean_path = Path(f"data/processed/sales/{today}_sales_clean.parquet")
    clean_path.parent.mkdir(parents=True, exist_ok=True)
    clean_df.to_parquet(clean_path)

    return clean_df

if __name__ == "__main__":
    run(r"C:\Users\danie\PycharmProjects\refactoring\data\raw\sales\20260904_sales_data.csv")