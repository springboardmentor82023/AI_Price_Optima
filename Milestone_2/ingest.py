import pandas as pd
import os
from datetime import datetime

# Paths
RAW_PATH = "data/raw"
PROCESSED_PATH = "data/processed"
DAILY_PATH = "data/daily_ingest"

# Create folders if not exist
os.makedirs(PROCESSED_PATH, exist_ok=True)
os.makedirs(DAILY_PATH, exist_ok=True)

# Today's date folder
today = datetime.now().strftime("%Y-%m-%d")
today_path = os.path.join(DAILY_PATH, today)
os.makedirs(today_path, exist_ok=True)


def process_file(filename, required_columns):
    try:
        print(f"\nLoading {filename}...")
        file_path = os.path.join(RAW_PATH, filename)
        df = pd.read_csv(file_path)

        # Validate columns
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

        # Cleaning steps
        df = df.drop_duplicates()
        df = df.fillna(method="ffill")

        # Save processed file
        cleaned_name = filename.replace(".csv", "_cleaned.csv")
        processed_file = os.path.join(PROCESSED_PATH, cleaned_name)
        df.to_csv(processed_file, index=False)

        # Save daily ingestion copy
        daily_file = os.path.join(today_path, cleaned_name)
        df.to_csv(daily_file, index=False)

        print(f"{filename} processed successfully")

    except Exception as e:
        print(f"Error processing {filename}: {e}")


# Process sales data
process_file(
    "sales_data.csv",
    required_columns=["date", "product_id", "units_sold", "price"]
)

# Process inventory data
process_file(
    "inventory_data.csv",
    required_columns=["product_id", "stock_level"]
)

print("\nIngestion completed successfully")
