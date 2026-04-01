🧠AI Dynamic Pricing System — PriceOptima

📌Project Overview
The PriceOptima – Dynamic Pricing System is a machine learning-based application that recommends optimal product prices to maximize revenue using demand prediction.

Traditional pricing methods are static and fail to adapt to market conditions. This system uses XGBoost-based demand prediction + price optimization logic to dynamically adjust prices and improve business performance.

The solution is deployed using Streamlit, providing an interactive dashboard for users.

🎯Objective
he main objectives of this project are:

Predict product demand using machine learning
Recommend optimal pricing dynamically
Maximize revenue using price optimization
Compare static pricing vs ML-based pricing
Provide an interactive dashboard for business users

❗ Problem Statement

Businesses often use fixed pricing strategies that:

Do not adapt to demand changes
Ignore competitor pricing
Fail to maximize revenue

This project solves the problem by:

Predicting demand using ML models
Testing multiple price points
Selecting the price that maximizes revenue
Providing real-time recommendations

📊 Dataset Description
📌 Dataset Used:

Dynamic Pricing Dataset (Processed)

📌 Features Used:
Price
Base Price
Competitor Price
Discount
Inventory
Date Features (Year, Month, Day, Hour)
Weekend Flag
Holiday Flag
🎯 Target Variable:
Sales Quantity (Demand)


🔄 Project Workflow

1️⃣ Data Ingestion
Loaded dataset using Pandas
Checked missing values
Verified data consistency

2️⃣ Data Processing
Removed null values
Feature engineering:
price_diff
price_ratio
discount_effect
Train-test split

3️⃣ Exploratory Data Analysis (EDA)

Performed:

Price vs Demand analysis
Demand distribution
Seasonal trends
Correlation analysis

4️⃣ Baseline Pricing

Static pricing formula:

Revenue
=
Price
×
Demand
Revenue=Price×Demand

Used as baseline comparison.

5️⃣ Machine Learning Model
Models Used:
XGBoost (Final Selected Model)
LightGBM (Experimental)
Evaluation Metrics:
MAE
RMSE
R² Score
Result:
R² ≈ 0.96 (Very strong model)

🤖 Model Details
🔹 XGBoost
High accuracy
Handles non-linear relationships
Best performing model

💰 Pricing Strategy

🔹 ML-Based Pricing (Final Approach)

Steps:

Generate multiple price options (±10%)
Predict demand for each price
Calculate revenue
Apply constraints:
Competitor pricing limit
Price change penalty
Demand-drop penalty (NEW IMPROVEMENT)
Select price with highest revenue


📈 Results
Revenue Improvement
Average improvement: ~9% – 10%
Consistent across all test cases

Sample Results
Scenario	      Original Price	Recommended     	Improvement
Balanced	            120          	132            	9.24%
High Competitor	        100	            110	            ~10%
Low Price	            80	            88	             9.7%


📊 Key Insights
Demand is relatively stable in dataset
Small price increases improve revenue
Overpricing is avoided due to penalty logic
ML pricing outperforms static pricing
System provides stable and consistent outputs

🖥️ Streamlit Application

Features:
User input:
Price
Competitor Price
Discount
Inventory
Outputs:
Recommended Price
Expected Demand
Expected Revenue
Revenue Improvement

Dashboard Includes:
Key Metrics
Price Comparison
Revenue Comparison
Interactive UI

Screenshots

<img width="1919" height="1032" alt="image" src="https://github.com/user-attachments/assets/96ff0916-4a61-4baf-aba3-5b05df8f2b69" />
<img width="1917" height="1025" alt="image" src="https://github.com/user-attachments/assets/1989ba97-b46b-4f43-81d6-2387ffe14692" />
<img width="1918" height="1015" alt="image" src="https://github.com/user-attachments/assets/00897dce-4252-4277-a142-509778058879" />
<img width="1917" height="973" alt="image" src="https://github.com/user-attachments/assets/f017cf16-9123-4f32-ab5e-156412a598a3" />

🧪 Testing

The system was tested across multiple scenarios:

High price
Low price
High competitor
Low competitor
Edge cases
Result:
Stable outputs
Logical pricing
Consistent revenue improvement

📌 How to Run the Project
Step 1 — Clone Repository
https://github.com/springboardmentor82023/AI_Price_Optima/tree/karthivani?tab=readme-ov-file

Step 2 — Navigate to Project Directory
cd AI_PRICE_OPTIMA

Step 3 — Install Dependencies
📦 Deployment
Run Locally:pip install -r requirements.txt

Step 4 — Run Streamlit Application
streamlit run app.py



 

