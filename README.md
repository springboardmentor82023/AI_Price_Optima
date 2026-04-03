# 🚀 AI PriceOptima – Dynamic Pricing System

---

## 📌 Project Overview

### 🎯 Objective

The objective of this project is to develop an intelligent **dynamic pricing system** that recommends optimal product prices using machine learning to maximize revenue.

### ❗ Problem Statement

Traditional static pricing fails to adapt to market demand, inventory levels, and customer behavior. This leads to revenue loss and inefficient pricing decisions.
This project aims to solve this by using **data-driven pricing strategies**.

---

## 📊 Dataset Description

### 📍 Source of Data

A synthetic dataset of 50,000 samples was created to simulate real-world pricing scenarios, incorporating factors such as demand, inventory levels, and price variations.
### 📌 Features Used

* Current Price
* Inventory Level
* Demand Factor
* Predicted Demand (Target Variable)

---

## 🔄 Project Workflow

### 1️⃣ Data Ingestion

Data was generated/collected and stored in structured format.

### 2️⃣ Data Processing

* Cleaned dataset
* Removed inconsistencies
* Prepared input-output structure

### 3️⃣ Exploratory Data Analysis (EDA)

* Relationship between price and demand analyzed
* Demand variation studied with inventory
* Revenue patterns observed

### 4️⃣ Baseline Pricing

* Static pricing used as baseline
* Fixed price regardless of demand

### 5️⃣ ML Model Development

* Models used:

  * LightGBM
  * XGBoost
* Model trained to predict demand

### 6️⃣ Deployment

* Model deployed using **Streamlit dashboard**
* Interactive UI created for business users

---

## 🤖 Model Details

### 📌 Algorithms Used

#### 🔹 XGBoost

* Gradient boosting algorithm
* Handles non-linear relationships effectively
* High accuracy and performance

#### 🔹 LightGBM

* Faster and efficient boosting model
* Works well with large datasets
* Low memory usage

---

### 📊 Features Used

* Price
* Inventory
* Demand Factor

---

### 📈 Evaluation Metrics

* R² Score
* MAE (Mean Absolute Error)
* RMSE (Root Mean Square Error)

---

## 💡 Pricing Strategy

### 🔹 Rule-Based Pricing

* Fixed increase in price based on demand
* Example: Price + 10%

### 🔹 ML-Based Pricing

* Predict demand using ML model
* Adjust price dynamically
* Optimize revenue

---

## 📊 Results

### 💰 Revenue Comparison

| Strategy   | Revenue           |
| ---------- | ----------------- |
| Static     | Base              |
| Rule-Based | Moderate Increase |
| ML-Based   | Highest Revenue   |

---

### 🔍 Key Insights

* ML-based pricing gives better revenue
* Demand-driven pricing is more effective
* Inventory impacts pricing flexibility
  
---

### ⚙️ Inputs

* Product Selection
* Current Price
* Inventory Level
* Demand Factor

---

### 📤 Outputs

* Recommended Price
* Expected Demand
* Expected Revenue
* Revenue Improvement

---

## ✅ Conclusion

### 📌 Final Outcomes

* Built a complete dynamic pricing system
* Successfully integrated ML model
* Developed an interactive dashboard

---

### 📚 Learnings

* Machine learning deployment
* Streamlit UI development
* Business-oriented analytics

---

## 🔮 Future Improvements

* Use real-world datasets
* Add deep learning models
* Integrate real-time pricing
* Deploy on cloud

---

## ▶️ How to Run the Project

### 🔧 Step 1: Install Dependencies

```bash
pip install numpy pandas scikit-learn streamlit plotly
```

### ▶️ Step 2: Run Application

```bash
streamlit run app.py
```

### 🌐 Step 3: Open Browser

```
http://localhost:8501
```

---
