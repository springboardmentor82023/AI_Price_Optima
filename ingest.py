import os
import pandas as pd
from datetime import datetime

# Define folder paths
BASE_DIR = "data"
RAW_FOLDER = os.path.join(BASE_DIR, "raw")
PROCESSED_FOLDER = os.path.join(BASE_DIR, "processed")
DAILY_FOLDER = os.path.join(BASE_DIR, "daily_ingest")

# Create folders if they don't exist
os.makedirs(RAW_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(DAILY_FOLDER, exist_ok=True)


def validate_columns(df, required_columns, file_name):
    """Check if required columns exist."""
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"{file_name} is missing columns: {missing_cols}")
    print(f"{file_name} columns validated successfully.")


def clean_data(df):
    """Basic cleaning steps."""
    # Remove duplicates
    df = df.drop_duplicates()

    # Handle missing values
    df = df.fillna(method='ffill')  # forward fill

    return df


def process_file(file_name, required_columns, cleaned_name):
    try:
        file_path = os.path.join(RAW_FOLDER, file_name)

        # Load data
        df = pd.read_csv(file_path)
        print(f"{file_name} loaded successfully.")

        # Validate columns
        validate_columns(df, required_columns, file_name)

        # Clean data
        df = clean_data(df)
        print(f"{file_name} cleaned successfully.")

        # Save to processed folder
        processed_path = os.path.join(PROCESSED_FOLDER, cleaned_name)
        df.to_csv(processed_path, index=False)
        print(f"{cleaned_name} saved in processed folder.")

        # Save to daily ingestion folder
        today = datetime.today().strftime("%Y-%m-%d")
        daily_path = os.path.join(DAILY_FOLDER, today)

        os.makedirs(daily_path, exist_ok=True)

        daily_file_path = os.path.join(daily_path, cleaned_name)
        df.to_csv(daily_file_path, index=False)

        print(f"{cleaned_name} saved in daily ingest folder ({today}).")

    except Exception as e:
        print(f"Error processing {file_name}: {e}")


def main():
    print("Starting Data Ingestion Pipeline...\n")

    # Sales processing
    process_file(
        file_name="sales_data.csv",
        required_columns=["order_id", "product_id", "date", "quantity", "price"],
        cleaned_name="sales_cleaned.csv"
    )

    # Inventory processing
    process_file(
        file_name="inventory_data.csv",
        required_columns=["product_id", "stock_level", "last_updated"],
        cleaned_name="inventory_cleaned.csv"
    )

    print("\nIngestion completed successfully.")


if __name__ == "__main__":
    main()