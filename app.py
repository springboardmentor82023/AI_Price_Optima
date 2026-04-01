import streamlit as st
import os
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="PriceOptima", layout="wide")

# -----------------------------
# TITLE
# -----------------------------
st.title("💰 PriceOptima - Dynamic Pricing System")
st.markdown("### Intelligent Price Recommendation Dashboard")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("⚙️ Advanced Settings")

competitor_price = st.sidebar.number_input("Competitor Price", value=95.0)
discount = st.sidebar.number_input("Discount (%)", value=5.0)
weekend_flag = st.sidebar.selectbox("Weekend?", [0, 1])
holiday_flag = st.sidebar.selectbox("Holiday?", [0, 1])

# -----------------------------
# MAIN INPUTS
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    price = st.number_input("Current Price", min_value=0.0, value=100.0)

with col2:
    inventory = st.number_input("Inventory Level", min_value=0, value=50)

# -----------------------------
# AUTO MODE
# -----------------------------
auto_mode = st.checkbox("⚡ Auto Mode (Recommended)")

if auto_mode:
    competitor_price = price * 0.95
    discount = 5.0
    weekend_flag = 0
    holiday_flag = 0

price_diff = price - competitor_price

# -----------------------------
# DEFAULT VALUES
# -----------------------------
base_price = price
year = 2024
month = 1
day = 1
hour = 12

# -----------------------------
# LOAD MODEL
# -----------------------------
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    pipeline = joblib.load(os.path.join(BASE_DIR, "pipeline.pkl"))
    st.success("✅ Model Ready")
    pipeline_loaded = True
except:
    st.error("❌ Model failed to load")
    pipeline_loaded = False

# -----------------------------
# BUTTON
# -----------------------------
if st.button("🚀 Get Recommendation"):

    if pipeline_loaded:

        # -----------------------------
        # INPUT DATA
        # -----------------------------
        input_df = pd.DataFrame([{
            "price": price,
            "base_price": base_price,
            "competitor_price": competitor_price,
            "discount": discount,
            "inventory": inventory,
            "year": year,
            "month": month,
            "day": day,
            "hour": hour,
            "weekend_flag": weekend_flag,
            "holiday_flag": holiday_flag,
            "price_diff": price_diff,
            "price_ratio": price / (competitor_price + 1),
            "discount_effect": discount / (price + 1)
        }])

        # -----------------------------
        # ORIGINAL DEMAND (FIXED)
        # -----------------------------
        pred_log = pipeline.predict(input_df)[0]
        demand = np.expm1(pred_log)
        static_revenue = price * demand

        # -----------------------------
        # OPTIMAL PRICE SEARCH (UPDATED ✅)
        # -----------------------------
        price_range = [price * (1 + x / 100) for x in range(-10, 11, 2)]  # smaller range

        best_price = price
        best_revenue = static_revenue
        best_demand = demand

        price_list = []
        demand_list = []
        revenue_list = []

        for test_price in price_range:

            # 🔥 1. COMPETITOR CONSTRAINT
            if test_price > max(price * 1.1, competitor_price * 1.1):
                continue


            temp_df = input_df.copy()
            temp_df["price"] = test_price
            temp_df["price_diff"] = test_price - competitor_price
            temp_df["price_ratio"] = test_price / (competitor_price + 1)
            temp_df["discount_effect"] = discount / (test_price + 1)

            # prediction
            temp_log = pipeline.predict(temp_df)[0]
            temp_demand = np.expm1(temp_log)

            # 🔥 2. PENALTY FOR LARGE CHANGE
            penalty = abs(test_price - price) * 0.1

            # 🔥 3. DEMAND DROP PENALTY (NEW)
            demand_drop_penalty = max(0, demand - temp_demand) * 50

            # FINAL REVENUE CALCULATION
            temp_revenue = (test_price * temp_demand) - penalty - demand_drop_penalty

            price_list.append(test_price)
            demand_list.append(temp_demand)
            revenue_list.append(temp_revenue)

            if temp_revenue > best_revenue:
                best_revenue = temp_revenue
                best_price = test_price
                best_demand = temp_demand
        # FINAL ML VALUES
        recommended_price = best_price
        new_demand = best_demand
        ml_revenue = best_revenue

        # -----------------------------
        # IMPROVEMENT
        # -----------------------------
        if static_revenue == 0:
            improvement = 0
        else:
            improvement = ((ml_revenue - static_revenue) / static_revenue) * 100

        # -----------------------------
        # KPI METRICS
        # -----------------------------
        st.subheader("📊 Key Metrics")

        k1, k2, k3, k4 = st.columns(4)

        k1.metric("Demand", f"{new_demand:.2f}")
        k2.metric("Recommended Price", f"{recommended_price:.2f}")
        k3.metric("Expected Revenue", f"{ml_revenue:.2f}")
        k4.metric("Revenue Improvement", f"{improvement:.2f}%")

        # -----------------------------
        # PRICE COMPARISON
        # -----------------------------
        st.subheader("📊 Price Comparison")

        c1, c2 = st.columns(2)

        c1.metric("Original Price", f"{price:.2f}")
        c2.metric("ML Suggested Price", f"{recommended_price:.2f}")

        # -----------------------------
        # REVENUE COMPARISON
        # -----------------------------
        st.subheader("📈 Revenue Comparison")

        fig1, ax1 = plt.subplots()
        labels = ["Static", "ML-Based"]
        values = [static_revenue, ml_revenue]

        ax1.bar(labels, values)
        ax1.set_ylabel("Revenue")
        ax1.set_title("Revenue Comparison")

        st.pyplot(fig1)

        # -----------------------------
        # DEMAND TREND
        # -----------------------------
        st.subheader("📉 Demand vs Price")

        fig2, ax2 = plt.subplots()
        ax2.plot(price_list, demand_list)
        ax2.set_xlabel("Price")
        ax2.set_ylabel("Demand")
        ax2.set_title("Demand Trend")

        st.pyplot(fig2)

        # -----------------------------
        # REVENUE TREND
        # -----------------------------
        st.subheader("📈 Revenue vs Price")

        fig3, ax3 = plt.subplots()
        ax3.plot(price_list, revenue_list)
        ax3.set_xlabel("Price")
        ax3.set_ylabel("Revenue")
        ax3.set_title("Price Impact on Revenue")

        st.pyplot(fig3)

        # -----------------------------
        # BUSINESS INSIGHT
        # -----------------------------
        st.subheader("📌 Business Insight")

        if improvement > 0:
            st.success("✅ ML pricing increases revenue")
        elif improvement < 0:
            st.error("⚠️ ML pricing reduces revenue")
        else:
            st.info("ℹ️ No revenue change")

        # -----------------------------
        # DEBUG INFO
        # -----------------------------
        st.write(f"Original Demand: {demand:.2f}")
        st.write(f"Optimized Demand: {new_demand:.2f}")
        st.write(f"Static Revenue: {static_revenue:.2f}")
        st.write(f"ML Revenue: {ml_revenue:.2f}")
        st.write("Model Loaded Successfully")