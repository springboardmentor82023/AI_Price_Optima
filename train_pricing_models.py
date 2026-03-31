"""Train and backtest dynamic pricing models.

This script trains XGBoost and LightGBM regression models to predict demand (units sold)
based on historical pricing, product/store attributes, and external signals.

The backtest simulates pricing decisions by selecting the price that maximizes
predicted revenue (price * predicted_units_sold) for each row in the test set.

Usage:
  python train_pricing_models.py

Optional:
  python train_pricing_models.py --data-path data/processed/retail_store_inventory_cleaned.csv \
      --output-dir models --no-backtest

"""

import argparse
import os
import subprocess
import sys

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Optional dependencies
try:
    import lightgbm as lgb
except ImportError:  # pragma: no cover
    lgb = None

try:
    import xgboost as xgb
except ImportError:  # pragma: no cover
    xgb = None


def _check_dependencies():
    missing = []
    if xgb is None:
        missing.append("xgboost")
    if lgb is None:
        missing.append("lightgbm")

    if missing:
        raise ImportError(
            "Missing required packages: {}. "
            "Install them with `pip install {}".format(
                ", ".join(missing), " ".join(missing)
            )
        )


def _install_packages(packages: list[str]) -> None:
    """Install missing packages via pip."""

    if not packages:
        return

    cmd = [sys.executable, "-m", "pip", "install"] + packages
    print("Installing missing dependencies:", " ".join(packages))
    subprocess.check_call(cmd)


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])

    # Keep only numeric/feature columns we expect downstream.
    df = df.copy()
    return df


def featurize(df: pd.DataFrame) -> (pd.DataFrame, pd.Series, list):
    """Create feature matrix X and targets y."""

    df = df.copy()

    # Engineering: time-based features
    df["Month"] = df["Date"].dt.month
    df["DayOfWeek"] = df["Date"].dt.dayofweek

    # Target: units sold
    y = df["Units Sold"].astype(float)

    # Candidate feature set
    base_features = [
        "Price",
        "Discount",
        "Inventory Level",
        "Demand Forecast",
        "Competitor Pricing",
        "Month",
        "DayOfWeek",
    ]

    categorical_features = [
        "Store ID",
        "Product ID",
        "Category",
        "Region",
        "Weather Condition",
        "Seasonality",
        "Holiday/Promotion",
    ]

    # Ensure these columns exist and fill missing values
    for col in base_features + categorical_features:
        if col not in df.columns:
            raise KeyError(f"Expected column '{col}' not found in data")

    # Fill missing values for numeric columns with median (as upstream ingestion does)
    df[base_features] = df[base_features].apply(lambda s: s.fillna(s.median()))

    # Fill missing values for categoricals
    for col in categorical_features:
        df[col] = df[col].fillna("<MISSING>")

    # Build preprocessing pipeline
    numeric_transformer = Pipeline(
        steps=[("scaler", StandardScaler())]
    )

    categorical_transformer = Pipeline(
        steps=[("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, base_features),
            ("cat", categorical_transformer, categorical_features),
        ],
        remainder="drop",
    )

    X = preprocessor.fit_transform(df)

    feature_names = (
        base_features
        + list(
            preprocessor.named_transformers_["cat"]
            .named_steps["onehot"]
            .get_feature_names_out(categorical_features)
        )
    )

    return X, y, feature_names, preprocessor


def split_train_test(df: pd.DataFrame, test_size: float = 0.2):
    """Time-aware train/test split."""

    df = df.sort_values("Date")
    split_index = int(len(df) * (1 - test_size))

    train = df.iloc[:split_index].reset_index(drop=True)
    test = df.iloc[split_index:].reset_index(drop=True)

    return train, test


def fit_model(model_name: str, X_train, y_train):
    if model_name == "xgb":
        _check_dependencies()
        model = xgb.XGBRegressor(
            objective="reg:squarederror",
            n_estimators=200,
            learning_rate=0.1,
            random_state=42,
            n_jobs=-1,
        )
    elif model_name == "lgbm":
        _check_dependencies()
        model = lgb.LGBMRegressor(
            n_estimators=200,
            learning_rate=0.1,
            random_state=42,
            n_jobs=-1,
        )
    else:
        raise ValueError("model_name must be one of ['xgb', 'lgbm']")

    model.fit(X_train, y_train)
    return model


def evaluate_regression(y_true, y_pred, prefix=""):
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    print(f"{prefix}RMSE: {rmse:.2f}")
    print(f"{prefix}MAE:  {mae:.2f}")
    print(f"{prefix}R2:   {r2:.3f}")
    
    return {"rmse": rmse, "mae": mae, "r2": r2}


def apply_rule_based_pricing(df: pd.DataFrame) -> pd.DataFrame:
    """Apply rule-based pricing logic from Milestone 4."""
    df = df.copy()
    
    # Ensure required columns exist
    required_cols = ["Price", "Month", "Inventory Level", "Weather Condition", 
                     "DayOfWeek", "Demand Forecast", "Units Sold", "Competitor Pricing"]
    for col in required_cols:
        if col not in df.columns:
            raise KeyError(f"Required column '{col}' not found for rule-based pricing")
    
    def pricing_engine(row):
        price = row["Price"]
        month = row["Month"]
        inventory = row["Inventory Level"]
        weather = row["Weather Condition"]
        day = row["DayOfWeek"]
        forecast = row.get("Demand Forecast", np.nan)
        units = row.get("Units Sold", np.nan)
        comp = row.get("Competitor Pricing", np.nan)
        
        # Monthly rule
        if month in [4, 12]:
            price *= 1.15
        elif month in [3, 10]:
            price *= 0.90
        
        # Weather rule
        if weather == "Cloudy":
            price *= 1.05
        
        # Weekend rule
        if day in [5, 6]:  # Saturday or Sunday
            price *= 1.07
        
        # High-volume/forecast rule
        if pd.notna(forecast) and pd.notna(units) and forecast > units * 1.2:
            price *= 1.12
        
        # High-volume threshold
        if pd.notna(units) and units > 203:  # 75th percentile
            price *= 1.08
        
        # Competitor gap
        if pd.notna(comp):
            gap = comp - price
            if gap >= 2:
                price *= 1.05
            elif gap <= -2:
                price *= 0.95
        
        # Scarcity check
        if pd.notna(forecast) and pd.notna(inventory) and inventory < 200 and forecast > units * 1.2:
            price *= 1.10
        
        return price
    
    df["Rule-Based Price"] = df.apply(pricing_engine, axis=1)
    df["Rule-Based Revenue"] = df["Rule-Based Price"] * df["Units Sold"]
    
    return df


def simulate_revenue(
    df: pd.DataFrame,
    preprocessor,
    model,
    price_grid=None,
    price_col: str = "Price",
    units_col: str = "Units Sold",
    verbose: bool = False,
):
    """Simulate revenue by choosing a price that maximizes predicted revenue."""
    
    if price_grid is None:
        # Relative grid around current price (reduced for faster testing)
        price_grid = np.linspace(0.8, 1.2, 11)
    
    df = df.copy().reset_index(drop=True)
    
    # Feature engineering that must match training.
    df["Month"] = df["Date"].dt.month
    df["DayOfWeek"] = df["Date"].dt.dayofweek
    
    # Apply rule-based pricing first
    df = apply_rule_based_pricing(df)
    
    best_prices = []
    best_rev = []
    best_pred_units = []
    
    for idx, row in df.iterrows():
        candidate_prices = row[price_col] * price_grid
        
        revenues = []
        predicted_units = []
        for p in candidate_prices:
            row_copy = row.copy()
            row_copy[price_col] = p
            
            row_df = pd.DataFrame([row_copy])
            X_test = preprocessor.transform(row_df)
            
            units_pred = model.predict(X_test)[0]
            revenues.append(p * max(units_pred, 0))
            predicted_units.append(units_pred)
        
        best_idx = int(np.nanargmax(revenues))
        best_prices.append(candidate_prices[best_idx])
        best_rev.append(revenues[best_idx])
        best_pred_units.append(predicted_units[best_idx])
        
        if verbose and idx % 5000 == 0 and idx > 0:
            print(f"  simulated {idx}/{len(df)} rows")
    
    df["Optimized Price"] = best_prices
    df["Optimized Units Pred"] = best_pred_units
    df["ML Revenue"] = best_rev
    
    df["Static Revenue"] = df[price_col] * df[units_col]
    
    # Calculate revenue lift comparisons
    total_static = df["Static Revenue"].sum()
    total_rule_based = df["Rule-Based Revenue"].sum()
    total_ml = df["ML Revenue"].sum()
    
    rule_based_lift = (total_rule_based - total_static) / total_static * 100
    ml_lift = (total_ml - total_static) / total_static * 100
    ml_vs_rule_based_lift = (total_ml - total_rule_based) / total_rule_based * 100
    
    print(f"Static revenue: {total_static:,.0f}")
    print(f"Rule-Based revenue: {total_rule_based:,.0f}")
    print(f"ML revenue: {total_ml:,.0f}")
    print(f"Rule-Based lift vs Static: {rule_based_lift:.2f}%")
    print(f"ML lift vs Static: {ml_lift:.2f}%")
    print(f"ML lift vs Rule-Based: {ml_vs_rule_based_lift:.2f}%")
    
    return df, ml_lift


def main():
    global xgb, lgb
    parser = argparse.ArgumentParser(description="Train pricing models and backtest revenue uplift.")
    parser.add_argument(
        "--data-path",
        default="data/processed/retail_store_inventory_cleaned.csv",
        help="Path to cleaned input CSV.",
    )
    parser.add_argument(
        "--output-dir",
        default="models",
        help="Directory to write trained model artifacts.",
    )
    parser.add_argument(
        "--no-backtest",
        action="store_true",
        help="Skip revenue backtesting (only train and evaluate).",
    )
    parser.add_argument(
        "--random-seed",
        type=int,
        default=42,
        help="Random seed for splits and model training.",
    )
    parser.add_argument(
        "--install-deps",
        action="store_true",
        help="Attempt to install missing dependencies (xgboost/lightgbm) via pip.",
    )
    args = parser.parse_args()

    np.random.seed(args.random_seed)

    if args.install_deps:
        missing = []
        if xgb is None:
            missing.append("xgboost")
        if lgb is None:
            missing.append("lightgbm")
        if missing:
            _install_packages(missing)
            # Re-import after install (global variables set at function scope).
            try:
                import xgboost as xgb
            except ImportError:
                xgb = None
            try:
                import lightgbm as lgb
            except ImportError:
                lgb = None

    df = load_data(args.data_path)

    train_df, test_df = split_train_test(df, test_size=0.2)
    print(f"Training on {len(train_df)} rows, testing on {len(test_df)} rows")

    X_train, y_train, feature_names, preprocessor = featurize(train_df)
    X_test, y_test, _, _ = featurize(test_df)

    # Train models
    results = {}
    for model_name in ["xgb", "lgbm"]:
        if (model_name == "xgb" and xgb is None) or (model_name == "lgbm" and lgb is None):
            print(f"Skipping {model_name}: package not installed")
            continue

        print(f"Training {model_name}...")
        model = fit_model(model_name, X_train, y_train)

        y_pred = model.predict(X_test)
        results[model_name] = evaluate_regression(y_test, y_pred, prefix=f"[{model_name}] ")

        # Save model
        os.makedirs(args.output_dir, exist_ok=True)
        output_path = os.path.join(args.output_dir, f"{model_name}_units_sold_model.pkl")
        try:
            import joblib

            joblib.dump({"model": model, "preprocessor": preprocessor, "features": feature_names}, output_path)
            print(f"Saved {model_name} artifact to {output_path}")
        except ImportError:
            print("joblib not installed; skipping model serialization")

        if not args.no_backtest:
            print("Running revenue backtest (this can take a bit)...")
            backtest_df, lift_pct = simulate_revenue(
                test_df,
                preprocessor,
                model,
                price_grid=np.linspace(0.8, 1.2, 21),
                verbose=True,
            )
            out_backtest = os.path.join(args.output_dir, f"{model_name}_backtest.csv")
            backtest_df.to_csv(out_backtest, index=False)
            print(f"Backtest results written to {out_backtest}\n")

    print("Done")

    # Final summary
    print("\n" + "="*50)
    print("MILESTONE 5 SUMMARY")
    print("="*50)
    print("Models Implemented: XGBoost, LightGBM")
    print("Target Variable: Units Sold (demand prediction)")
    print("Features Used:")
    print("  - Price")
    print("  - Discount")
    print("  - Inventory Level")
    print("  - Demand Forecast")
    print("  - Competitor Pricing")
    print("  - Month, DayOfWeek (time features)")
    print("  - Categorical: Store ID, Product ID, Category, Region, Weather Condition, Seasonality, Holiday/Promotion")
    print("Preprocessing: StandardScaler for numeric, OneHotEncoder for categorical")
    print("Evaluation Metrics: RMSE, MAE, R²")
    print("Backtesting: Simulated optimal pricing using model predictions")
    print("Revenue Scenarios: Static, Rule-Based (Milestone 4), ML-Based")
    print("Revenue Lift Formula: (New Revenue - Static Revenue) / Static Revenue * 100")
    print("="*50)


if __name__ == "__main__":
    main()
