import os
import pandas as pd
from datetime import datetime

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_PATH = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed")
DAILY_PATH = os.path.join(BASE_DIR, "data", "daily_ingest")

REQUIRED_COLUMNS = [
    "Date",
    "Product ID",
    "Category",
    "Inventory Level",
    "Units Sold",
    "Price"
]

def validate_columns(df):
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

def clean_data(df):
    print("Cleaning data...")

    # Drop duplicates
    df = df.drop_duplicates()

    # Handle missing values
    df = df.ffill()

    # Convert date column
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Remove rows with invalid dates
    df = df.dropna(subset=["Date"])

    return df

def save_outputs(df):
    # Save processed file
    processed_file = os.path.join(PROCESSED_PATH, "sales_cleaned.csv")
    df.to_csv(processed_file, index=False)

    # Create daily folder
    today = datetime.now().strftime("%Y-%m-%d")
    daily_folder = os.path.join(DAILY_PATH, today)

    os.makedirs(daily_folder, exist_ok=True)

    daily_file = os.path.join(daily_folder, "sales_cleaned.csv")
    df.to_csv(daily_file, index=False)

    print("Files saved successfully.")

def main():
    try:
        print("Starting ingestion process...")

        raw_file = os.path.join(RAW_PATH, "sales_data.csv")

        df = pd.read_csv(raw_file)
        print("Sales data loaded successfully.")

        validate_columns(df)

        df_cleaned = clean_data(df)

        save_outputs(df_cleaned)

        print("Ingestion completed successfully.")

    except Exception as e:
        print(f"Error during ingestion: {e}")

if __name__ == "__main__":
    main()