# Retail Intelligence Platform

An end-to-end retail data intelligence platform combining automated analytics, 10 production-grade SQL analytical queries, recursive Random Forest demand forecasting, and an interactive Streamlit intelligence dashboard.

---

## 1. Project Overview

The **Retail Intelligence Platform** is designed for retail operations and decision-makers seeking transparent, data-backed insights across omnichannel transactional data. It unifies historical sales ingestion, multi-dimensional SQL KPI analysis, leak-free machine learning revenue forecasting, and an executive business intelligence interface.

---

## 2. Business Problem

Retail operations generate high-velocity transaction records across diverse product lines and regional markets. Without centralized data pipelines:
- Executives lack immediate visibility into revenue trends, order sizes, and regional growth.
- Category managers struggle to quantify product-level concentration and dead inventory.
- Demand planning relies on manual heuristics rather than reproducible forecasting algorithms.
- Legacy ad-hoc queries frequently double-count revenue or produce uncalibrated demand claims.

This platform automates data extraction, standardizes operational metrics, and provides defensible short-term demand projections.

---

## 3. Technology Stack

| Layer | Component | Purpose |
|---|---|---|
| **Language & Runtime** | Python 3.10 | Core pipeline execution and modeling |
| **Relational Storage** | MySQL 8.0+ | Normalized retail schema and indexed analytics |
| **Data Engineering** | Pandas 2.x, NumPy | Vectorized transformations, aggregation, and ETL |
| **SQL Analytics** | MySQL 8 (CTEs, Window Functions) | Ranking, running totals, MoM growth, and frequency analysis |
| **Machine Learning** | Scikit-learn (Random Forest) | 7-day recursive time-series revenue forecasting |
| **Interactive Dashboard**| Streamlit 1.x, Plotly | Executive KPI cards, interactive charts, and SQL showcase |
| **Configuration & Security** | python-dotenv, git-filter-repo | Safe environment isolation and credential hygiene |
| **Testing & Quality** | pytest | Automated configuration, database, and secret scan tests |

---

## 4. Architecture and Data Flow

```text
┌─────────────────────────┐
│ Raw Retail Transactions │ (sales, products, daily_metrics)
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│     MySQL 8 Storage     │ ◄── Database Configuration (`config.py`)
└──────┬───────────┬──────┘
       │           │
       │           ▼
       │     ┌───────────────────────────────────┐
       │     │  Sales Forecasting Engine         │
       │     │  (`sales_forecast.py`)            │
       │     │  • Lagged & rolling features      │
       │     │  • Chronological train/test split │
       │     │  • Recursive 7-day projection     │
       │     └───────────────┬───────────────────┘
       │                     │
       ▼                     ▼
┌──────────────────────┐   ┌─────────────────────┐
│ Python ETL Analytics │   │ Model Metrics JSON  │
│ (`pipeline.py`)      │   │ (`model_metrics.json│
└──────┬───────────────┘   └──────────┬──────────┘
       │                              │
       └──────────────┬───────────────┘
                      ▼
       ┌──────────────────────────────┐
       │ Streamlit Intelligence App   │ (`retail_platform.py`)
       │ • 6 Executive KPI Cards      │
       │ • Interactive Visuals        │
       │ • 10 SQL Analytics Queries   │
       │ • Data Quality Auditing      │
       └──────────────────────────────┘
```

---

## 5. Repository Structure

```text
retail analytics/
├── .env.example              # Template environment configuration (placeholders only)
├── .gitignore                # Excludes secrets, caches, virtual environments, backups
├── config.py                 # Centralized, sanitized MySQL connection loader
├── model_metrics.json        # Verified Random Forest evaluation metrics
├── pipeline.py               # Core data analysis and reporting pipeline
├── requirements.txt          # Python runtime dependencies
├── retail_platform.py        # Streamlit multi-page executive dashboard
├── sales_forecast.py         # 7-day recursive Random Forest forecasting script
├── sales_forecast.png        # Historical vs. 7-day forecast point prediction chart
├── screenshots/              # Directory for dashboard UI screenshots
│   └── README.md             # Guide for manual UI screenshot capture
├── sql/                      # 10 production-grade SQL analytical queries
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
└── tests/
    └── smoke_test.py         # 8 automated smoke and security verification tests
```

---

## 6. MySQL Setup

### Option A: Standard Database Setup
Log in to your local MySQL 8 instance and create the database:
```sql
CREATE DATABASE retail_intelligence;
```

### Option B: Dedicated Least-Privilege Application User (Recommended)
For production security, avoid running application queries as `root`. Create a restricted user:
```sql
-- Create dedicated application user
CREATE USER 'retail_app'@'localhost' IDENTIFIED BY 'StrongAppPassword_123!';

-- Grant required operational privileges on application database only
GRANT SELECT, INSERT, UPDATE, DELETE ON retail_intelligence.* TO 'retail_app'@'localhost';

-- Apply privilege changes
FLUSH PRIVILEGES;
```

---

## 7. Python Environment Setup

Create and activate a virtual environment using Python 3.10 on Windows PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

---

## 8. Dependency Installation

Install all required dependencies:
```powershell
pip install -r requirements.txt
```

---

## 9. Environment Variable Setup

Copy the `.env.example` template to `.env`:
```powershell
Copy-Item .env.example .env
```

Edit `.env` with your local database credentials:
```env
DB_HOST=localhost
DB_NAME=retail_intelligence
DB_USER=root
DB_PASSWORD=your_password_here
```
> [!NOTE]
> `.env` is strictly excluded from version control in `.gitignore`. Never commit actual passwords or credentials.

---

## 10. ETL & Analysis Execution

Run the Python analytics reporting pipeline:
```powershell
python pipeline.py
```
This generates:
- Executive summary metrics in console output
- Visualization charts saved locally (`top_products.png`, `daily_revenue.png`, `category_revenue.png`, `city_revenue.png`, `payment_methods.png`)

---

## 11. Forecasting Execution

Train the Random Forest regressor and generate the 7-day recursive forecast:
```powershell
python sales_forecast.py
```
This script:
1. Loads historical daily metrics from MySQL.
2. Constructs leak-free lag and rolling features.
3. Performs a chronological 80/20 train-test split (19 training days, 5 test days).
4. Evaluates genuine out-of-sample metrics and persists them to `model_metrics.json`.
5. Projects sales recursively for the next 7 days.
6. Stores clean forecast records into `sales_predictions` in MySQL.
7. Generates `sales_forecast.png`.

---

## 12. Dashboard Execution

Launch the interactive Streamlit intelligence dashboard:
```powershell
streamlit run retail_platform.py
```
The application will open in your browser at `http://localhost:8501`.

### Core Dashboard Views:
- **📊 Executive Dashboard**: 6 core KPIs, interactive date/category/city filters, revenue trends, top 10 products, and 7-day forecast table.
- **📂 Data Explorer**: Searchable, filterable transactional records with CSV/Excel/JSON export.
- **🔧 Advanced Filters**: Dynamic multi-condition rule builder.
- **📋 Data Quality**: Automated null checks, duplicate checks, and outlier detection.
- **🗄️ SQL Analytics**: Interactive query browser executing all 10 SQL scripts live.
- **ℹ️ About**: System architecture, data limitations, and methodology disclosures.

---

## 13. SQL Analytics Queries

The `sql/` directory contains 10 specialized analytical queries demonstrating advanced SQL (MySQL 8.0+):

1. **`01_monthly_revenue.sql`**: Monthly revenue, order volume, and AOV using date formatting and aggregation.
2. **`02_revenue_growth.sql`**: Month-over-month growth percentage utilizing the `LAG()` window function with zero-division protection.
3. **`03_top_products.sql`**: Top 10 products ranked by total revenue using `RANK() OVER (ORDER BY SUM(revenue) DESC)`.
4. **`04_category_performance.sql`**: Category revenue contribution, unit volume, and percentage share of total revenue.
5. **`05_city_performance.sql`**: Regional performance comparing order volume, total units, gross revenue, and revenue per unit.
6. **`06_aov_by_month.sql`**: Average order value trend and month-over-month change using window offsets.
7. **`07_transaction_patterns.sql`**: Transaction signature grouping (`customer_city` + `payment_method`) to segment purchasing frequency patterns without claiming false individual customer identity.
8. **`08_running_revenue.sql`**: Cumulative running revenue across chronological sale dates using unbounded preceding window frames.
9. **`09_mom_growth.sql`**: Categorized growth classification ('Strong Growth', 'Growth', 'Flat', 'Decline') using CTEs and CASE expressions.
10. **`10_product_ranking.sql`**: Intra-category product revenue ranking using `PARTITION BY` with both `RANK()` and `DENSE_RANK()`.

---

## 14. Forecast Evaluation & Methodology

The forecasting model intentionally uses strict time-based validation rather than randomized k-fold splits to prevent temporal leakage:

- **Algorithm**: `RandomForestRegressor(n_estimators=200, max_depth=12, random_state=42)`
- **Target Variable**: Daily `total_revenue` ($)
- **Features**: Day of week, day of month, month, weekend indicator, 1-day lag, 2-day lag, 3-day lag, 7-day lag, 3-day rolling mean, 7-day rolling mean, expanding weekday historical average.
- **Validation Scheme**: Chronological split (19 training days: 2026-03-31 to 2026-04-18; 5 test days: 2026-04-19 to 2026-04-23).
- **Out-of-Sample Metrics**:
  - **Train R²**: `0.929`
  - **Test R²**: `0.409`
  - **Test MAE**: `$11,718.11` (`17.11%` of mean test revenue)
  - **Test RMSE**: `$12,073.46` (`17.62%` of mean test revenue)

### Honest Disclosure on Prediction Intervals
Earlier prototype versions presented an arbitrary "85% confidence interval" calculated as `predicted_value ± 15%`. This has been completely removed. Standard Random Forest regressors do not produce formal parametric confidence intervals, and computing empirical conformal prediction intervals on a 5-observation test window is statistically invalid. Point predictions are displayed honestly alongside genuine validation metrics.

---

## 15. Known Data Limitations

1. **Compact Sample Size**: The dataset contains 31 daily aggregation points. While suitable for demonstrating recursive forecasting pipelines and time-based feature engineering, production forecasting typically requires ≥180–365 days of continuous history to model seasonality and promotional cycles.
2. **Absence of Dedicated Customer ID**: The `sales` table does not record a discrete individual customer identifier. Customer behavior is analyzed through composite transaction channel signatures (`customer_city` + `payment_method`), not unique user accounts.
3. **Derived Quantity Conversion**: The model forecasts gross daily revenue. Estimated unit counts are derived using verified empirical Average Selling Price (ASP = `$157.19/unit`), not arbitrary constant multipliers.

---

## 16. Security & Credential Hygiene

- **Working Tree**: No real passwords or production credentials exist in tracked source code, SQL queries, or documentation.
- **Git History Remediation**: Repository history was purged using `git-filter-repo` to eliminate historical commit artifacts containing credentials.
- **Environment Isolation**: Database credentials must be loaded via local `.env` (excluded by `.gitignore`).
- **Sanitized Diagnostics**: Application error handlers suppress database tracebacks to prevent credential leakage in logs or dashboard errors.

---

## 17. Automated Testing

Verify local reproducibility and security:
```powershell
python -m pytest tests/smoke_test.py -v
```

The 8 automated tests verify:
1. `test_config_imports`: DB configuration loads from environment.
2. `test_config_validation_missing_env`: Missing environment variables raise informative errors.
3. `test_connection`: Active connection succeeds against MySQL.
4. `test_metrics_file`: `model_metrics.json` exists with complete validation keys.
5. `test_sql_files`: All 10 SQL query files exist in `sql/`.
6. `test_sql_queries_execution`: All 10 SQL queries execute successfully against MySQL.
7. `test_no_obvious_secrets_in_tracked_files`: No hardcoded passwords in tracked files.
8. `test_no_compromised_password_in_history`: Complete Git history scan confirms zero exposed credentials.

---

## 18. UI Screenshots

Launch the dashboard locally (`streamlit run retail_platform.py`) and capture the following views to save in the `screenshots/` directory:
- `screenshots/01_executive_dashboard.png`: Executive KPI cards, daily revenue trend, and top 10 products.
- `screenshots/02_sales_forecasting.png`: 7-day recursive forecast table and trend visualization.
- `screenshots/03_sql_analytics.png`: Interactive SQL showcase executing analytical queries.
- `screenshots/04_data_explorer.png`: Data explorer table with filters and export actions.

---

## 19. License & Attribution

Developed for retail analytics portfolio evaluation, technical interview review, and reproducible data pipeline architecture demonstration.
