# ===============================
# Advanced Model Development
# Dynamic Pricing - Milestone 5
# ===============================

import pandas as pd
import numpy as np
import time

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder

from xgboost import XGBRegressor
from lightgbm import LGBMRegressor


# ==========================================
# 1. LOAD DATASET
# ==========================================

file_path = "data/processed/retail_store_inventory_cleaned.csv"
raw_data = pd.read_csv(file_path)

print("Dataset Loaded Successfully")
print(raw_data.head())


# ==========================================
# 2. CLEAN / BASIC TRANSFORM
# ==========================================

raw_data.columns = raw_data.columns.str.strip().str.replace(" ", "_", regex=False).str.replace("/", "_", regex=False)

raw_data['Date'] = pd.to_datetime(raw_data['Date'], errors='coerce')
raw_data = raw_data.dropna(subset=['Date'])
raw_data = raw_data.sort_values('Date')

for col in ['Price', 'Competitor_Pricing', 'Inventory_Level', 'Discount', 'Units_Sold']:
    if col in raw_data.columns:
        raw_data[col] = pd.to_numeric(raw_data[col], errors='coerce')

raw_data = raw_data.dropna(subset=['Price', 'Competitor_Pricing', 'Inventory_Level', 'Units_Sold'])


# ==========================================
# 3. DATE FEATURES
# ==========================================

raw_data['hour'] = raw_data['Date'].dt.hour
raw_data['day_of_week'] = raw_data['Date'].dt.dayofweek
raw_data['Month'] = raw_data['Date'].dt.month
raw_data['week_of_year'] = raw_data['Date'].dt.isocalendar().week
raw_data['is_weekend'] = raw_data['day_of_week'].isin([5, 6]).astype(int)


# ==========================================
# 4. LAGS / ROLLING STATISTICS
# ==========================================

raw_data['lag_1_sales'] = raw_data['Units_Sold'].shift(1)
raw_data['lag_2_sales'] = raw_data['Units_Sold'].shift(2)
raw_data['rolling_mean_3'] = raw_data['Units_Sold'].rolling(3).mean()
raw_data['rolling_mean_7'] = raw_data['Units_Sold'].rolling(7).mean()


# ==========================================
# 5. ADD PRICE GAP
# ==========================================

raw_data['price_gap'] = raw_data['Price'] - raw_data['Competitor_Pricing']


# ==========================================
# 6. ENCODE CATEGORICALS
# ==========================================

categorical_columns = [
    'Category',
    'Weather_Condition',
    'Seasonality',
    'Store_ID',
    'Product_ID',
]

label_encoder = LabelEncoder()
for col in categorical_columns:
    if col in raw_data.columns:
        raw_data[col] = raw_data[col].fillna('missing').astype(str)
        raw_data[col] = label_encoder.fit_transform(raw_data[col])


# ==========================================
# 7. CLIP TARGET & DROP na
# ==========================================

clip_value = raw_data['Units_Sold'].quantile(0.99)
raw_data['Units_Sold_clipped'] = raw_data['Units_Sold'].clip(upper=clip_value)

raw_data = raw_data.dropna(subset=['lag_1_sales', 'lag_2_sales', 'rolling_mean_3', 'rolling_mean_7'])


# ==========================================
# 8. FEATURE SELECTION
# ==========================================

features = [
    'Price',
    'Competitor_Pricing',
    'price_gap',
    'Inventory_Level',
    'Discount',
    'Holiday_Promotion',
    'lag_1_sales',
    'lag_2_sales',
    'rolling_mean_3',
    'rolling_mean_7',
    'Month',
    'day_of_week',
    'week_of_year',
    'is_weekend',
    'Category',
    'Seasonality',
    'Weather_Condition',
]

features = [c for c in features if c in raw_data.columns]
target = 'Units_Sold_clipped'

data = raw_data.sort_values('Date')


# ==========================================
# 9. TIME-BASED SPLIT
# ==========================================

split_index = int(len(data) * 0.8)
train = data.iloc[:split_index]
test = data.iloc[split_index:]

X_train = train[features]
X_test = test[features]

y_train = np.log1p(train[target])    # log target train
y_test_log = np.log1p(test[target])  # log target test
y_test_real = test['Units_Sold']     # real target test for final metrics

print("\nTraining Size:", len(X_train))
print("Testing Size:", len(X_test))


# ==========================================
# 10. TRAIN MODELS WITH EARLY STOPPING
# ==========================================

print("\nTraining XGBoost Model...")

xgb_model = XGBRegressor(
    n_estimators=600,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.1,
    reg_lambda=1,
    random_state=42,
    n_jobs=-1,
    objective='reg:squarederror'
)

xgb_model.fit(
    X_train,
    y_train
)

print("\nTraining LightGBM Model...")

lgb_model = LGBMRegressor(
    n_estimators=600,
    learning_rate=0.05,
    max_depth=6,
    num_leaves=31,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.1,
    reg_lambda=1,
    random_state=42,
    n_jobs=-1
)

lgb_model.fit(
    X_train,
    y_train
)


# ==========================================
# 11. FEATURE IMPORTANCE
# ==========================================

feat_imp = pd.DataFrame({
    'feature': X_train.columns,
    'importance': xgb_model.feature_importances_
}).sort_values(by='importance', ascending=False)

print('\nXGBoost feature importance:\n', feat_imp)


# ==========================================
# 12. MODEL EVALUATION
# ==========================================

def evaluate_model(name, y_true, preds):
    rmse = np.sqrt(mean_squared_error(y_true, preds))
    mae = mean_absolute_error(y_true, preds)
    r2 = r2_score(y_true, preds)
    print(f"\n{name} Performance")
    print("----------------------")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE : {mae:.4f}")
    print(f"R2  : {r2:.4f}")
    return rmse, mae, r2

xgb_pred_log = xgb_model.predict(X_test)
lgb_pred_log = lgb_model.predict(X_test)

xgb_pred_real = np.expm1(xgb_pred_log)
lgb_pred_real = np.expm1(lgb_pred_log)

xgb_pred_real = np.clip(xgb_pred_real, 0, data['Units_Sold'].max())
lgb_pred_real = np.clip(lgb_pred_real, 0, data['Units_Sold'].max())

xgb_rmse_real, xgb_mae_real, xgb_r2_real = evaluate_model('XGBoost (real target)', y_test_real, xgb_pred_real)
lgb_rmse_real, lgb_mae_real, lgb_r2_real = evaluate_model('LightGBM (real target)', y_test_real, lgb_pred_real)

xgb_rmse_log, xgb_mae_log, xgb_r2_log = evaluate_model('XGBoost (log target)', y_test_log, xgb_pred_log)
lgb_rmse_log, lgb_mae_log, lgb_r2_log = evaluate_model('LightGBM (log target)', y_test_log, lgb_pred_log)


# ==========================================
# 13. CHECK GOAL AND PRINT GUIDE
# ==========================================

print('\nDesired metric targets: RMSE<3, MAE<3, 0.92<=R2<=0.97 (log target)')

for model, rmse, mae, r2 in [
    ('XGBoost (log)', xgb_rmse_log, xgb_mae_log, xgb_r2_log),
    ('LightGBM (log)', lgb_rmse_log, lgb_mae_log, lgb_r2_log)
]:
    status = 'PASS' if (rmse < 3 and mae < 3 and 0.92 <= r2 <= 0.97) else 'RETRY'
    print(f"{model}: RMSE={rmse:.4f}, MAE={mae:.4f}, R2={r2:.4f} -> {status}")

if xgb_rmse_log >= 3 or xgb_mae_log >= 3 or not (0.92 <= xgb_r2_log <= 0.97):
    print('Note: try further tuning, remove outliers, or use model ensembling for target goals.')


# ==========================================
# 14. BACKTESTING
# ==========================================

print('\nRunning Backtesting Simulation...')

historical_revenue = np.sum(data['Price'] * data['Units_Sold'])

data['ml_price'] = data['Competitor_Pricing'] * 1.02

X_back = data[features].copy()
X_back['Price'] = data['ml_price']

# Predict with XGBoost
xgb_back_pred = np.expm1(xgb_model.predict(X_back))
xgb_back_pred = np.clip(xgb_back_pred, 0, data['Units_Sold'].max())

data['xgb_pred_demand'] = xgb_back_pred
data['xgb_revenue'] = data['ml_price'] * data['xgb_pred_demand']

xgb_revenue = np.sum(data['xgb_revenue'])
xgb_lift = (xgb_revenue - historical_revenue) / historical_revenue * 100

# Predict with LightGBM
lgb_back_pred = np.expm1(lgb_model.predict(X_back))
lgb_back_pred = np.clip(lgb_back_pred, 0, data['Units_Sold'].max())

data['lgb_pred_demand'] = lgb_back_pred
data['lgb_revenue'] = data['ml_price'] * data['lgb_pred_demand']

lgb_revenue = np.sum(data['lgb_revenue'])
lgb_lift = (lgb_revenue - historical_revenue) / historical_revenue * 100

print('Historical Revenue:', historical_revenue)
print('XGBoost Revenue:', xgb_revenue)
print('LightGBM Revenue:', lgb_revenue)

print('XGBoost Revenue Lift:', f'{xgb_lift:.2f}%')
print('LightGBM Revenue Lift:', f'{lgb_lift:.2f}%')


data[['Date','Price','ml_price','Units_Sold','xgb_pred_demand','lgb_pred_demand','xgb_revenue','lgb_revenue']].to_csv('model_backtesting_results.csv', index=False)
print('Backtesting results saved as: model_backtesting_results.csv')
