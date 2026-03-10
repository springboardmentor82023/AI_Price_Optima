import pandas as pd
import numpy as np

df = pd.read_csv(r"C:\Users\Shubm\OneDrive\Desktop\shubham\AI_Price_Optima\data\processed\retail_store_inventory_cleaned.csv")

def pricing_engine(row):

    price = row["Price"]

    month = row["Month"]
    inventory = row["Inventory Level"]
    weather = row["Weather Condition"]
    day = row["DayOfWeek"]

    # existing rules ------------------------------------------------------
    # Monthly rule
    if month in [4, 12]:
        price *= 1.15
    elif month in [3, 10]:
        price *= 0.90

    # Inventory rule
    if inventory < 200:
        price *= 1.10
    elif inventory > 400:
        price *= 0.92

    # Weather rule
    if weather == "Cloudy":
        price *= 1.05
    
    if day in [5,6]:   # Saturday or Sunday
        price *= 1.07  # increase price by 7%

    # new rules -----------------------------------------------------------
    # 1. high-volume / forecast rule: raise price when demand forecast is much
    #    larger than units already sold (i.e. expected high demand and little
    #    stock has been moved).
    forecast = row.get("Demand Forecast", np.nan)
    units = row.get("Units Sold", np.nan)
    if pd.notna(forecast) and pd.notna(units) and forecast > units * 1.2:
        price *= 1.12

    # 2. high-volume threshold: if this row is already in the top quartile of
    #    historic units sold, apply a modest premium
    if pd.notna(units) and units > 203:  # 75th percentile from data exploration
        price *= 1.08

    # 3. competitor gap: if competitor is substantially higher, we can afford
    #    to bump price; if they are far lower, consider a small cut
    comp = row.get("Competitor Pricing", np.nan)
    if pd.notna(comp):
        # gap positive means competitor more expensive
        gap = comp - price
        if gap >= 2:
            price *= 1.05
        elif gap <= -2:
            price *= 0.95

    # 4. scarcity check: low inventory relative to forecast
    if pd.notna(forecast) and pd.notna(inventory) and inventory < 200 and forecast > units * 1.2:
        # stack with the earlier forecast rule; another multiplier
        price *= 1.10

    return price

df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.month
df["DayOfWeek"] = df["Date"].dt.dayofweek
df["Adjusted Price"] = df.apply(pricing_engine, axis=1)


df["Static Revenue"] = df["Price"] * df["Units Sold"]
df["Dynamic Revenue"] = df["Adjusted Price"] * df["Units Sold"]

original_revenue = df["Static Revenue"].sum()
new_revenue = df["Dynamic Revenue"].sum()

revenue_lift = ((new_revenue - original_revenue) / original_revenue) * 100

print(df[["Price","Adjusted Price","Month"]].head())

print("Original Revenue:", original_revenue)
print("New Revenue:", new_revenue)
print("Revenue Lift (%):", revenue_lift)