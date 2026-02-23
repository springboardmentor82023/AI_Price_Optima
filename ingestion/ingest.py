import os
import pandas as pd
from datetime import datetime

# STEP 1: Define Project Root Directory
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

# STEP 2: Define Required Paths
CLEAN_DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "amazon_sales_cleaned.csv"
)

DAILY_INGEST_FOLDER = os.path.join(
    BASE_DIR,
    "data",
    "daily_ingest"
)

LOG_FOLDER = os.path.join(
    BASE_DIR,
    "logs"
)

LOG_FILE = os.path.join(
    LOG_FOLDER,
    "ingestion.log"
)

# Create folders if not exist
os.makedirs(DAILY_INGEST_FOLDER, exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)

# STEP 3: Logging Function
def write_log(message):
    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a") as log:
        log.write(f"[{time_stamp}] {message}\n")


write_log("Ingestion Pipeline Started")

# STEP 4: Read Cleaned Dataset
if not os.path.exists(CLEAN_DATA_PATH):
    write_log("ERROR: Cleaned dataset not found")
    raise FileNotFoundError(
        f"Cleaned dataset not found at {CLEAN_DATA_PATH}"
    )

df = pd.read_csv(CLEAN_DATA_PATH)
write_log("Cleaned dataset loaded successfully")

# STEP 5: Validation Check
required_columns = [
    'order_id','order_date','product_id',
    'product_category','price',
    'discount_percent','quantity_sold',
    'customer_region','payment_method',
    'rating','review_count',
    'discounted_price','total_revenue'
]

missing_cols = set(required_columns) - set(df.columns)

if missing_cols:
    write_log(f"ERROR: Missing columns {missing_cols}")
    raise Exception(f"Missing columns: {missing_cols}")

write_log("Dataset validation successful")

# STEP 6: Create Daily Folder
today_date = datetime.now().strftime("%Y-%m-%d")

today_folder = os.path.join(
    DAILY_INGEST_FOLDER,
    today_date
)

os.makedirs(today_folder, exist_ok=True)

write_log(f"Daily folder created: {today_folder}")

# STEP 7: Save Daily Ingestion Copy
output_file = os.path.join(
    today_folder,
    "amazon_sales_cleaned.csv"
)

df.to_csv(output_file, index=False)

write_log("Daily ingestion file saved successfully")

# STEP 8: Pipeline Completion
write_log("Ingestion Pipeline Completed Successfully")

print("Daily Data Ingestion Completed Successfully")
print("Saved File Location:")
print(output_file)