import os
import pandas as pd
from datetime import datetime

# ==========================
# Define Folder Paths
# ==========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RAW_FOLDER = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_FOLDER = os.path.join(BASE_DIR, "data", "processed")
DAILY_FOLDER = os.path.join(BASE_DIR, "data", "daily_ingest")

REQUIRED_COLUMNS = [
    "Date",
    "Store ID",
    "Product ID",
    "Category",
    "Price",
    "Units Sold"
]

# ==========================
# Validate Required Columns
# ==========================
def validate_columns(df):
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    print("Column validation successful.")


# ==========================
# Clean Data
# ==========================
def clean_data(df):

    # Convert Date
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Remove duplicates
    df = df.drop_duplicates()

    # Handle numeric missing values
    numeric_cols = df.select_dtypes(include="number").columns
    for col in numeric_cols:
        df[col].fillna(df[col].median(), inplace=True)

    # Handle categorical missing values
    categorical_cols = df.select_dtypes(include="object").columns
    for col in categorical_cols:
        df[col].fillna(df[col].mode()[0], inplace=True)

    return df


# ==========================
# Process File
# ==========================
def process_file(filename):

    file_path = os.path.join(RAW_FOLDER, filename)

    if not os.path.exists(file_path):
        print(f"{filename} not found in raw folder.")
        return

    print("File loaded successfully.")

    df = pd.read_csv(file_path)

    validate_columns(df)

    df_clean = clean_data(df)

    print("Data cleaning completed.")

    # Save to processed folder
    processed_path = os.path.join(PROCESSED_FOLDER, f"cleaned_{filename}")
    df_clean.to_csv(processed_path, index=False)

    print("Processed file saved.")

    # Create daily folder
    today = datetime.now().strftime("%Y-%m-%d")
    daily_path = os.path.join(DAILY_FOLDER, today)

    os.makedirs(daily_path, exist_ok=True)

    daily_file = os.path.join(daily_path, f"cleaned_{filename}")
    df_clean.to_csv(daily_file, index=False)

    print("Daily ingestion file saved.")


# ==========================
# Main Execution
# ==========================
if __name__ == "__main__":

    print("Starting Ingestion Pipeline...\n")

    process_file("sales_data.csv")

    print("\nIngestion completed successfully.")