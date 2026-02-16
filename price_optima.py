import pandas as pd
import numpy as np

# Load
df = pd.read_excel(r"C:\Users\Shubm\OneDrive\Desktop\shubham\AI_Price_Optima\retail_store_inventory.csv.xlsx")


# Convert Date
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Drop critical missing
critical_cols = ['Date','Store ID','Product ID','Price','Units Sold']
df = df.dropna(subset=critical_cols)

# Remove duplicates
df = df.drop_duplicates(subset=['Store ID','Product ID','Date'])

# Remove invalid values
df = df[df['Price'] > 0]
df = df[df['Units Sold'] >= 0]
df = df[df['Inventory Level'] >= 0]


num_cols = df.select_dtypes(include=np.number).columns
# Fill numerical columns
for col in num_cols:
    df[col] = df[col].fillna(df[col].median())


# Fill categorical columns with mode
cat_cols = df.select_dtypes(include='object').columns
for col in cat_cols:
    df[col] = df[col].fillna(df[col].mode()[0])


# Create revenue
df['Revenue'] = df['Price'] * df['Units Sold']

# Define output path
output_path = r"C:\Users\Shubm\OneDrive\Desktop\shubham\AI_Price_Optima\retail_store_inventory_cleaned.csv"

# Save cleaned dataset
df.to_csv(output_path, index=False)

#print(f"Cleaned dataset saved at: {output_path}")

print("Cleaning Completed Successfully")
