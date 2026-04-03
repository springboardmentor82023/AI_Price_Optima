
PROJECT WORK BY :MAHALAKSHMI AVNK

💰 AI: PriceOptima – Dynamic Pricing System

 1. Project Overview

AI: PriceOptima is an intelligent, data-driven dynamic pricing system designed to optimize product pricing in retail environments.

The system leverages:

* Historical sales data
* Inventory levels
* Market conditions

to dynamically adjust prices and maximize revenue while maintaining competitiveness.



 ❗ 2. Problem Statement

Traditional retail systems rely on **static pricing**, which does not adapt to changing market conditions such as demand fluctuations, stock availability, or competitor pricing.

This results in:

* Missed revenue opportunities
* Overstocking or stockouts
* Poor responsiveness to market trends

👉 **Solution:**
Develop an **AI-based dynamic pricing system** that adjusts prices using:

* Rule-based logic
* Machine learning models
* Real-time insights

---

🎯 3. Project Objectives

* Build a **data pipeline** for structured retail data processing
* Analyze demand and pricing behavior using EDA
* Develop a **rule-based pricing engine**
* Train **machine learning models** to predict demand
* Optimize pricing using ML predictions
* Deploy the system using an **interactive dashboard**
* Demonstrate **revenue improvement**

---

 📊 4. Dataset Overview

The project uses the **Retail Store Inventory Forecasting Dataset**.

 📌 Key Details

* Records: 73,100
* Features: 15
* Granularity: Daily (Store × Product level)

 📊 Important Features

* Product ID, Category
* Price, Discount, Competitor Price
* Units Sold (Demand)
* Inventory Level
* Date (Time-based analysis)
* Weather, Promotion, Seasonality

👉 The dataset satisfies all requirements for **dynamic pricing and demand forecasting**.

---

 🔄 5. Project Workflow

```text
Data Ingestion → Data Processing → EDA → 
Rule-Based Pricing → ML Models → 
Pricing Engine → Dashboard
```

---

⚙️ 6. Milestone-wise Implementation

---

🔹 Milestone 1: Data Preparation

 ✔ Work Done

* Selected a **Kaggle retail dataset**
* Verified mandatory features
* Defined pricing and demand objectives

✔ Outcome

* Dataset approved and ready for pipeline

---

🔹 Milestone 2: Data Ingestion Pipeline

⚙️ Implementation

* Developed `ingest.py` using Pandas
* Organized folder structure:

  
  data/
  ├── raw/
  ├── processed/
  └── daily_ingest/
  

 🔄 Pipeline Steps

* Loaded raw data
* Validated dataset
* Removed duplicates
* Handled missing values
* Saved cleaned data
* Created **date-wise ingestion folders**

 ✔ Result

* Built a **robust, repeatable ingestion pipeline**
* Simulated real-world daily data processing

---

🔹 Milestone 3: Exploratory Data Analysis (EDA)

 📊 Analysis Performed

* Demand trends over time
* Price vs demand relationship
* Revenue analysis
* Correlation heatmap
* Product-level performance

🔍 Key Insights

* Demand decreases when price increases
* Sales vary across time (seasonality present)
* Few products generate most revenue
* Inventory affects sales performance
* Revenue depends on both price and demand

 ✔ Result

* Identified **critical pricing patterns**
* Provided foundation for pricing strategies

---

🔹 Milestone 4: Baseline Pricing Engine

 🧠 Pricing Rules

**Time-Based:**

* Weekend → Price ↑ 10%

**Inventory-Based:**

* Inventory < 20 → Price ↑ 15%
* Inventory > 100 → Price ↓ 10%

---

💰 Revenue Comparison

* Original Revenue: ~41.05
* New Revenue: ~44.68

📈 **Revenue Lift: 8.85%**

---
 ✔ Result

* Rule-based pricing improved revenue
* Established baseline for ML comparison

---

🔹 Milestone 5: Machine Learning Models

 🤖 Models Used

* XGBoost
* LightGBM

---

 ⚙️ Model Setup

* Target: Units Sold
* Features:

  * Price
  * Inventory
  * Time features
* Data split: 80/20

---

 📏 Performance

| Model    | MAE    | RMSE   | R²     |
| -------- | ------ | ------ | ------ |
| XGBoost  | 0.0348 | 0.0442 | 0.9980 |
| LightGBM | 0.0402 | 0.0505 | 0.9974 |

---

📈 Revenue Impact

* Static Revenue: 79.45
* ML Revenue: 92.35

 Revenue Lift: 16.23%

---

 ✔ Result

* ML significantly outperformed rule-based approach
* Enabled **data-driven pricing decisions**

---

🔹 Milestone 6: Deployment & Dashboard

🖥 Implementation

* Built using Streamlit

---

 🔧 Features

Inputs:

* Price
* Inventory
* Competitor Price
* Date

Outputs:

* Recommended Price
* Predicted Demand
* Expected Revenue

---

 📊 Visualizations

* Revenue comparison
* Demand trends
* Model performance

---

✔ Result

* Successfully deployed an **interactive pricing system**
* Enabled real-time decision-making

---

🏗 7. System Architecture


                ┌──────────────┐
                │ Raw Data     │
                └──────┬───────┘
                       ↓
                ┌──────────────┐
                │ Ingestion     │
                └──────┬───────┘
                       ↓
                ┌──────────────┐
                │ Processing    │
                └──────┬───────┘
                       ↓
                ┌──────────────┐
                │ EDA & Insights│
                └──────┬───────┘
                       ↓
        ┌──────────────┴──────────────┐
        ↓                             ↓
┌──────────────┐             ┌──────────────┐
│ Rule-Based    │             │ ML Models     │
│ Pricing       │             │ (XGBoost)     │
└──────┬───────┘             └──────┬───────┘
       ↓                            ↓
       └──────────┬─────────────────┘
                  ↓
          ┌──────────────┐
          │ Pricing Engine│
          └──────┬───────┘
                 ↓
          ┌──────────────┐
          │ Dashboard     │
          └──────────────┘


---

 🔄 8. Pricing Strategy Flow

```text
Input Data → Demand Prediction → Price Adjustment → Revenue Calculation → Output Recommendation
```

---

📈 9. Key Results

* Rule-Based Pricing → **+8.85% revenue**
* ML-Based Pricing → **+16.23% revenue**
* XGBoost achieved highest accuracy
* Dynamic pricing outperformed static pricing

---

✅ 10. Conclusion

This project successfully demonstrates the effectiveness of **AI-driven dynamic pricing systems** in real-world retail scenarios.
 🎯 Achievements

* Built end-to-end ML pipeline
* Implemented rule-based and ML pricing
* Achieved measurable revenue improvement
* Developed a deployable application

---

📚 11. Learnings

* Importance of EDA in business problems
* Demand-price relationship (elasticity)
* Real-world ML deployment
* Data pipeline design

---

🔮 12. Future Scope

* Real-time API integration (FastAPI)
* Reinforcement learning for pricing
* Customer segmentation
* Competitor data scraping
* Scalable cloud deployment




