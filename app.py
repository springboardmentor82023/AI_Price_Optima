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
# CUSTOM CSS (🔥 BEAUTY)
# -----------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.big-title {
    font-size: 42px;
    font-weight: bold;
    color: white;
}
.subtitle {
    color: #9ca3af;
    font-size: 18px;
}
.card {
    background: linear-gradient(145deg, #1f2937, #111827);
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 0px 15px rgba(0,255,255,0.1);
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# HEADER
# -----------------------
st.markdown('<div class="big-title">💰 PriceOptima</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-powered Dynamic Pricing Dashboard 🚀</div>', unsafe_allow_html=True)
st.markdown("---")

# -----------------------
# LOAD MODEL
# -----------------------
BASE_DIR = os.path.dirname(__file__)

model = pickle.load(open(os.path.join(BASE_DIR, "model/model.pkl"), "rb"))
scaler = pickle.load(open(os.path.join(BASE_DIR, "model/scaler.pkl"), "rb"))
features = pickle.load(open(os.path.join(BASE_DIR, "model/features.pkl"), "rb"))

# -----------------------
# SIDEBAR
# -----------------------
st.sidebar.header("⚙️ Input Controls")

price = st.sidebar.slider("💵 Price", 50, 1000, 200)
month = st.sidebar.slider("📅 Month", 1, 12, 3)
day = st.sidebar.slider("📆 Day", 1, 31, 15)
weekday = st.sidebar.slider("📊 Weekday", 0, 6, 2)

# -----------------------
# INPUT PROCESSING
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
# PREDICTION
# -----------------------
pred_log = model.predict(input_scaled)[0]
predicted_demand = np.expm1(pred_log)

# SMART PRICING
if predicted_demand > 100:
    recommended_price = price * 1.15
    trend = "📈 Increase Price"
else:
    recommended_price = price * 0.90
    trend = "📉 Reduce Price"

original_revenue = price * predicted_demand
new_revenue = recommended_price * predicted_demand
lift = ((new_revenue - original_revenue) / original_revenue) * 100

# -----------------------
# KPI CARDS
# -----------------------
st.subheader("📊 Key Metrics")

c1, c2, c3, c4 = st.columns(4)

c1.markdown(f'<div class="card">💵<br><b>Price</b><br>₹{price}</div>', unsafe_allow_html=True)
c2.markdown(f'<div class="card">💡<br><b>Recommended</b><br>₹{recommended_price:.2f}</div>', unsafe_allow_html=True)
c3.markdown(f'<div class="card">📦<br><b>Demand</b><br>{predicted_demand:.2f}</div>', unsafe_allow_html=True)
c4.markdown(f'<div class="card">🚀<br><b>Lift</b><br>{lift:.2f}%</div>', unsafe_allow_html=True)

st.markdown("---")

# -----------------------
# PRICING DECISION
# -----------------------
st.subheader("🧠 AI Pricing Decision")
st.success(trend)

# -----------------------
# REVENUE CHART (PLOTLY)
# -----------------------
st.subheader("📈 Revenue Comparison")

fig = go.Figure()

fig.add_trace(go.Bar(
    x=["Original", "Optimized"],
    y=[original_revenue, new_revenue],
    text=[f"₹{original_revenue:.0f}", f"₹{new_revenue:.0f}"],
    textposition="auto"
))

fig.update_layout(
    template="plotly_dark",
    height=400
)

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

fig2.add_trace(go.Scatter(x=prices, y=demands, mode='lines', name='Demand'))

fig2.update_layout(
    template="plotly_dark",
    xaxis_title="Price",
    yaxis_title="Demand"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------
# PRICE VS REVENUE
# -----------------------
st.subheader("💰 Revenue Curve")

revenues = prices * np.array(demands)

fig3 = go.Figure()

fig3.add_trace(go.Scatter(x=prices, y=revenues, mode='lines', name='Revenue'))

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
📊 Demand responds dynamically to price changes  
💡 AI suggests optimal pricing strategy  
🚀 Estimated revenue lift: {lift:.2f}%  

This tool helps businesses take smarter pricing decisions.
""")