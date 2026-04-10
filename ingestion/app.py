import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from datetime import datetime

# Load Model & Encoders
model = joblib.load("../models/xgb_model.pkl")
encoders = joblib.load("../models/encoders.pkl")
feature_order = joblib.load("../models/features.pkl")

# UI Configuration
st.set_page_config(page_title="AI Price Optimizer", layout="wide")

st.title("📊 AI Price Optimizer Dashboard")
st.markdown("Optimize product pricing using Machine Learning to maximize revenue.")

# Sidebar Inputs
st.sidebar.header("🔧 Product Inputs")

price = st.sidebar.slider("Price (₹)", 100, 5000, 1000)
discount = st.sidebar.slider("Discount (%)", 0, 80, 10)
inventory = st.sidebar.number_input("Inventory Level", min_value=0, step=1)
rating = st.sidebar.slider("Rating", 1.0, 5.0, 4.0)
reviews = st.sidebar.slider("Review Count", 0, 5000, 100)
product_id = st.sidebar.text_input("Product ID", "P123")

category = st.sidebar.selectbox(
    "Product Category",
    encoders["product_category"].classes_
)
region = st.sidebar.selectbox(
    "Customer Region",
    encoders["customer_region"].classes_
)
payment = st.sidebar.selectbox(
    "Payment Method",
    encoders["payment_method"].classes_
)

# Safe Encoding Function
# Safe Encoding Function
def safe_encode(encoder, value):
    if value in encoder.classes_:
        return encoder.transform([value])[0]
    else:
        return -1  # Handle unseen categories

# ✅ FIX 1: Moved simulate_best_price up here
def simulate_best_price(input_data):
    candidate_changes = [-0.10, -0.05, 0.0, 0.05, 0.10]

    best_price = input_data["price"]
    best_revenue = -1
    best_demand = 0

    for change in candidate_changes:
        temp = input_data.copy()
        new_price = input_data["price"] * (1 + change)
        temp["price"] = new_price

        temp_df = pd.DataFrame([temp])
        temp_df = temp_df[feature_order]  # Ensure correct order
        pred = model.predict(temp_df)[0]
        pred = max(pred, 0)

        revenue = new_price * pred

        if revenue > best_revenue:
            best_revenue = revenue
            best_price = new_price
            best_demand = pred

    return best_price, best_demand, best_revenue

# Date Feature Extraction (current date for simulation)
order_date = datetime.today()
day = order_date.day
month = order_date.month
year = order_date.year
day_of_week = order_date.weekday()
week_of_year = order_date.isocalendar()[1]
is_weekend = 1 if day_of_week >= 5 else 0

# ✅ FIX 2: Added safe_encode to product_id
input_data = {
    "price": price,
    "discount_percent": discount,
    "inventory_level": inventory,
    "rating": rating,
    "review_count": reviews,
    "product_id": safe_encode(encoders["product_id"], product_id), # Fixed line
    "product_category": safe_encode(encoders["product_category"], category),
    "customer_region": safe_encode(encoders["customer_region"], region),
    "payment_method": safe_encode(encoders["payment_method"], payment),
    "day": day,
    "month": month,
    "year": year,
    "day_of_week": day_of_week,
    "week_of_year": week_of_year,
    "is_weekend": is_weekend
}

# Convert input to DataFrame and reorder features
input_df = pd.DataFrame([input_data])
input_df = input_df[feature_order]

# Model Prediction
original_demand = model.predict(input_df)[0]
original_demand = max(original_demand, 0)  # Ensure non-negative
original_revenue = price * original_demand

best_price, best_demand, best_revenue = simulate_best_price(input_data)

# KPI Metrics
st.subheader("📌 Key Performance Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Original Price", f"₹{price}")
col2.metric("Recommended Price", f"₹{best_price:.2f}")
col3.metric(
    "Revenue Improvement",
    f"{((best_revenue - original_revenue) / original_revenue) * 100:.2f}%"
)

# Revenue Comparison
st.subheader("📊 Revenue Comparison")

strategies = ["Original", "ML Optimized"]
revenues = [original_revenue, best_revenue]

fig1, ax1 = plt.subplots()
ax1.bar(strategies, revenues)
ax1.set_ylabel("Revenue")
st.pyplot(fig1)

# Demand vs Price Curve
st.subheader("📉 Demand vs Price")

price_range = np.linspace(price * 0.7, price * 1.3, 25)
demand_curve = []

for p in price_range:
    temp = input_data.copy()
    temp["price"] = p
    temp_df = pd.DataFrame([temp])
    temp_df = temp_df[feature_order]  # Keep the order
    d = model.predict(temp_df)[0]
    demand_curve.append(max(d, 0))

fig2, ax2 = plt.subplots()
ax2.plot(price_range, demand_curve)
ax2.set_xlabel("Price (₹)")
ax2.set_ylabel("Demand")
st.pyplot(fig2)

# Revenue vs Price Curve
st.subheader("📈 Revenue vs Price")

revenue_curve = [p * d for p, d in zip(price_range, demand_curve)]

fig3, ax3 = plt.subplots()
ax3.plot(price_range, revenue_curve)
ax3.set_xlabel("Price (₹)")
ax3.set_ylabel("Revenue")
st.pyplot(fig3)

# Detailed Comparison Table
st.subheader("📋 Detailed Comparison")

comparison_df = pd.DataFrame({
    "Metric": ["Price", "Demand", "Revenue"],
    "Original": [price, original_demand, original_revenue],
    "ML Suggested": [best_price, best_demand, best_revenue]
})

st.table(comparison_df)

# Simulation Function
def simulate_best_price(input_data):
    candidate_changes = [-0.10, -0.05, 0.0, 0.05, 0.10]

    best_price = input_data["price"]
    best_revenue = -1
    best_demand = 0

    for change in candidate_changes:
        temp = input_data.copy()
        new_price = input_data["price"] * (1 + change)
        temp["price"] = new_price

        temp_df = pd.DataFrame([temp])
        temp_df = temp_df[feature_order]  # Ensure correct order
        pred = model.predict(temp_df)[0]
        pred = max(pred, 0)

        revenue = new_price * pred

        if revenue > best_revenue:
            best_revenue = revenue
            best_price = new_price
            best_demand = pred

    return best_price, best_demand, best_revenue