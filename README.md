# 💰 AI Price Optima
## Dynamic Pricing System with ML-Powered Recommendations

AI Price Optima is a fully functioning dynamic pricing tool that combines ML (XGBoost + LightGBM) with business rules to recommend optimized prices and maximize revenue for each product.

---

## Project Overview
AI Price Optima enables retailers and e-commerce teams to generate pricing recommendations through a friendly Streamlit dashboard and model inference pipeline.

### Objective of the dynamic pricing system
- Increase revenue per SKU.
- Optimize margins in real time.
- Reduce manual pricing effort.

### Problem statement
Manual or static price management is often insufficient when demand, competition, seasonality, and inventory change rapidly. This system delivers automated ML recommendations to close that gap.

---

## Dataset Description
### Source of data
- `data/processed/retail_store_inventory_cleaned.csv` (cleaned retail transactions historic dataset).
- Derived from internal retail performance history and competitor/market information.

### Features used
- `product_id`, `category`, `store_id`
- `current_price`, `competitor_price`, `cost`, `margin`
- `inventory`, `units_sold`, `promo_flag`
- `season`, `weather_condition`, `holiday_flag`, `day_of_week`, `month`
- Additional engineered features: `price_gap`, `inventory_ratio`, `demand_trend`, `competitor_diff`

---

## Project Workflow
1. Data ingestion (ingest.py)
2. Data processing & EDA (EDA.py)
3. Baseline pricing rules (pricingEngine.py)
4. Model training (modelTrain.py, train_pricing_models.py)
5. Dashboard deployment (app.py, run_dashboard.py)

### Data Ingestion
- Load raw records, cleanup, store in `data/processed/`.
- Validate schema and missing values.

### Data Processing
- Enrich data with season, weather, competitor spread, and inventory ratios.
- Encode categories and normalize numerical features.

### EDA
- Use `EDA.py` to inspect trends and demand elasticity.
- Evaluate relationships: price vs units sold, season vs demand.

### Baseline Pricing
- Apply rule-based strategy for comparison.
- Rules founded on cost+margin and competitor bounds.

### ML Model Development
- Train XGBoost and LightGBM models for units sold prediction.
- Ensemble by averaging outputs for stability.
- Evaluate R², RMSE, MAE.

### Deployment
- Streamlit front-end in `app.py`.
- Launch helper in `run_dashboard.py`.

---

## Model Details
### XGBoost and LightGBM explanation
- XGBoost: gradient boosting with weighted quantile sketch for robust tree construction.
- LightGBM: leaf-wise tree growth for efficiency with large datasets.
- Ensemble uses average of predictions from both model files (`models/xgb_units_sold_model.pkl`, `models/lgbm_units_sold_model.pkl`).

### Features used
- All features described in dataset section, plus derived features for price elasticity and inventory consumption rates.

### Evaluation metrics
- R² (coefficient of determination)
- RMSE (root mean squared error)
- MAE (mean absolute error)
- Business metric: revenue lift vs baseline.

---

## Pricing Strategy
### Rule-based logic
- Start with cost + target margin.
- Adjust for competitor price range and 20% max/min delta.
- Add seasonal and promotional business adjustments.

### ML-based pricing approach
- Predict demand at candidate prices (0.7x to 1.5x current price).
- Calculate revenue for each candidate: `price_i * predicted_demand_i`.
- Choose price maximizing expected revenue.
- Enforce constraints: margin floor, max delta ±20%, stock levels.

---

## Results
### Revenue comparison (Static vs Rule-based vs ML-based)
| Strategy | Backtest Revenue Lift | Notes |
|----------|-----------------------|-------|
| Static | 0.0% | baseline in use today |
| Rule-based | +5.0% | deterministic margin rules |
| ML-based | +9.2% avg | ensemble recommendation |

### Key insights
- ML-driven pricing wins 87% of the time in backtest.
- Electronics & toys show largest uplift (11–15%).
- Safety cap prevents adverse loss events (worst case -2%).

---

## Application / Demo
### Screenshots of Streamlit app
- `code running.png` (main UI)
- `Figure_1.png` and `Figure_2.png` (visuals from output charts)

### Explanation of inputs and outputs
- Inputs: product, current price, inventory, competitor price, season, weather, promotion status.
- Outputs: recommended price, revenue change, demand change, KPI charts, comparison table.

---

## Conclusion
### Final outcomes
- Implemented and deployed pricing optimization system.
- Real-world potential revenue lift ~9–10%.
- Fully documented handoff package for evaluation.

### Learnings
- Feature engineering is key for demand accuracy.
- Ensemble reduces variance and increases reliability.
- Streamlit provides rapid MVP deployment with interactive business controls.

---

## Future Improvements
### Possible enhancements
- Add online retraining with real-time sales streaming.
- Add competitor API scraping and price monitoring.
- Add user authentication, RBAC, and audit logging.
- Add multi-objective optimization (revenue vs margin vs inventory velocity).
- Add automatic training & tuning pipeline (CI/CD).

---

## How to Run the Project
### Step-by-step instructions
1. `cd C:\Users\Shubm\OneDrive\Desktop\shubham\AI_Price_Optima`
2. `.venv\Scripts\Activate.ps1`
3. `pip install -r requirements.txt`
4. `streamlit run app.py`
5. Open `http://localhost:8501` (or `8502` if 8501 in use)

### Troubleshooting
- `streamlit run app.py --server.port 8502`
- `pip install scikit-learn==1.5.2 joblib==1.4.2` for _RemainderColsList problem
- Validate model files:
  - `ls models/xgb_units_sold_model.pkl`
  - `ls models/lgbm_units_sold_model.pkl`

---

## Additional References
- `DEPLOYMENT_GUIDE.md` deploying instructions
- `QUICK_REFERENCE.md` daily usage
- `FINAL_EVALUATION_REPORT.md` business analysis
- `ROLLOUT_PLAN.md` implementation roadmap
