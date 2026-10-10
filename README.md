# Retail Intelligence Platform

Retail Intelligence Platform — End-to-end retail analytics with SQL, ML forecasting, and interactive dashboards.

## 1. Business Problem

Retail businesses generate vast transactional and product data across physical and digital storefronts, but decision-makers often struggle to translate raw records into timely operational decisions. Without unified analytics, detecting revenue leakage, tracking product-level performance, and predicting short-term demand remains manual and error-prone. This platform establishes a reliable, data-backed foundation for retail intelligence and operational reporting.

## 2. Features

- Executive dashboard (6 KPIs)
- 10 SQL analytics queries
- 7-day Random Forest forecast
- Customer/transaction pattern analysis
- Advanced filters + global search
- Data quality monitoring
- CSV/Excel/JSON export

## 3. Tech Stack

| Layer | Tools |
|---|---|
| Ingestion | Python, Pandas |
| Storage | MySQL 8 |
| Analytics | SQL (CTEs, window functions) |
| ML | Scikit-learn (Random Forest) |
| UI | Streamlit, Plotly |
| Config | python-dotenv |

## 4. Architecture

```text
Data Source → ETL Pipeline → MySQL → Analytics Engine → Streamlit UI
                               ↑
                          Forecast ML
```

## 5. Repository Structure

```text
retail analytics/
├── .env.example
├── .gitignore
├── config.py
├── model_metrics.json
├── pipeline.py
├── requirements.txt
├── retail_platform.py
├── sales_forecast.py
└── sql/
    ├── 01_monthly_revenue.sql
    ├── 02_revenue_growth.sql
    ├── 03_top_products.sql
    ├── 04_category_performance.sql
    ├── 05_city_performance.sql
    ├── 06_aov_by_month.sql
    ├── 07_transaction_patterns.sql
    ├── 08_running_revenue.sql
    ├── 09_mom_growth.sql
    └── 10_product_ranking.sql
```

## 6. Setup

### 1. Create Python 3.10 Virtual Environment (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Configure Database
Create the MySQL database `retail_intelligence` in your local MySQL 8 instance:
```sql
CREATE DATABASE retail_intelligence;
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and fill in local database credentials:
```powershell
Copy-Item .env.example .env
```
Update `.env`:
```env
DB_HOST=localhost
DB_NAME=retail_intelligence
DB_USER=root
DB_PASSWORD=your_password_here
```

## 7. Run Commands

Run the ETL and reporting pipeline:
```powershell
python pipeline.py
```

Train and run the 7-day sales forecast model:
```powershell
python sales_forecast.py
```

Launch the Streamlit executive intelligence dashboard:
```powershell
streamlit run retail_platform.py
```

## 8. SQL Analytics

1. `01_monthly_revenue.sql`
2. `02_revenue_growth.sql`
3. `03_top_products.sql`
4. `04_category_performance.sql`
5. `05_city_performance.sql`
6. `06_aov_by_month.sql`
7. `07_transaction_patterns.sql`
8. `08_running_revenue.sql`
9. `09_mom_growth.sql`
10. `10_product_ranking.sql`

## 9. Forecast Model + Limitations

- **Algorithm**: `RandomForestRegressor` (200 trees, max depth 12).
- **Validation**: Strict chronological time-based split (no shuffle).
- **Validation Metrics**: Train R²: 0.93 | Test R²: 0.41 | MAE: 17.1% | RMSE: 17.6%.
- **Limitation**: Evaluated on a 5-sample test window. Reliable forecasting requires ≥6 months of continuous daily data. This model demonstrates recursive forecasting architecture rather than production demand readiness.

## 10. Known Limitations

- **Small Historical Dataset**: Approximately 31 daily aggregation points; short observation window limits seasonal and promotional pattern learning.
- **No Discrete Customer ID**: The `sales` schema does not store a dedicated customer primary key; transaction patterns represent composite city and payment method signatures.
- **Demo / Synthetic Data**: Data reflects demonstrative retail operations and should not be used for production commercial planning without domain calibration.

## 11. Screenshots

![Dashboard](screenshots/dashboard.png)

## 12. License & Attribution

Project created for retail analytics demonstration, portfolio review, and automated intelligence pipeline architecture.
