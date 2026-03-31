import pandas as pd
from xgboost import XGBRegressor
import pickle

# Load dataset
df = pd.read_csv("sample_data.csv")

# Check columns
print(df.columns)

# Select features 
X = df[['Price', 'Inventory Level', 'Competitor Pricing', 'Demand Forecast']]
y = df['Units Ordered']

# Rename for Streamlit
X.columns = ['price', 'inventory', 'competitor_price', 'demand_index']

# Train model
model = XGBRegressor()
model.fit(X, y)

# Save model
pickle.dump(model, open("xgb_model.pkl", "wb"))

print("✅ Model trained successfully!")