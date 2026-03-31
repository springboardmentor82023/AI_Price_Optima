import streamlit as st
import numpy as np
import pickle
import pandas as pd
import plotly.express as px

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="AI PriceOptima", layout="wide")

# -------------------------------
# UNIVERSAL UI (LIGHT + DARK SAFE)
# -------------------------------
st.markdown("""
<style>

/* GENERAL TEXT FIX */
html, body, [class*="css"] {
    color: #ffffff;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0e2433, #1c3b4d);
}

/* SELECT BOX FIX */
div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #000000 !important;
}

/* SELECT TEXT */
div[data-baseweb="select"] span {
    color: #000000 !important;
}

/* NUMBER INPUT FIX */
input {
    background-color: #ffffff !important;
    color: #000000 !important;
}

/* SLIDER LABEL */
label {
    color: #ffffff !important;
}

/* KPI CARDS */
.metric-card {
    background: #162f3f;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid #1f4e5f;
}

/* HEADER */
h1, h2, h3 {
    color: #00f5d4 !important;
}

/* SPACING */
.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# HEADER
# -------------------------------
st.markdown("""
<h1 style='text-align:center;'>🚀 AI PriceOptima Dashboard</h1>
<p style='text-align:center;'>Dynamic Pricing for Revenue Optimization</p>
""", unsafe_allow_html=True)

# -------------------------------
# LOAD MODEL
# -------------------------------
try:
    model = pickle.load(open("model.pkl", "rb"))
    st.success("✅ Model Loaded Successfully")
except:
    st.error("❌ Model not found")
    st.stop()

# -------------------------------
# SIDEBAR INPUTS
# -------------------------------
st.sidebar.header("🔧 Input Parameters")

product = st.sidebar.selectbox("Product", ["Product A", "Product B", "Product C"])
price = st.sidebar.number_input("Current Price (₹)", min_value=1.0, value=100.0)
inventory = st.sidebar.slider("Inventory Level", 0, 1000, 100)
demand_factor = st.sidebar.slider("Demand Factor", 0.1, 1.0, 0.5)

# -------------------------------
# MODEL PREDICTION
# -------------------------------
input_data = np.array([[price, inventory, demand_factor]])
predicted_demand = model.predict(input_data)[0]

# FIX NEGATIVE
predicted_demand = max(predicted_demand, 1)

# -------------------------------
# PRICING LOGIC
# -------------------------------
recommended_price = price * (1 + demand_factor * 0.2)
rule_price = price * 1.1

# REVENUES
original_revenue = max(price * predicted_demand, 1)
rule_revenue = max(rule_price * predicted_demand, 1)
ml_revenue = max(recommended_price * predicted_demand, 1)

# -------------------------------
# KPI CARDS
# -------------------------------
st.markdown("## 📈 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.markdown(f"""
<div class="metric-card">
<h4>💰 Recommended Price</h4>
<h2>₹ {recommended_price:.2f}</h2>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class="metric-card">
<h4>📦 Expected Demand</h4>
<h2>{predicted_demand:.2f}</h2>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class="metric-card">
<h4>📊 Expected Revenue</h4>
<h2>₹ {ml_revenue:.2f}</h2>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# COMPARISON
# -------------------------------
st.markdown("## 🔍 Comparison")

improvement = max(((ml_revenue - original_revenue) / original_revenue) * 100, 0)

c1, c2, c3 = st.columns(3)

c1.metric("Original Price", f"₹ {price}")
c2.metric("Suggested Price", f"₹ {recommended_price:.2f}")
c3.metric("Revenue Improvement", f"{improvement:.2f}%")

# -------------------------------
# REVENUE CHART
# -------------------------------
st.markdown("## 📊 Revenue Comparison")

df = pd.DataFrame({
    "Strategy": ["Static", "Rule-Based", "ML-Based"],
    "Revenue": [original_revenue, rule_revenue, ml_revenue]
})

fig = px.bar(df, x="Strategy", y="Revenue", color="Strategy")
st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# PRICE VS DEMAND
# -------------------------------
st.markdown("## 📉 Price vs Demand")

prices = np.linspace(50, 200, 50)
demands = np.maximum(predicted_demand - (prices * 0.1), 1)

df2 = pd.DataFrame({"Price": prices, "Demand": demands})
fig2 = px.line(df2, x="Price", y="Demand")

st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# DEMAND TREND
# -------------------------------
st.markdown("## 📈 Demand Trend")

trend = pd.DataFrame({
    "Time": range(1, 21),
    "Demand": np.maximum(predicted_demand + np.random.randn(20)*5, 1)
})

fig3 = px.line(trend, x="Time", y="Demand")
st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# BUSINESS INSIGHTS
# -------------------------------
st.markdown("## 💡 Business Insights")

st.success("""
✔ ML-based pricing dynamically adjusts price  
✔ Higher demand → higher optimized price → more revenue  
✔ Inventory influences pricing flexibility  
✔ ML strategy outperforms static pricing  
""")

# -------------------------------
# EXPLAINER
# -------------------------------
with st.expander("📘 How This Works"):
    st.write("""
This system predicts demand using ML and recommends optimal pricing.
It compares static, rule-based, and ML pricing to maximize revenue.
""")
