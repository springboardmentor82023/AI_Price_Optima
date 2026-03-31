# 💰 AI-Based Dynamic Pricing System

## 📌 Project Overview

### 🎯 Objective

The objective of this project is to build an **AI-powered dynamic pricing system** that adjusts product prices based on demand, inventory, and market conditions to maximize revenue.

### ❗ Problem Statement

Businesses often use **static pricing**, which does not adapt to changing demand or stock levels.
This project solves that by implementing:

* Rule-based pricing
* Machine learning-based pricing
* Real-time price recommendations

---

## 📊 Dataset Description

### 📥 Source

* Dataset sourced from **Kaggle**

### 📌 Features Used

* Product ID / Category
* Price
* Competitor Price
* Demand (Units Sold)
* Inventory Level
* Date (for time-based analysis)

---

## 🔄 Project Workflow

### 1️⃣ Data Ingestion

* Raw data stored in `data/raw/`
* Cleaned data stored in `data/processed/`
* Daily ingestion simulated in `data/daily_ingest/`

---

### 2️⃣ Data Processing

* Missing values handled
* Duplicates removed
* Data types corrected

---

### 3️⃣ Exploratory Data Analysis (EDA)

* Price vs Demand analysis
* Sales trends over time
* Revenue patterns
* Inventory vs Sales relationship

---

### 4️⃣ Baseline Pricing (Rule-Based)

Implemented simple business rules:

* Weekend → Increase price
* Low inventory → Increase price
* High inventory → Decrease price

---

### 5️⃣ ML Model Development

* Trained models:

  * XGBoost
  * LightGBM

* Target:

  * Predict **demand (quantity sold)**

---

### 6️⃣ Deployment

* Built an interactive **Streamlit dashboard**
* Users can:

  * Enter product details
  * Get price recommendations
  * View revenue insights

---

## 🤖 Model Details

### 📌 Models Used

#### 🔹 XGBoost

* Gradient boosting algorithm
* Handles structured data efficiently
* Provides high accuracy

#### 🔹 LightGBM

* Faster and optimized boosting model
* Works well with large datasets

---

### 📥 Features Used in Model

* Price
* Inventory Level
* Competitor Price
* Demand Index
* Time-based features

---

### 📏 Evaluation Metrics

* MAE (Mean Absolute Error)
* RMSE (Root Mean Squared Error)
* R² Score

---

## 💡 Pricing Strategy

### 🔹 Rule-Based Pricing

* Based on predefined business logic
* Easy to implement
* Less accurate

---

### 🔹 ML-Based Pricing

* Uses demand prediction
* Adjusts price dynamically
* Optimizes revenue

---

## 📈 Results

### 💰 Revenue Comparison

| Strategy           | Description                |
| ------------------ | -------------------------- |
| Static Pricing     | No change in price         |
| Rule-Based Pricing | Price adjusted using rules |
| ML-Based Pricing   | Price optimized using ML   |

---

### 🚀 Key Insights

* Demand decreases when price increases (price sensitivity)
* Weekend sales are higher
* Low inventory leads to higher pricing opportunities
* Few products generate majority of revenue
* ML-based pricing improves revenue compared to static pricing

---

## 🖥 Application / Demo

### 📊 Streamlit Dashboard Features

* User input panel
* Price recommendation
* Demand prediction
* Revenue comparison

### 📥 Inputs

* Price
* Inventory
* Competitor Price
* Demand Index
* Date

### 📤 Outputs

* Recommended Price
* Expected Demand
* Expected Revenue

---

## ✅ Conclusion

### 🎯 Final Outcomes

* Built a complete pricing pipeline
* Implemented rule-based and ML-based pricing
* Achieved improved revenue performance

### 📚 Learnings

* Importance of EDA in pricing
* Impact of demand and inventory on pricing
* Practical use of ML in business problems

---

## 🔮 Future Improvements

* Add real-time data integration
* Use advanced deep learning models
* Include customer segmentation
* Integrate competitor tracking APIs

---

## ⚙️ How to Run the Project

### 🔧 Step 1: Clone Repository

```bash
git clone <your-repo-link>
cd Dynamic_Pricing_App
```

### 🔧 Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### 🔧 Step 3: Run Application

```bash
streamlit run app.py
```

---

## 📄 License

This project is licensed under the MIT License.
