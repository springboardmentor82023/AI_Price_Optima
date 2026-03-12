import pandas as pd
import os

print("Starting ingestion...")

df = pd.read_csv("data/raw/dynamic_pricing_final_50000.csv")

df = df.drop_duplicates()

os.makedirs("data/processed", exist_ok=True)
df.to_csv("data/processed/dynamic_pricing_cleaned.csv", index=False)

print("Data saved to processed folder")