def calculate_revenue(price, discount, demand):

    # Apply discount to price
    effective_price = price * (1 - discount / 100)

    # Calculate revenue
    revenue = effective_price * demand

    return revenue


def calculate_revenue_improvement(
        static_revenue,
        ml_revenue
):

    # Avoid division error
    if static_revenue == 0:
        return 0

    improvement = (
        (ml_revenue - static_revenue)
        / static_revenue
    ) * 100

    return improvement