import os
import pandas as pd
from datetime import datetime

# Paths
RAW_PATH = "data/raw/"
PROCESSED_PATH = "data/processed/"
DAILY_PATH = "data/daily_ingest/"

# Required columns (adjust if needed after checking your CSV)
REQUIRED_COLUMNS = [
    "Order Date",
    "Product ID",
    "Sales",
    "Quantity",
    "Discount",
    "Profit"
]

def validate_columns(df):
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")
    print("Column validation passed.")

def clean_data(df):
    df = df.drop_duplicates()
    df = df.fillna(0)
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    return df

def save_daily_copy(df, filename):
    today = datetime.today().strftime("%Y-%m-%d")
    daily_folder = os.path.join(DAILY_PATH, today)
    os.makedirs(daily_folder, exist_ok=True)
    df.to_csv(os.path.join(daily_folder, filename), index=False)

def main():
    print("Starting ingestion pipeline...\n")

    file_path = os.path.join(RAW_PATH, "sales_data.csv")

    if not os.path.exists(file_path):
        print("sales_data.csv not found in raw folder.")
        return

    print("Loading sales data...")
    df = pd.read_csv(file_path, encoding="latin1")

    validate_columns(df)
    df_clean = clean_data(df)

    # Save to processed folder
    os.makedirs(PROCESSED_PATH, exist_ok=True)
    processed_file_path = os.path.join(PROCESSED_PATH, "sales_data.csv")
    df_clean.to_csv(processed_file_path, index=False)

    # Save daily copy
    save_daily_copy(df_clean, "sales_data.csv")

    print("Cleaning completed.")
    print("Files saved successfully.")
    print("Ingestion completed successfully.")

if __name__ == "__main__":
    main()