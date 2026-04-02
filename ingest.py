import pandas as pd
import os
from datetime import datetime

RAW_FILE = "data/raw/sales_data.csv"
PROCESSED_FILE = "data/processed/sales_cleaned.csv"
DAILY_FOLDER = "data/daily_ingest"

def run_ingestion():
    try:
        print("Loading raw data...")
        df = pd.read_csv(RAW_FILE)
        print("Raw data loaded successfully")

      
        print("Columns found:", df.columns.tolist())
        required_columns = ["Date", "Product ID", "Price", "Units Ordered"]

        for col in required_columns:
              if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")


    
        df.drop_duplicates(inplace=True)
        df.dropna(inplace=True)
        df.drop(columns=["Promotion", "Epidemic"], inplace=True)

        print("Duplicates and missing values handled")

    
        df.to_csv(PROCESSED_FILE, index=False)
        print("Saved to processed folder")

      
        today = datetime.today().strftime("%Y-%m-%d")
        daily_path = os.path.join(DAILY_FOLDER, today)
        os.makedirs(daily_path, exist_ok=True)

        df.to_csv(os.path.join(daily_path, "sales_cleaned.csv"), index=False)

        print("Daily ingestion completed successfully")

    except Exception as e:
        print("Error during ingestion:", e)


if __name__ == "__main__":
    run_ingestion()
