import joblib
import pandas as pd

# Load trained model
model = joblib.load("models/best_model.pkl")


def predict_demand(
        price,
        discount,
        shipping_cost,
        month,
        day_of_week
):

    # Create input dataframe
    input_data = pd.DataFrame([{

        "price": price,
        "Discount": discount,
        "Shipping Cost": shipping_cost,
        "month": month,
        "day_of_week": day_of_week

    }])

    # Predict demand
    prediction = model.predict(input_data)

    return prediction[0]