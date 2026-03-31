import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI Pricing Dashboard", layout="wide")

# Load model
model = pickle.load(open("xgb_model.pkl", "rb"))

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("⚙️ Control Panel")

price = st.sidebar.number_input("💰 Current Price", value=100.0)
inventory = st.sidebar.number_input("📦 Inventory Level", value=50)
competitor_price = st.sidebar.number_input("🏪 Competitor Price", value=95.0)
demand_index = st.sidebar.slider("📊 Demand Index", 0, 100, 50)
date = st.sidebar.date_input("📅 Select Date")

run = st.sidebar.button("🚀 Generate Recommendation")

# -----------------------------
# MAIN TITLE
# -----------------------------
st.title("💡 AI-Powered Dynamic Pricing Dashboard")

# -----------------------------
# TOP METRICS (LIVE VIEW)
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Price", f"₹{price}")
col2.metric("📦 Inventory", inventory)
col3.metric("🏪 Competitor", f"₹{competitor_price}")
col4.metric("📊 Demand", demand_index)

# -----------------------------
# DAY INSIGHT
# -----------------------------
day_name = date.strftime("%A")

if date.weekday() >= 5:
    st.warning(f"⚠️ {day_name}: Weekend → Higher demand expected")
else:
    st.info(f"{day_name}: Normal demand")

# -----------------------------
# MODEL INPUT
# -----------------------------
input_data = pd.DataFrame({
    "price": [price],
    "inventory": [inventory],
    "competitor_price": [competitor_price],
    "demand_index": [demand_index]
})

# -----------------------------
# RUN MODEL
# -----------------------------
if run:

    predicted_demand = model.predict(input_data)[0]

    # Pricing logic
    original_price = price

    rule_price = price
    if date.weekday() >= 5:
        rule_price *= 1.10
    if inventory < 20:
        rule_price *= 1.15
    elif inventory > 100:
        rule_price *= 0.90

    recommended_price = price * (1 + (demand_index / 200))

    # Revenue
    original_revenue = original_price * predicted_demand
    rule_revenue = rule_price * predicted_demand
    ml_revenue = recommended_price * predicted_demand

    improvement = ((ml_revenue - original_revenue) / original_revenue) * 100

    # -----------------------------
    # KPI CARDS
    # -----------------------------
    st.subheader("📊 Prediction Results")

    c1, c2, c3 = st.columns(3)

    c1.metric("📦 Expected Demand", f"{predicted_demand:.2f}")
    c2.metric("💰 Recommended Price", f"₹{recommended_price:.2f}")
    c3.metric("📈 Revenue", f"₹{ml_revenue:.2f}", f"{improvement:.2f}% ↑")

    # -----------------------------
    # SMART INSIGHTS
    # -----------------------------
    st.subheader("🧠 AI Insights")

    if demand_index > 70:
        st.success("🔥 High demand detected → Increase price to maximize profit")
    elif demand_index < 30:
        st.warning("⚠️ Low demand → Consider discounts")
    else:
        st.info("✅ Moderate demand → Maintain balanced pricing")

    if inventory < 20:
        st.warning("📦 Low inventory → Increase price")
    elif inventory > 100:
        st.info("📦 High inventory → Reduce price to clear stock")

    # -----------------------------
    # TABS (INTERACTIVE SECTIONS)
    # -----------------------------
    tab1, tab2, tab3 = st.tabs(["📊 Comparison", "📉 Demand Curve", "📈 Revenue Curve"])

    # -----------------------------
    # TAB 1: COMPARISON
    # -----------------------------
    with tab1:

        df_comp = pd.DataFrame({
            "Type": ["Original", "Rule-Based", "ML-Based"],
            "Revenue": [original_revenue, rule_revenue, ml_revenue]
        })

        fig = px.bar(df_comp, x="Type", y="Revenue", title="Revenue Comparison")
        st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # DEMAND TREND
    # -----------------------------
    prices = np.linspace(price * 0.8, price * 1.5, 20)

    demands = []
    for p in prices:
        temp = pd.DataFrame({
            "price": [p],
            "inventory": [inventory],
            "competitor_price": [competitor_price],
            "demand_index": [demand_index]
        })
        demands.append(model.predict(temp)[0])

    # -----------------------------
    # TAB 2: DEMAND CURVE
    # -----------------------------
    with tab2:

        fig2 = px.line(x=prices, y=demands, labels={'x': 'Price', 'y': 'Demand'},
                       title="Demand vs Price")
        st.plotly_chart(fig2, use_container_width=True)

    # -----------------------------
    # TAB 3: REVENUE CURVE
    # -----------------------------
    with tab3:

        revenues_curve = [p * d for p, d in zip(prices, demands)]

        fig3 = px.line(x=prices, y=revenues_curve,
                       labels={'x': 'Price', 'y': 'Revenue'},
                       title="Revenue vs Price")

        st.plotly_chart(fig3, use_container_width=True)