# Telco Customer Churn Prediction & Analytics System
## 📌 Project Overview
Customer churn occurs when subscribers or customers stop doing business with a company. For telecommunication providers, retaining existing customers is far less expensive than acquiring new ones. 

The objective of this project is to build an end-to-end data pipeline and machine learning system that analyzes historical customer data, uncovers why customers leave (**churn analytics**), and provides an interactive web application to predict whether a current customer is at risk of leaving in real-time.

---

## 🛠️ Technical Modules

### Module 1: Data Auditing & Exploration (SQL)
Before building models, the raw data must be understood and verified. Using structured SQL queries, we conducted a thorough analysis of the customer database.
* **Data Cleaning:** Handled missing values across key fields (such as resolving blank entries in `TotalCharges` for new customers with zero tenure).
* **Demographic Segmentation:** Grouped customers by age, partner status, and dependents to find trends.
* **Service Analysis:** Analyzed churn behaviors across different account characteristics, discovering how variables like contract type (*Month-to-month* vs. *One-year*) and internet service type (*Fiber optic* vs. *DSL*) correlate with customer departure.

### Module 2: Machine Learning Pipeline (Python & Scikit-Learn)
This module acts as the mathematical engine of the project, focusing on predictive accuracy and feature relationship extraction.
* **Exploratory Data Analysis (EDA):** Used Python libraries to visualize feature distributions and correlations.
* **Data Preprocessing:** Handled categorical variable encoding and numeric feature scaling to prepare data for model consumption.
* **Model Training:** Built and optimized a predictive model using a powerful ensemble algorithm (**Random Forest Classifier**). The model learns historical patterns to calculate the exact probability of a customer churning.
* **Model Serialization:** Exported the finalized model architecture (`churn_model.pkl`) and its operational feature map (`model_features.pkl`) into binary files using Joblib so they can be loaded instantly by external applications.

### Module 3: Business Intelligence Design (Power BI)
While machine learning handles future predictions, businesses need a high-level view of historical performance to make strategic decisions.
* **KPI Tracking:** Visualized total revenue losses, overall churn percentages, and high-risk customer pools.
* **Interactive Filtering:** Built dynamic charts allowing stakeholders to break down churn statistics by contract types, payment methods, and technical support status.
* **Actionable Insights:** Provided a clear visual map demonstrating that customers on short-term monthly contracts without tech support represent the highest financial risk.

### Module 4: Production User Interface (Streamlit)
To bridge the gap between complex machine learning code and everyday business users, we deployed an interactive web application.
* **User Input Forms:** Created clean, intuitive fields where an agent or manager can input a customer's specific profile metrics (e.g., monthly charges, contract type, internet type).
* **Real-Time Prediction Engine:** When submitted, the interface reads the data, passes it through the backend `.pkl` files, and prints an instantaneous risk percentage score.
* **Retention Strategy:** Empowers customer service teams to proactively identify at-risk clients and offer targeted retention incentives before the customer decides to close their account.
  
---

## 📂 Repository Structure
```text
├── sql_queries/          # SQL scripts for data cleaning & auditing
├── models/               # Saved serialised models (churn_model.pkl, model_features.pkl)
├── notebooks/            # Jupyter notebooks for EDA and Model Training
├── dashboard/            # Power BI dashboard files (.pbix)
├── app.py                # Streamlit web application
├── requirements.txt      # List of required Python libraries
└── README.md             # Project documentation
