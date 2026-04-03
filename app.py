import streamlit as st
import pandas as pd
import xgboost as xgb

# Load data
df = pd.read_csv("/content/cleaned_retail_inventory.csv")

# Safe column handling
df.columns = df.columns.str.strip()

# If Date exists → use it, else create dummy
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.month
    df["Weekday"] = df["Date"].dt.weekday
else:
    df["Month"] = 1
    df["Weekday"] = 1

# Check column names
price_col = "Price"
inventory_col = "Inventory Level"
demand_col = "Units Sold"

# Train model
X = df[[price_col, inventory_col, "Month", "Weekday"]]
y = df[demand_col]

model = xgb.XGBRegressor()
model.fit(X, y)

# UI
st.title("💰 PriceOptima Dashboard")

st.sidebar.header("Input")

price = st.sidebar.slider("Price", 1, 500, 50)
inventory = st.sidebar.slider("Inventory", 1, 200, 50)
month = st.sidebar.slider("Month", 1, 12, 6)
weekday = st.sidebar.slider("Weekday", 0, 6, 3)

# Prediction
input_data = pd.DataFrame({
    price_col: [price],
    inventory_col: [inventory],
    "Month": [month],
    "Weekday": [weekday]
})

predicted_demand = model.predict(input_data)[0]

# Pricing logic
recommended_price = price * 1.1

# Revenue
original_revenue = price * predicted_demand
new_revenue = recommended_price * predicted_demand

lift = ((new_revenue - original_revenue) / original_revenue) * 100

# KPI
st.subheader("📊 Results")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Recommended Price", round(recommended_price,2))
col2.metric("Demand", round(predicted_demand,2))
col3.metric("Revenue", round(new_revenue,2))
col4.metric("Lift %", round(lift,2))

# Chart
st.subheader("📈 Revenue Comparison")

chart = pd.DataFrame({
    "Type": ["Original", "New"],
    "Revenue": [original_revenue, new_revenue]
})

st.bar_chart(chart.set_index("Type"))

# Trend
st.subheader("📉 Demand Trend")
trend = df.groupby("Month")[demand_col].mean()
st.line_chart(trend)
