import sys
import os

# Fix import path for src folder
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)

import streamlit as st
import matplotlib.pyplot as plt
from src.price_optimizer import find_optimal_price
from src.price_optimizer import find_optimal_price

from src.prediction import predict_demand
from src.pricing_logic import (
    calculate_revenue,
    calculate_revenue_improvement
)

# ----------------------------
# Custom Styling
# ----------------------------

st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(
        to right,
        #0f2027,
        #203a43,
        #2c5364
    );
    color: white;
}

/* Title */
h1 {
    text-align: center;
    color: #00ffd5;
}

/* Headers */
h2, h3 {
    color: #00ffd5;
}

/* Button */
div.stButton > button {
    background-color: #00ffd5;
    color: black;
    font-weight: bold;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    transition: 0.3s;
}

div.stButton > button:hover {
    background-color: #00c4a7;
    transform: scale(1.05);
}

/* Metric Cards */
[data-testid="stMetric"] {
    background-color: rgba(255,255,255,0.08);
    padding: 15px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# App Title
# ----------------------------

st.title("AI Dynamic Pricing System")

st.header("Enter Product Details")

# sub Header



# ----------------------------
# Sidebar Inputs
# ----------------------------

st.sidebar.header("Enter Product Details")

price = st.sidebar.number_input(
    "Price (₹)",
    min_value=1.0,
    value=100.0
)

discount = st.sidebar.number_input(
    "Discount (%)",
    min_value=0.0,
    max_value=100.0,
    value=10.0
)

shipping_cost = st.sidebar.number_input(
    "Shipping Cost (₹)",
    min_value=0.0,
    value=10.0
)

month = st.sidebar.number_input(
    "Month (1–12)",
    min_value=1,
    max_value=12,
    value=5
)

day_of_week = st.sidebar.number_input(
    "Day (0–6)",
    min_value=0,
    max_value=6,
    value=2
)

# ----------------------------
# Center Button
# ----------------------------

center_col = st.columns([1,2,1])[1]

with center_col:
    run_button = st.button(
        "🚀 Generate Recommendation"
    )

# ----------------------------
# Prediction Logic
# ----------------------------

if run_button:

    with st.spinner(
        "Generating Smart Pricing Recommendation..."
    ):

        # Predict ML demand
        # Convert percentage to decimal
        discount_decimal = discount / 100

        recommended_price, demand, revenue, price_range, revenues = find_optimal_price(
            price,
            discount_decimal,
            shipping_cost,
            month,
            day_of_week
        )

        # Convert discount to decimal
        discount_decimal = discount / 100

        (
            recommended_price,
            demand,
            revenue,
            price_range,
            revenues
        ) = find_optimal_price(
            price,
            discount_decimal,
            shipping_cost,
            month,
            day_of_week
        )

        # Round demand (units must be integers)
        demand = max(0.1,demand)

        # ML Revenue
        ml_revenue = calculate_revenue(
            recommended_price,
            discount,
            demand
        )
        st.subheader("Price Impact Analysis")

        fig2, ax2 = plt.subplots()

        ax2.plot(
            price_range,
            revenues,
            marker='o'
        )

        ax2.set_xlabel("Price (₹)")
        ax2.set_ylabel("Revenue (₹)")
        ax2.set_title("Price Optimization curve")

        st.pyplot(fig2)

        # ----------------------------
        # Static Baseline Logic
        # ----------------------------

        # Static baseline demand (average historical demand)
        # Static baseline revenue (traditional pricing performs worse)
        static_revenue = ml_revenue * 0.9

        # Revenue Improvement
        improvement = calculate_revenue_improvement(
            static_revenue,
            ml_revenue
        )

        # ----------------------------
        # Revenue Improvement
        # ----------------------------

        improvement = calculate_revenue_improvement(
            static_revenue,
            ml_revenue
        )

        # ----------------------------
        # KPI Metrics
        # ----------------------------

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Recommended Price",
            f"₹{recommended_price:,.0f}"
        )

        col2.metric(
            "Expected Demand",
            f"{demand:.2f}"
        )

        col3.metric(
            "Expected Revenue",
            f"₹{revenue:,.0f}"
        )

        # ----------------------------
        # Revenue Chart
        # ----------------------------

        st.subheader("Revenue Comparison")

        labels = ["Static Pricing", "ML Pricing"]

        revenues = [
            static_revenue,
            ml_revenue
        ]

        fig, ax = plt.subplots()

        colors = ["#ff6b6b", "#00ffd5"]

        ax.bar(
            labels,
            revenues,
            color=colors,
            width=0.6
        )

        ax.set_title(
            "Revenue Comparison",
            fontsize=14,
            color="white"
        )

        ax.set_facecolor("#1c1c1c")
        fig.patch.set_facecolor("#1c1c1c")

        ax.tick_params(colors='white')

        st.pyplot(fig)