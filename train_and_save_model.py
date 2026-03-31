import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

# Create models folder
os.makedirs("models", exist_ok=True)

# Load dataset
df = pd.read_csv("data/sales_data.csv")

print("Dataset loaded successfully")
print("Columns:", df.columns.tolist())
print("Shape:", df.shape)

# Keep only required columns
df = df[[
    "Price",
    "Inventory Level",
    "Discount",
    "Competitor Pricing",
    "Units Sold"
]].copy()

# Rename columns
df.columns = [
    "current_price",
    "inventory_level",
    "discount",
    "competitor_price",
    "units_sold"
]

# Remove missing values
df = df.dropna()

print("Shape after dropna:", df.shape)

# Use smaller sample for faster training
df = df.sample(n=min(15000, len(df)), random_state=42)

print("Shape after sampling:", df.shape)

# Features and target
X = df[[
    "current_price",
    "inventory_level",
    "discount",
    "competitor_price"
]]
y = df["units_sold"]

print("Training started...")

# Faster model
model = RandomForestRegressor(
    n_estimators=20,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)

model.fit(X, y)

print("Model trained successfully")

# Save model and features
joblib.dump(model, "models/best_model.pkl")
joblib.dump(X.columns.tolist(), "models/model_features.pkl")

print("Model and features saved successfully")