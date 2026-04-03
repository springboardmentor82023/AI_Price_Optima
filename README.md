# 🚀 AI-Based Dynamic Pricing Optimization System

## 📌 Project Overview
This project presents an **AI-driven Dynamic Pricing System** that adjusts product prices based on multiple influencing factors such as demand, seasonality, inventory, and customer behavior.

The system leverages **machine learning models (XGBoost & LightGBM)** to predict optimal pricing strategies that maximize revenue while maintaining competitiveness and customer trust.

---

## 🎯 Objective
To design and implement a **machine learning–based pricing engine** that:

- Dynamically adjusts product prices
- Maximizes revenue and profitability
- Maintains competitive pricing
- Adapts to real-time and historical trends
- Provides actionable insights to businesses

---

## ❗ Problem Statement
Traditional static pricing fails to adapt to changing market conditions such as:

- Demand fluctuations
- Seasonal trends
- Inventory changes
- Customer behavior

This project solves the problem by building a **smart pricing engine** that continuously learns and recommends optimal prices.

---

## 📊 Dataset Description

- **Source**: Kaggle  
  https://www.kaggle.com/datasets/tanishkagoyal1/retail-sales-inventory-dataset

- **Description**:  
  A realistic retail dataset representing sales and inventory behavior across different products.

  It includes:

  - Product-level sales data  
  - Pricing information  
  - Inventory levels and stock availability  
  - Time-based sales records  
  - Demand (units sold) patterns  

- **Duration**:  
  Multiple time-period records enabling trend analysis and demand forecasting

---

## 🧾 Features Used

### 🔹 Raw Features
- `order_id`
- `order_date`
- `product_id`
- `product_category`
- `price`
- `discount_percent`
- `quantity_sold` (Target Variable)
- `customer_region`
- `payment_method`
- `rating`
- `review_count`
- `discounted_price`
- `total_revenue`

---

### 🔹 Engineered Features
- `inventory_level`
- `demand_level`
- `day`
- `month`
- `year`
- `day_of_week`
- `week_of_year`
- `is_weekend`

---

## ⚙️ Project Workflow

### 1️⃣ Data Ingestion
- Load dataset from Kaggle
- Integrate sales and pricing data

---

### 2️⃣ Data Processing
- Remove duplicate rows
- Handle missing values
- Fix data types
- Perform validation checks
- Save cleaned dataset

---

### 3️⃣ Feature Engineering
- Date feature extraction
- Label encoding for categorical variables
- Demand and inventory transformation
- Seasonal indicators (weekend, week number)

---

### 4️⃣ Exploratory Data Analysis (EDA)

Key analyses performed:

- 📉 Price vs Quantity Sold (Demand Curve)
- 💸 Discount % vs Quantity Sold
- 📊 Revenue by Product Category
- 📅 Monthly Revenue Trends
- ⭐ Rating vs Quantity Sold

---

### 5️⃣ Model Development

#### 🔹 Models Used:
- XGBoost Regressor
- LightGBM Regressor

#### 🔹 Input Features:




#### 🔹 Evaluation Metrics:
- MAE (Mean Absolute Error) - 69.2
- RMSE (Root Mean Squared Error) - 89.1
- R² Score - 0.32

---

### 6️⃣ Pricing Strategy

#### ✅ Rule-Based Pricing
- Minimum and maximum price thresholds
- Inventory-based adjustments
- Seasonal price changes

#### 🤖 ML-Based Pricing
- Predicts demand based on features
- Recommends optimal price
- Balances demand and profitability

---

### 7️⃣ Model Deployment

- Model saved using `pickle`
- Features and encoders stored for consistency
- Integrated into a **Streamlit application**

---

### 8️⃣ Application Layer (Streamlit)

#### 🎯 Features:
- User input for pricing factors
- Real-time demand prediction
- Price recommendation output
- Interactive UI for business users

---

## 📊 Results

### 💰 Revenue Comparison
| Strategy        | Performance |
|----------------|------------|
| Static Pricing | Baseline   |
| Rule-Based     | Moderate   |
| ML-Based       | Highest Revenue |

---

### 📌 Key Insights
- Discounts increase demand but reduce margins
- Weekend sales show higher demand
- Ratings strongly influence buying behavior
- Inventory scarcity increases optimal price

---

## 🖥️ Application Demo

### Inputs:
- Price
- Discount %
- Inventory Level
- Rating & Reviews
- Product Category
- Region
- Payment Method
- Date

### Outputs:
- Predicted Demand
- Recommended Optimal Price

---

## 🧠 Learnings
- Importance of **feature consistency between training and inference**
- Handling categorical encoding properly
- Real-world challenges in ML deployment
- Feature engineering significantly impacts performance

---

## 🔮 Future Improvements

- 🔄 Real-time pricing using streaming data
- 🧠 Reinforcement Learning for adaptive pricing
- 🌐 Integration with live e-commerce APIs
- 📊 Advanced dashboard using React.js
- 📦 Competitor price tracking
- 📈 A/B testing for pricing strategies

---

## 🛠️ Tech Stack

- **Language**: Python
- **Libraries**:
  - Pandas
  - NumPy
  - Scikit-learn
  - XGBoost
  - LightGBM
- **Frontend**: Streamlit
- **Model Storage**: Pickle
- **Deployment (Optional)**: Docker, FastAPI

---

## ▶️ How to Run the Project

### Step 1: Clone Repository
```bash
git clone https://github.com/your-username/ai-dynamic-pricing.git
cd ai-dynamic-pricing
```
### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Model Training (if needed)
```bash
python XGBoosterAndLightGBM.py
```
Step 4: Run Streamlit App
```bash
streamlit run app.py
```
