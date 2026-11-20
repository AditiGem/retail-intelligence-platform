# 📊 Retail Intelligence Platform

An end-to-end retail analytics and forecasting platform built using **Python, MySQL, SQL, Machine Learning, and Streamlit**. The platform transforms retail sales data into meaningful business insights through data processing, SQL analytics, interactive dashboards, and sales forecasting.

**GitHub Repository:** [Retail Intelligence Platform](https://github.com/AditiGem/retail-intelligence-platform)

---

## 📌 Project Overview

Retail businesses generate large amounts of sales data across products, categories, cities, and transactions. Analyzing this data effectively helps businesses understand sales performance, identify profitable products, monitor trends, and make informed decisions.

The Retail Intelligence Platform provides an integrated solution for analyzing retail data and generating actionable business insights.

The project combines a Python-based data processing workflow, MySQL database, analytical SQL queries, a machine learning forecasting model, and an interactive Streamlit dashboard.

## 🎯 Project Objectives

- Analyze overall retail sales performance.
- Track important business KPIs such as revenue, orders, average order value, and units sold.
- Identify top-performing products and categories.
- Analyze revenue distribution across different cities.
- Understand daily and monthly sales trends.
- Forecast future sales using machine learning.
- Present business insights through an interactive dashboard.

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Database | MySQL 8.0 |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Visualization | Plotly, Matplotlib |
| Dashboard | Streamlit |
| Database Connectivity | mysql-connector-python |
| Configuration | python-dotenv |
| Version Control | Git, GitHub |

## 🏗️ Project Architecture

The platform follows a data analytics workflow:

1. **Data Source:** Retail sales data is used as the input.
2. **ETL Pipeline:** Python processes, cleans, and prepares the data.
3. **Database Storage:** Processed data is stored and accessed through MySQL.
4. **SQL Analytics:** Analytical queries extract business insights.
5. **Machine Learning:** A Random Forest regression model forecasts future sales.
6. **Visualization:** Streamlit presents KPIs, charts, filters, and forecasting results.

```text
             Retail Sales Data
                    |
                    v
          Python ETL Pipeline
          (Pandas / NumPy)
                    |
                    v
              MySQL Database
                    |
          +---------+---------+
          |                   |
          v                   v
     SQL Analytics       Forecasting Model
     (10 Queries)        (Random Forest)
          |                   |
          +---------+---------+
                    |
                    v
          Streamlit Dashboard
                    |
                    v
          Business Insights
```

## ✨ Key Features

### 1. Executive Dashboard

An interactive dashboard that provides an overview of retail business performance.

**Key Performance Indicators:**
- Total Revenue
- Total Orders
- Average Order Value (AOV)
- Units Sold
- Sales Growth Percentage
- Forecast Revenue

### 2. Sales Analytics

- Daily revenue trend analysis.
- Revenue growth monitoring.
- Monthly revenue analysis.
- Category-wise sales performance.
- City-wise revenue comparison.

### 3. Product Analytics

- Top 10 products based on revenue.
- Product performance comparison.
- Category contribution analysis.
- Identification of high-performing products.

### 4. Geographic Analytics

- City-wise revenue analysis.
- Comparison of business performance across locations.
- Identification of top-performing cities.

### 5. SQL Analytics

The project includes 10 SQL analytical queries using aggregations, Common Table Expressions (CTEs), window functions, ranking, and other SQL techniques.

| No. | SQL Analysis |
|---|---|
| 01 | Monthly Revenue |
| 02 | Revenue Growth |
| 03 | Top Products |
| 04 | Category Performance |
| 05 | City Performance |
| 06 | Average Order Value by Month |
| 07 | Transaction Patterns |
| 08 | Running Revenue |
| 09 | Month-over-Month Growth |
| 10 | Product Ranking |

### 6. Sales Forecasting

A Random Forest Regression model is implemented to predict future sales.

**Forecasting methodology:**
- Lag-based feature engineering.
- Rolling statistical features.
- Time-based features such as day of the week and month.
- Chronological training and testing split.
- Recursive multi-step forecasting.
- Model evaluation using R², MAE, and RMSE.

**Reported model evaluation:**

| Metric | Result |
|---|---:|
| Training Samples | 19 daily observations |
| Testing Samples | 5 daily observations |
| Test R² Score | 0.41 |
| MAE | 66 units (17.1%) |
| RMSE | 68 units (17.6%) |

The model produces point forecasts without claiming unsupported statistical prediction intervals.

*Note: The evaluation uses a relatively small dataset. The reported performance should be interpreted accordingly.*

## 📈 Dashboard Screenshots

### Executive Dashboard

<!-- Add your actual screenshot here -->
![Executive Dashboard](screenshots/executive_dashboard.png)

### Product and Category Analysis

<!-- Add your actual screenshot here -->
![Product and Category Analysis](screenshots/product_analysis.png)

### Sales Trend Analysis

<!-- Add your actual screenshot here -->
![Sales Trend Analysis](screenshots/sales_trends.png)

### Sales Forecasting

<!-- Add your actual screenshot here -->
![Sales Forecasting](screenshots/sales_forecast.png)

## 📂 Project Structure

```text
retail-intelligence-platform/
│
├── config.py
├── pipeline.py
├── retail_platform.py
├── sales_forecast.py
├── model_metrics.json
│
├── sql/
│   ├── 01_monthly_revenue.sql
│   ├── 02_revenue_growth.sql
│   ├── 03_top_products.sql
│   ├── 04_category_performance.sql
│   ├── 05_city_performance.sql
│   ├── 06_aov_by_month.sql
│   ├── 07_transaction_patterns.sql
│   ├── 08_running_revenue.sql
│   ├── 09_mom_growth.sql
│   └── 10_product_ranking.sql
│
├── tests/
│
├── screenshots/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

*The local `.env`, virtual environment, and other private configuration files are intentionally excluded from version control.*

## ⚙️ Installation and Setup

### Prerequisites

Make sure the following are installed:

- Python 3.10
- MySQL 8.0 or later
- Git
- pip

### Step 1: Clone the repository

```bash
git clone https://github.com/AditiGem/retail-intelligence-platform.git
```

Navigate into the project directory:

```bash
cd retail-intelligence-platform
```

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure MySQL

Create the project database in MySQL:

```sql
CREATE DATABASE retail_intelligence;
```

Import or prepare the required retail dataset and tables according to the project's SQL queries and Python code.

### Step 5: Configure environment variables

Create a local `.env` file in the project root using `.env.example` as a reference.

Example:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=retail_intelligence
DB_USER=your_database_user
DB_PASSWORD=your_database_password
```

Replace the example values with your own MySQL credentials.

**Important:** Never upload your actual `.env` file or database passwords to GitHub.

### Step 6: Run the application

Start the Streamlit dashboard:

```bash
streamlit run retail_platform.py
```

Open the local URL displayed in your terminal, usually:

```text
http://localhost:8501
```

## 🧪 Testing

Run the project's smoke tests:

```bash
python -m pytest tests/smoke_test.py -v
```

Compile Python files to check for syntax errors:

```bash
python -m compileall -q .
```

## 📊 Business Value

The platform demonstrates how retail transaction data can be transformed into business insights.

It helps users:

- Monitor key business performance indicators.
- Identify high-revenue products and categories.
- Understand geographic sales distribution.
- Analyze historical revenue trends.
- Explore future sales estimates.
- Support data-driven business decisions.

## ⚠️ Limitations

- Forecasting performance is based on a limited historical dataset.
- The model's test evaluation uses only five daily observations.
- Forecasts are estimates and should not be treated as guaranteed future sales.
- Analytical results depend on the completeness and quality of the source data.
- Customer-level analysis is limited by the availability of reliable customer identifiers.

## 🚀 Future Improvements

- Train forecasting models on a larger historical dataset.
- Evaluate additional forecasting algorithms.
- Integrate automated data refresh workflows.
- Improve model performance through additional feature engineering.
- Add more advanced customer segmentation when reliable customer identifiers are available.
- Deploy the dashboard to a cloud platform.

## 👩‍💻 Author

**Aditi**

B.Tech Computer Science and Engineering

**Areas of Interest:** Data Analytics | Data Engineering | Machine Learning

**GitHub:** [AditiGem](https://github.com/AditiGem)

---

⭐ If you find this project useful, consider giving the repository a star!

