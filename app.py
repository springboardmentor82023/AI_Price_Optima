import streamlit as st
import pandas as pd
import joblib

# -----------------------------
# Load model and features
# -----------------------------
model = joblib.load("models/best_model.pkl")
model_features = joblib.load("models/model_features.pkl")

st.set_page_config(page_title="AI PriceOptima", layout="wide")
st.title("💰 AI PriceOptima - Dynamic Pricing Dashboard")
st.write("Enter values and click Predict.")

# -----------------------------
# User-friendly input section
# -----------------------------
st.sidebar.header("User Input")

inventory_level = st.sidebar.number_input("Inventory Level", min_value=0.0, value=50.0)
units_ordered = st.sidebar.number_input("Units Ordered", min_value=0.0, value=40.0)
demand_forecast = st.sidebar.number_input("Demand Forecast", min_value=0.0, value=45.0)
price = st.sidebar.number_input("Price", min_value=0.0, value=100.0)
discount = st.sidebar.number_input("Discount", min_value=0.0, value=5.0)
competitor_pricing = st.sidebar.number_input("Competitor Pricing", min_value=0.0, value=95.0)

# -----------------------------
# Build full input with zeros
# -----------------------------
input_data = {feature: 0 for feature in model_features}

# Fill only known numeric fields if they exist
if "Inventory Level" in input_data:
    input_data["Inventory Level"] = inventory_level

if "Units Ordered" in input_data:
    input_data["Units Ordered"] = units_ordered

if "Demand Forecast" in input_data:
    input_data["Demand Forecast"] = demand_forecast

if "Price" in input_data:
    input_data["Price"] = price

if "Discount" in input_data:
    input_data["Discount"] = discount

if "Competitor Pricing" in input_data:
    input_data["Competitor Pricing"] = competitor_pricing

# -----------------------------
# Predict
# -----------------------------
if st.sidebar.button("Generate Recommendation"):
    input_df = pd.DataFrame([input_data])

    prediction = model.predict(input_df)[0]

    recommended_price = price * 1.10
    original_revenue = price * prediction
    predicted_revenue = recommended_price * prediction
    improvement = 0
    if original_revenue != 0:
        improvement = ((predicted_revenue - original_revenue) / original_revenue) * 100

    # Output cards
    st.subheader("📊 Prediction Output")
    c1, c2, c3 = st.columns(3)

    c1.metric("Predicted Units Sold", f"{round(prediction, 2)}")
    c2.metric("Recommended Price", f"₹{recommended_price:.2f}")
    c3.metric("Expected Revenue", f"₹{predicted_revenue:.2f}")

    # Comparison
    st.subheader("📈 Comparison Section")
    st.write(f"**Original Price:** ₹{price:.2f}")
    st.write(f"**Suggested Price:** ₹{recommended_price:.2f}")
    st.write(f"**Original Revenue:** ₹{original_revenue:.2f}")
    st.write(f"**Predicted Revenue:** ₹{predicted_revenue:.2f}")
    st.write(f"**Revenue Improvement:** {improvement:.2f}%")

    # KPI chart
    st.subheader("📉 KPI Visualization")

    chart_df = pd.DataFrame({
        "Strategy": ["Original", "Recommended"],
        "Revenue": [original_revenue, predicted_revenue]
    })

    st.bar_chart(chart_df.set_index("Strategy"))

else:
    st.info("Enter values in the sidebar and click 'Generate Recommendation'.")