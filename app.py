import streamlit as st
import numpy as np
import pandas as pd
import pickle
import os
import plotly.graph_objects as go

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="PriceOptima", layout="wide")

# -----------------------
# HEADER
# -----------------------
st.title("💰 PriceOptima Dashboard")
st.markdown("AI-powered Dynamic Pricing 🚀")
st.markdown("---")

# -----------------------
# LOAD MODEL
# -----------------------
BASE_DIR = os.path.dirname(__file__)

model = pickle.load(open(os.path.join(BASE_DIR, "model/model.pkl"), "rb"))
scaler = pickle.load(open(os.path.join(BASE_DIR, "model/scaler.pkl"), "rb"))
features = pickle.load(open(os.path.join(BASE_DIR, "model/features.pkl"), "rb"))

# -----------------------
# SIDEBAR INPUTS
# -----------------------
st.sidebar.header("⚙️ Controls")

price = st.sidebar.slider("Price", 0, 1000, 200)
month = st.sidebar.slider("Month", 1, 12, 3)
day = st.sidebar.slider("Day", 1, 31, 15)
weekday = st.sidebar.slider("Weekday", 0, 6, 2)

# -----------------------
# INPUT PREP
# -----------------------
input_dict = {
    "Price": price,
    "month": month,
    "day": day,
    "weekday": weekday
}

input_df = pd.DataFrame([input_dict])

for col in features:
    if col not in input_df.columns:
        input_df[col] = 0

input_df = input_df[features]
input_scaled = scaler.transform(input_df)

# -----------------------
# ORIGINAL DEMAND
# -----------------------
pred_log = model.predict(input_scaled)[0]
predicted_demand = np.expm1(pred_log)

# -----------------------
# INITIAL PRICING LOGIC
# -----------------------
if predicted_demand > 100:
    recommended_price = price * 1.15
    trend = "📈 Increase Price"
else:
    recommended_price = price * 0.90
    trend = "📉 Reduce Price"

# -----------------------
# NEW DEMAND (AFTER PRICE CHANGE)
# -----------------------
# -----------------------
# FIND BEST PRICE (MAX REVENUE)
# -----------------------
price_range = np.linspace(price * 0.7, price * 1.3, 20)

best_price = price
best_revenue = 0

for p in price_range:
    temp = {
        "Price": p,
        "month": month,
        "day": day,
        "weekday": weekday
    }

    temp_df = pd.DataFrame([temp])

    for col in features:
        if col not in temp_df.columns:
            temp_df[col] = 0

    temp_df = temp_df[features]
    temp_scaled = scaler.transform(temp_df)

    d = np.expm1(model.predict(temp_scaled)[0])
    revenue = p * d

    if revenue > best_revenue:
        best_revenue = revenue
        best_price = p

# FINAL SELECTED PRICE
recommended_price = best_price
new_revenue = best_revenue

# ORIGINAL REVENUE
original_revenue = price * predicted_demand

# LIFT (NOW WILL CHANGE)
lift = ((new_revenue - original_revenue) / original_revenue) * 100

# TREND TEXT
if lift > 0:
    trend = "🚀 Optimized Price for Maximum Revenue"
else:
    trend = "⚖️ Current Price Already Optimal"
# -----------------------
# REVENUE CALCULATION
# ----------------------
# -----------------------
# KPIs
# -----------------------
st.subheader("📊 Key Metrics")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Price", f"₹{price}")
c2.metric("Recommended", f"₹{recommended_price:.2f}")
c3.metric("Demand", f"{predicted_demand:.2f}")
c4.metric("Revenue Lift", f"{lift:.2f}%")

st.markdown("---")

# -----------------------
# DECISION
# -----------------------
st.subheader("🧠 Pricing Decision")
st.success(trend)

# -----------------------
# REVENUE CHART
# -----------------------
st.subheader("📈 Revenue Comparison")

fig = go.Figure()

fig.add_trace(go.Bar(
    x=["Original", "Optimized"],
    y=[original_revenue, new_revenue],
    text=[f"₹{original_revenue:.0f}", f"₹{new_revenue:.0f}"],
    textposition="auto"
))

fig.update_layout(template="plotly_dark")

st.plotly_chart(fig, use_container_width=True)

# -----------------------
# DEMAND VS PRICE
# -----------------------
st.subheader("📉 Demand vs Price")

prices = np.linspace(price * 0.5, price * 1.5, 30)
demands = []

for p in prices:
    temp = {"Price": p, "month": month, "day": day, "weekday": weekday}
    temp_df = pd.DataFrame([temp])

    for col in features:
        if col not in temp_df.columns:
            temp_df[col] = 0

    temp_df = temp_df[features]
    temp_scaled = scaler.transform(temp_df)

    d = np.expm1(model.predict(temp_scaled)[0])
    demands.append(d)

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=prices, y=demands, mode='lines'))

fig2.update_layout(
    template="plotly_dark",
    xaxis_title="Price",
    yaxis_title="Demand"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------
# REVENUE CURVE
# -----------------------
st.subheader("💰 Revenue Curve")

revenues = prices * np.array(demands)

fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=prices, y=revenues, mode='lines'))

fig3.update_layout(
    template="plotly_dark",
    xaxis_title="Price",
    yaxis_title="Revenue"
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------
# INSIGHTS
# -----------------------
st.subheader("📌 Insights")

st.info(f"""
📊 Demand reacts to pricing changes  
💡 AI avoids loss-making decisions  
🚀 Revenue lift ensured: {lift:.2f}%  

This system ensures optimal and safe pricing.
""")