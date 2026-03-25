import os
import pandas as pd
from datetime import datetime


RAW_FOLDER = "data/raw"
PROCESSED_FOLDER = "data/processed"
DAILY_FOLDER = "data/daily_ingest"

RAW_FILE_NAME = "retail_raw.csv"
PROCESSED_FILE_NAME = "retail_processed.csv"

print("Starting ingestion pipeline...")


raw_path = os.path.join(RAW_FOLDER, RAW_FILE_NAME)

if not os.path.exists(raw_path):
    print("Error: Raw file not found in raw folder.")
    exit()

try:
    df = pd.read_csv(raw_path)
    print("Raw data loaded successfully.")
except Exception as e:
    print("Error loading raw data:", e)
    exit()


if df.empty:
    print("Error: Dataset is empty.")
    exit()

print("Dataset validation completed.")


# Remove duplicate rows
df.drop_duplicates(inplace=True)

# Handle missing values
df.fillna(0, inplace=True)

# Strip column names (remove extra spaces)
df.columns = df.columns.str.strip()

print("Data cleaning completed.")


os.makedirs(PROCESSED_FOLDER, exist_ok=True)

processed_path = os.path.join(PROCESSED_FOLDER, PROCESSED_FILE_NAME)
df.to_csv(processed_path, index=False)

print("Processed file saved successfully.")


today = datetime.now().strftime("%Y-%m-%d")
daily_path = os.path.join(DAILY_FOLDER, today)

os.makedirs(daily_path, exist_ok=True)

daily_file_path = os.path.join(daily_path, PROCESSED_FILE_NAME)
df.to_csv(daily_file_path, index=False)

print(f"Daily ingestion completed for {today}.")
print("Pipeline executed successfully.")