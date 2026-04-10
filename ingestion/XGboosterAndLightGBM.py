import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder

from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
import os

import joblib
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "processed",
    "amazon_sales_dynamic_pricing.csv"
)

file_path = os.path.abspath(file_path)

print("Loading from:", file_path)
print("File exists:", os.path.exists(file_path))

df = pd.read_csv(file_path)

# Date feature extraction
if "order_date" in df.columns:
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["day"] = df["order_date"].dt.day
    df["month"] = df["order_date"].dt.month
    df["year"] = df["order_date"].dt.year
    df["day_of_week"] = df["order_date"].dt.dayofweek
    df["week_of_year"] = df["order_date"].dt.isocalendar().week.astype(int)
    df["is_weekend"] = df["day_of_week"].apply(lambda x: 1 if x >= 5 else 0)

# Encode categorical columns
encoders = {}

categorical_cols = [
    "product_id",
    "product_category",
    "customer_region",
    "payment_method"
]

for col in categorical_cols:
    if col in df.columns:
        encoder = LabelEncoder()
        df[col] = encoder.fit_transform(df[col].astype(str))
        encoders[col] = encoder

# Feature selection
target = "quantity_sold"

possible_features = [
    'price', 'discount_percent', 'inventory_level', 'rating', 'review_count',
    'product_id', 'product_category', 'customer_region', 'payment_method',
    'day', 'month', 'year', 'day_of_week', 'week_of_year', 'is_weekend'
]
features = [col for col in possible_features if col in df.columns]
print("Columns in dataset:\n", df.columns)

X = df[features]
y = df[target]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train XGBoost
xgb_model = XGBRegressor(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

xgb_model.fit(X_train, y_train)
xgb_preds = xgb_model.predict(X_test)

# Train LightGBM
lgbm_model = LGBMRegressor(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=6,
    random_state=42
)

lgbm_model.fit(X_train, y_train)
lgbm_preds = lgbm_model.predict(X_test)

# Evaluation function
def evaluate_model(name, y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)

    print(f"\n{name} Results")
    print(f"MAE  : {mae:.4f}")
    print(f"RMSE : {rmse:.4f}")
    print(f"R²   : {r2:.4f}")

    return {
        "Model": name,
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    }

xgb_results = evaluate_model("XGBoost", y_test, xgb_preds)
lgbm_results = evaluate_model("LightGBM", y_test, lgbm_preds)

# Rule-based pricing
def apply_rule_based_price(row):
    price = row["price"]
    inventory = row["inventory_level"] if "inventory_level" in row.index else None

    if inventory is not None:
        if inventory < 20:
            return price * 1.10
        elif inventory > 100:
            return price * 0.90

    return price

# ML-based pricing simulation
def simulate_best_price(row, model, candidate_changes=None):
    if candidate_changes is None:
        candidate_changes = [-0.10, -0.05, 0.0, 0.05, 0.10]

    best_price = row["price"]
    best_revenue = -1
    best_demand = 0

    for change in candidate_changes:
        test_row = row.copy()
        new_price = row["price"] * (1 + change)
        test_row["price"] = new_price

        demand_pred = model.predict(pd.DataFrame([test_row[features]]))[0]
        demand_pred = max(demand_pred, 0)

        revenue = new_price * demand_pred

        if revenue > best_revenue:
            best_revenue = revenue
            best_price = new_price
            best_demand = demand_pred

    return best_price, best_demand, best_revenue

# Backtesting
backtest_df = X_test.copy()
backtest_df["actual_quantity_sold"] = y_test.values
backtest_df["original_price"] = backtest_df["price"]

# Static pricing revenue
backtest_df["static_revenue"] = (
    backtest_df["original_price"] * backtest_df["actual_quantity_sold"]
)

# Rule-based pricing revenue
backtest_df["rule_price"] = backtest_df.apply(apply_rule_based_price, axis=1)
backtest_df["rule_predicted_quantity"] = backtest_df["actual_quantity_sold"]
backtest_df["rule_revenue"] = (
    backtest_df["rule_price"] * backtest_df["rule_predicted_quantity"]
)

# ML-based pricing revenue using XGBoost
ml_prices = []
ml_demands = []
ml_revenues = []

for _, row in backtest_df.iterrows():
    best_price, best_demand, best_revenue = simulate_best_price(row, xgb_model)
    ml_prices.append(best_price)
    ml_demands.append(best_demand)
    ml_revenues.append(best_revenue)

backtest_df["ml_price"] = ml_prices
backtest_df["ml_predicted_demand"] = ml_demands
backtest_df["ml_revenue"] = ml_revenues

# Revenue comparison
static_revenue = backtest_df["static_revenue"].sum()
rule_revenue = backtest_df["rule_revenue"].sum()
ml_revenue = backtest_df["ml_revenue"].sum()

rule_lift = ((rule_revenue - static_revenue) / static_revenue) * 100
ml_lift = ((ml_revenue - static_revenue) / static_revenue) * 100

print("\nRevenue Comparison")
print(f"Static Pricing Revenue    : {static_revenue:.2f}")
print(f"Rule-Based Pricing Revenue: {rule_revenue:.2f}")
print(f"ML-Based Pricing Revenue  : {ml_revenue:.2f}")

print("\nRevenue Lift")
print(f"Rule-Based Lift over Static: {rule_lift:.2f}%")
print(f"ML-Based Lift over Static  : {ml_lift:.2f}%")

# Save tables
evaluation_df = pd.DataFrame([xgb_results, lgbm_results])

revenue_summary = pd.DataFrame({
    "Strategy": ["Static Pricing", "Rule-Based Pricing", "ML-Based Pricing"],
    "Revenue": [static_revenue, rule_revenue, ml_revenue],
    "Revenue Lift (%)": [0, rule_lift, ml_lift]
})

evaluation_df.to_csv("model_evaluation_results.csv", index=False)
revenue_summary.to_csv("revenue_comparison_results.csv", index=False)
backtest_df.to_csv("backtesting_results.csv", index=False)

print("\nFiles saved:")
print("- model_evaluation_results.csv")
print("- revenue_comparison_results.csv")
print("- backtesting_results.csv")

# Graphs
# 1. Actual vs Predicted - XGBoost
plt.figure(figsize=(8, 6))
plt.scatter(y_test, xgb_preds, alpha=0.6)
plt.xlabel("Actual Demand")
plt.ylabel("Predicted Demand")
plt.title("XGBoost: Actual vs Predicted Demand")
plt.grid(True)
plt.show()

# 2. Actual vs Predicted - LightGBM
plt.figure(figsize=(8, 6))
plt.scatter(y_test, lgbm_preds, alpha=0.6)
plt.xlabel("Actual Demand")
plt.ylabel("Predicted Demand")
plt.title("LightGBM: Actual vs Predicted Demand")
plt.grid(True)
plt.show()

# 3. MAE Comparison
models = ["XGBoost", "LightGBM"]
mae_values = [xgb_results["MAE"], lgbm_results["MAE"]]

plt.figure(figsize=(8, 6))
plt.bar(models, mae_values)
plt.xlabel("Models")
plt.ylabel("MAE")
plt.title("MAE Comparison")
plt.grid(axis="y")
plt.show()

# 4. RMSE Comparison
rmse_values = [xgb_results["RMSE"], lgbm_results["RMSE"]]

plt.figure(figsize=(8, 6))
plt.bar(models, rmse_values)
plt.xlabel("Models")
plt.ylabel("RMSE")
plt.title("RMSE Comparison")
plt.grid(axis="y")
plt.show()

# 5. R² Comparison
r2_values = [xgb_results["R2"], lgbm_results["R2"]]

plt.figure(figsize=(8, 6))
plt.bar(models, r2_values)
plt.xlabel("Models")
plt.ylabel("R² Score")
plt.title("R² Comparison")
plt.grid(axis="y")
plt.show()

# 6. Revenue Comparison
strategies = ["Static", "Rule-Based", "ML-Based"]
revenues = [static_revenue, rule_revenue, ml_revenue]

plt.figure(figsize=(8, 6))
plt.bar(strategies, revenues)
plt.xlabel("Pricing Strategy")
plt.ylabel("Revenue")
plt.title("Revenue Comparison")
plt.grid(axis="y")
plt.show()

# 7. Revenue Lift Comparison
lift_values = [0, rule_lift, ml_lift]

plt.figure(figsize=(8, 6))
plt.bar(strategies, lift_values)
plt.xlabel("Pricing Strategy")
plt.ylabel("Revenue Lift (%)")
plt.title("Revenue Lift Comparison")
plt.grid(axis="y")
plt.show()

# 8. Combined model metric comparison
metric_names = ["MAE", "RMSE", "R2"]
xgb_metric_values = [xgb_results["MAE"], xgb_results["RMSE"], xgb_results["R2"]]
lgbm_metric_values = [lgbm_results["MAE"], lgbm_results["RMSE"], lgbm_results["R2"]]

x = np.arange(len(metric_names))
width = 0.35

plt.figure(figsize=(10, 6))
plt.bar(x - width/2, xgb_metric_values, width, label="XGBoost")
plt.bar(x + width/2, lgbm_metric_values, width, label="LightGBM")
plt.xticks(x, metric_names)
plt.xlabel("Metrics")
plt.ylabel("Values")
plt.title("XGBoost vs LightGBM Metrics Comparison")
plt.legend()
plt.grid(axis="y")
plt.show()


# ✅ FIX 4: Cleaned up model saving (deleted pickle, kept joblib)
model_dir = os.path.join(BASE_DIR, "..", "models")
os.makedirs(model_dir, exist_ok=True) # Creates a 'models' folder if it doesn't exist

joblib.dump(xgb_model, os.path.join(model_dir, "xgb_model.pkl"))
joblib.dump(encoders, os.path.join(model_dir, "encoders.pkl"))
joblib.dump(possible_features, os.path.join(model_dir, "features.pkl"))

print(f"\nModels and encoders saved to {model_dir}")