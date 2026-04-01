import numpy as np
from src.prediction import predict_demand

def find_optimal_price(
    current_price,
    discount,
    shipping_cost,
    month,
    day_of_week
):

    # Generate price range
    price_range = np.linspace(
        current_price * 0.5,
        current_price * 1.5,
        20
    )

    best_price = current_price
    best_revenue = 0
    best_demand = 0

    revenues = []

    for price in price_range:

        demand = predict_demand(
            price,
            discount,
            shipping_cost,
            month,
            day_of_week
        )

        revenue = price * demand

        revenues.append(revenue)

        if revenue > best_revenue:
            best_revenue = revenue
            best_price = price
            best_demand = demand

    return (
        best_price,
        best_demand,
        best_revenue,
        price_range,
        revenues
    )