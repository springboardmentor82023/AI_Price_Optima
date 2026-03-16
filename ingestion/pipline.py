import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "amazon_sales_cleaned.csv"
)

OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "amazon_sales_dynamic_pricing.csv"
)

df = pd.read_csv(DATA_PATH)

df["order_date"] = pd.to_datetime(df["order_date"])
df["price"] = pd.to_numeric(df["price"])
df["quantity_sold"] = pd.to_numeric(df["quantity_sold"])

df["day_of_week"] = df["order_date"].dt.day_name()
df["month"] = df["order_date"].dt.month
df["is_weekend"] = df["day_of_week"].isin(["Saturday", "Sunday"])

def demand_level(q):
    if q >= 4:
        return "high"
    elif q <= 2:
        return "low"
    else:
        return "medium"

df["demand_level"] = df["quantity_sold"].apply(demand_level)

if "inventory_level" not in df.columns:
    np.random.seed(42)
    df["inventory_level"] = np.random.randint(10, 150, len(df))

def adjust_price(row):
    price = row["price"]

    if row["demand_level"] == "high":
        price *= 1.10
    elif row["demand_level"] == "low":
        price *= 0.95

    if row["inventory_level"] < 20:
        price *= 1.15
    elif row["inventory_level"] > 100:
        price *= 0.90

    if row["is_weekend"]:
        price *= 1.05

    if row["month"] in [11, 12]:
        price *= 1.08

    return round(price, 2)

df["adjusted_price"] = df.apply(adjust_price, axis=1)

df["static_revenue"] = df["price"] * df["quantity_sold"]
df["dynamic_revenue"] = df["adjusted_price"] * df["quantity_sold"]

static_rev = df["static_revenue"].sum()
dynamic_rev = df["dynamic_revenue"].sum()

revenue_lift = ((dynamic_rev - static_rev) / static_rev) * 100

df.to_csv(OUTPUT_PATH, index=False)

print("Static Revenue :", round(static_rev, 2))
print("Dynamic Revenue:", round(dynamic_rev, 2))
print("Revenue Lift % :", round(revenue_lift, 2))

plt.figure()

labels = ["Static Pricing", "Dynamic Pricing"]
revenues = [static_rev, dynamic_rev]

plt.bar(labels, revenues)

plt.title("Static vs Dynamic Pricing Revenue Comparison")
plt.xlabel("Pricing Strategy")
plt.ylabel("Total Revenue")

plt.show()

daily_revenue = df.groupby("order_date")[["static_revenue","dynamic_revenue"]].sum()

plt.figure()

plt.plot(daily_revenue.index, daily_revenue["static_revenue"], label="Static Revenue")
plt.plot(daily_revenue.index, daily_revenue["dynamic_revenue"], label="Dynamic Revenue")

plt.title("Daily Revenue: Static vs Dynamic Pricing")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.legend()

plt.xticks(rotation=45)

plt.show()

sample = df.sample(100)

plt.figure()

plt.scatter(sample["price"], sample["adjusted_price"])

plt.title("Static Price vs Dynamic Price")
plt.xlabel("Static Price")
plt.ylabel("Dynamic Price")

plt.show()