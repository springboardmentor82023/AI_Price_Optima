# eda_mandatory.py
# Run this after preprocessing/ingestion (uses the cleaned dataset).
# Graphs are shown ONE BY ONE with short, practical interpretation notes.

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

# 1) Load cleaned dataset
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CLEAN_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "amazon_sales_cleaned.csv")

if not os.path.exists(CLEAN_DATA_PATH):
    raise FileNotFoundError(f"Cleaned dataset not found at: {CLEAN_DATA_PATH}")

df = pd.read_csv(CLEAN_DATA_PATH)

# Safe conversions
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["discount_percent"] = pd.to_numeric(df["discount_percent"], errors="coerce")
df["quantity_sold"] = pd.to_numeric(df["quantity_sold"], errors="coerce")
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["review_count"] = pd.to_numeric(df["review_count"], errors="coerce")
df["total_revenue"] = pd.to_numeric(df["total_revenue"], errors="coerce")

df = df.dropna(subset=["order_date", "price", "discount_percent", "quantity_sold", "rating", "review_count", "total_revenue"])

print("Dataset loaded for EDA:", df.shape)
print(df.head())

# Correlation Heatmap (Numeric Relationships)
numeric_cols = [
    "price",
    "discount_percent",
    "quantity_sold",
    "rating",
    "review_count",
    "total_revenue"
]

print(df[numeric_cols].dtypes)

# Remove constant columns
non_constant_cols = [c for c in numeric_cols if df[c].nunique() > 1]

corr = df[non_constant_cols].corr()

plt.figure(figsize=(10, 6))
sns.heatmap(
    corr,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    square=True
)
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.show()

# 2) Price vs Quantity Sold (Demand Curve / Price Sensitivity)
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="price", y="quantity_sold", alpha=0.6)
sns.regplot(data=df, x="price", y="quantity_sold", scatter=False)  # trend line
plt.title("Price vs Quantity Sold")
plt.xlabel("Price")
plt.ylabel("Quantity Sold")
plt.show()

# 3) Discount % vs Quantity Sold (Discount Effectiveness)
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="discount_percent", y="quantity_sold", alpha=0.6)
sns.regplot(data=df, x="discount_percent", y="quantity_sold", scatter=False)
plt.title("Discount % vs Quantity Sold")
plt.xlabel("Discount Percent")
plt.ylabel("Quantity Sold")
plt.show()

# 4) Revenue by Product Category (Category Performance)
category_rev = (
    df.groupby("product_category")["total_revenue"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))
sns.barplot(x=category_rev.index, y=category_rev.values)
plt.title("Total Revenue by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Total Revenue (Sum)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# 5) Monthly Revenue Trend (Seasonality & Time Trend)
df["month"] = df["order_date"].dt.to_period("M").astype(str)
monthly_rev = df.groupby("month")["total_revenue"].sum()

plt.figure(figsize=(10, 5))
plt.plot(monthly_rev.index, monthly_rev.values, marker="o")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Total Revenue (Sum)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# 6) Rating vs Quantity Sold (Trust → Demand)
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="rating", y="quantity_sold", alpha=0.6)
sns.regplot(data=df, x="rating", y="quantity_sold", scatter=False)
plt.title("Rating vs Quantity Sold")
plt.xlabel("Rating")
plt.ylabel("Quantity Sold")
plt.show()

print("\n Mandatory EDA visuals completed.")