🚚 ShipmentSure – Smart Delivery Prediction System
📌 Project Overview
🎯 Objective

The objective of this project is to build an intelligent shipment prediction system that determines whether a delivery will be On-Time or Delayed using machine learning techniques.

❗ Problem Statement

In logistics, delayed deliveries lead to customer dissatisfaction and financial losses. Traditional systems fail to predict delays in advance.
This project solves that problem by using data-driven predictive analytics to forecast delivery outcomes.

📊 Dataset Description
📍 Source of Data

A structured dataset containing shipment and customer-related features was used for training the model.

📌 Features Used
Warehouse Block
Mode of Shipment
Customer Care Calls
Customer Rating
Cost of Product
Prior Purchases
Product Importance
Gender
Discount Offered
Weight in Grams
🎯 Target Variable
Delivery Status (On-Time / Delayed)
🔄 Project Workflow
1️⃣ Data Ingestion
Loaded dataset from CSV file
Structured input features
2️⃣ Data Processing
Handled missing values
Encoded categorical variables
Scaled numerical features
3️⃣ Exploratory Data Analysis (EDA)
Analyzed shipment trends
Studied delay patterns
Identified important features affecting delivery
4️⃣ Model Development
Built machine learning pipeline
Trained classification models
5️⃣ Model Training
Used training dataset
Evaluated using accuracy metrics
6️⃣ Deployment
Backend: Flask API
Frontend: React / Streamlit dashboard
Integrated model for real-time prediction
🤖 Model Details
📌 Algorithm Used

🔹 XGBoost

High performance boosting algorithm
Handles complex relationships
Provides better accuracy
📊 Evaluation Metrics
Accuracy: ~65%
Precision & Recall evaluated
Classification Report generated
📊 Results
🔍 Key Insights
High customer care calls → higher delay chances
Low ratings → increased delivery risk
Heavy weight shipments → more delays
Discounted products → higher uncertainty
🖥️ Application / Demo
⚙️ Inputs
Shipment details (warehouse, mode, weight, etc.)
Customer-related data
📤 Outputs
Delivery Status (On-Time / Delayed)
Confidence Score (%)
Risk Level
🎨 User Interface
💻 Features
Modern Dashboard UI (Neon / Glass / Premium styles)
Interactive Input Form
Real-time Predictions
Visual Confidence Indicator
🧠 System Architecture
🔹 Frontend
React (Neon Cyberpunk UI)
Handles user input and displays results
🔹 Backend
Flask API
Processes input data
Sends prediction response
🔹 Machine Learning Layer
XGBoost Model
Trained on shipment dataset
🔄 Project Flow
User enters shipment details
Frontend sends data to Flask API
Backend processes input
Model predicts delivery status
Result returned to frontend
UI displays prediction with confidence
▶️ How to Run the Project
🔧 Step 1: Install Dependencies
pip install numpy pandas scikit-learn xgboost flask streamlit
npm install
▶️ Step 2: Run Backend
cd backend
python app.py
▶️ Step 3: Run Frontend (React)
cd frontend
npm run dev
▶️ Step 4: Run Streamlit (Optional)
streamlit run streamlit_app.py
🌐 Open Browser
http://localhost:5173   (React)
http://localhost:8501   (Streamlit)
✅ Conclusion
📌 Final Outcomes
Built a complete delivery prediction system
Integrated ML model with frontend & backend
Developed interactive dashboard
📚 Learnings
Machine Learning Model Deployment
Flask API Development
React UI Design
Real-world logistics problem solving
🔮 Future Improvements
Improve model accuracy
Add real-time shipment tracking
Deploy on cloud (AWS / Azure)
Add advanced analytics dashboard
👩‍💻 Contributors
Your Name
⭐ Project Highlights

✔ Real-time prediction
✔ End-to-end ML pipeline
✔ Professional UI dashboard
✔ Industry-relevant problem
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/ac58fb7f-cdd6-4878-a1e6-fcc5d8a66531" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/70d125bc-5d9f-403c-bfe1-51783a2b7b55" />

