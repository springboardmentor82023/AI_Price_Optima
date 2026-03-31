AI PriceOptima – Dynamic Pricing System

1.Project Overview
Objective: 
The objective of this project is to design and implement an AI-powered dynamic pricing system that automatically adjusts product prices based on various influencing factors such as demand, inventory levels, competitor pricing, and seasonal trends.
The system aims to maximize revenue and improve decision-making by predicting demand and suggesting optimal pricing strategies in real time.

Problem Statement: 
In traditional retail systems, pricing is often static and manually controlled. This leads to several inefficiencies:
1.Loss of revenue during high demand periods.
2.Overstock issues when demand is low.
3.Lack of competitiveness against dynamic market pricing.
4.No data-driven decision-making.
To overcome these issues, this project introduces a machine learning-based pricing model that adapts dynamically to changing market conditions.

2. Dataset Description
   
Source of Data:
The dataset used in this project is synthetically generated using Python libraries such as NumPy and Pandas.
It simulates real-world retail/e-commerce scenarios with realistic relationships between features.

Features Used:
Price
Inventory Level
Discount
Competitor Price
Seasonality
Units Sold
Category
Region
Weather

Target Variable
Demand → Number of units expected to be sold


3. Project Workflow

1. Data Ingestion: 
   Generated dataset programmatically
   Stored in tabular format (DataFrame)
   Ensured variability in features for better model learning
2. Data Processing: 
   Converted categorical features into numerical format using encoding
   Normalized and cleaned data
   Removed unnecessary or redundant features
   Ensured consistency across all inputs
3. Exploratory Data Analysis (EDA): 
   EDA was performed to understand patterns and relationships:
   Price vs Demand → Inverse relationship
   Discount vs Demand → Positive relationship
   Inventory vs Demand → Availability impact
   Region & Weather → External influencing factors
   Visualization tools were used to better understand trends and distributions.
4. Baseline Pricing: 
   A static pricing strategy was implemented where:
   Price remains constant regardless of demand
   Used as a benchmark for comparison with advanced approaches
5. ML Model Development: 
   Problem Type: Regression (Demand Prediction)
   Model trained to learn relationship between input features and demand
   Steps: 
    Train-test split performed
    Model trained on historical/simulated data
    Predictions generated for unseen inputs
6. Deployment: 
   Built using Streamlit
   Interactive UI with sliders and dropdowns
   Real-time predictions based on user inputs
   Visual dashboards for insights


4. Model Details
   
Algorithms Considered: 
XGBoost
  Advanced boosting algorithm
  Handles complex feature interactions
  High predictive accuracy
  Robust to overfitting
LightGBM
  Faster than XGBoost
  Efficient with large datasets
  Lower memory consumption
Final Model Used: RandomForest
  Ensemble learning method
  Stable and easy to deploy
  Works well for non-linear relationships

Features Usedin Model:
Price
Inventory Level
Discount
Competitor Price
Seasonality
Units Sold
Category
Region
Weather

Evaluation Metrics: 
MAE - Measures Average Error
MSE - Penalizes large errors
R2 Score - Measures Model Acccuracy



5. Pricing Strategy

Rule-Based Pricing:
Simple logic applied:
High Demand → Increase Price
Low Demand → Decrease Price
Medium Demand → Keep Price Stable

ML-Based Pricing:
Demand predicted using ML model
Pricing adjusted dynamically
Revenue calculated using:
Revenue=Demand×Price
Helps optimize pricing decisions automatically



6. Results

Revenue Comparison:
| Strategy       | Description                 |
| -------------- | --------------------------- |
| Static Pricing | Fixed price, no adjustment  |
| Rule-Based     | Based on simple thresholds  |
| ML-Based       | Data-driven dynamic pricing |
ML-based pricing consistently produced higher revenue.

Key Insights:
Price has a strong negative impact on demand
Discounts significantly boost sales
Competitor pricing directly affects demand
Seasonal trends influence purchasing behavior
Inventory availability impacts sales performance




7. Application / Demo

Features of Dashboard
Clean and interactive UI
Real-time demand prediction
Price recommendation system
Revenue calculation
Visual charts for analysis

Inputs
Price
Inventory
Discount
Competitor Price
Season
Units Sold
Category
Region
Weather

Outputs
 Predicted Demand
 Suggested Price
 Revenue
 Pricing Strategy

<img width="1920" height="1080" alt="Screenshot (246)" src="https://github.com/user-attachments/assets/8aaeba11-f1e2-4867-ba0f-d27c416cb109" />


8. Conclusion:

Final Outcomes
Built a fully functional dynamic pricing system
Implemented machine learning for demand prediction
Developed an interactive web dashboard
Demonstrated real-world business application

Learnings
Importance of feature selection
Understanding demand-price relationships
Hands-on experience with ML models
Deployment using Streamlit
Real-world problem-solving using AI

Future Improvements
Use real-world datasets
Integrate deep learning models
Add customer segmentation
Improve UI with advanced visualizations
Deploy on cloud platforms
Real-time API integration


9. How to Run the Project

Step 1: Install Libraries
pip install pandas numpy scikit-learn streamlit

Step 2: Train Model
python train_model.py

Step 3: Run App
streamlit run app.py

Step 4: Open in Browser
http://localhost:8501

