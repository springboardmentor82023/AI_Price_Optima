import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt

# Load model
model = pickle.load(open("model.pkl", "rb"))

st.title("💰 PriceOptima - Dynamic Pricing System")

st.sidebar.header("User Input")

# 🔹 User Inputs
price = st.sidebar.slider("Current Price", 10.0, 1000.0, 100.0)
discount = st.sidebar.slider("Discount (%)", 0.0, 50.0, 10.0)

day = st.sidebar.slider("Day", 1, 31, 15)
month = st.sidebar.slider("Month", 1, 12, 6)

# 🔹 Create input dataframe
input_data = pd.DataFrame({
    'selling_price': [price],
    'discount': [discount],
    'day': [day],
    'month': [month],
    
})

# 🔹 Predict demand
predicted_demand = model.predict(input_data)[0]
predicted_demand = max(0, predicted_demand)

# 🔹 Recommended price logic (small optimization)
recommended_price = price * (1 + 0.01 * (predicted_demand / 5))

# 🔹 Revenue calculations
current_revenue = price * predicted_demand
new_revenue = recommended_price * predicted_demand

if current_revenue != 0:
    revenue_lift = ((new_revenue - current_revenue) / current_revenue) * 100
else:
    revenue_lift = 0

# 🔹 Display outputs
st.header("📊 Pricing Recommendation")

st.success(f"💡 Recommended Price: ₹{recommended_price:.2f}")
st.info(f"📦 Predicted Demand: {predicted_demand:.2f}")

col1, col2 = st.columns(2)
col1.metric("Current Revenue", f"₹{current_revenue:.2f}")
col2.metric("Expected Revenue", f"₹{new_revenue:.2f}")

st.metric("Revenue Lift (%)", f"{revenue_lift:.2f}%")
# 🔹 Comparison Section
st.subheader("📈 Comparison")

comparison_df = pd.DataFrame({
    'Type': ['Current', 'Optimized'],
    'Price': [price, recommended_price],
    'Revenue': [current_revenue, new_revenue]
})

st.bar_chart(comparison_df.set_index('Type'))

# 🔹 Demand vs Price Simulation
st.subheader("📉 Price vs Demand Simulation")

price_range = np.linspace(price * 0.8, price * 1.2, 20)
demands = []

for p in price_range:
    temp = input_data.copy()
    temp['selling_price'] = p
    d = model.predict(temp)[0]
    demands.append(max(0, d))

fig, ax = plt.subplots()
ax.plot(price_range, demands)
ax.set_xlabel("Price")
ax.set_ylabel("Demand")
ax.set_title("Price vs Demand")

st.pyplot(fig)

# 🔹 Revenue comparison chart
st.subheader("💰 Revenue Comparison")

revenues = price_range * np.array(demands)

fig2, ax2 = plt.subplots()
ax2.plot(price_range, revenues)
ax2.set_xlabel("Price")
ax2.set_ylabel("Revenue")
ax2.set_title("Price vs Revenue")

st.pyplot(fig2)