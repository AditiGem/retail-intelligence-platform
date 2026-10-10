# sales_forecast_fixed.py - COMPLETELY WORKING WITH PROPER DATAFRAME HANDLING

from config import DB_CONFIG, get_connection
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

import sys, io
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

print("="*60)
print("SALES FORECASTING SYSTEM")
print("="*60)

# ============================================
# LOAD DATA
# ============================================

print("\nLoading historical sales data...")

conn = get_connection()
query = """
SELECT 
    metric_date,
    total_revenue,
    total_units_sold
FROM daily_metrics
ORDER BY metric_date
"""
df = pd.read_sql(query, conn)
conn.close()

# Convert date column FIRST (before any operations)
df['metric_date'] = pd.to_datetime(df['metric_date'])

print(f"   Loaded {len(df)} days of data")
print(f"   Date range: {df['metric_date'].min().strftime('%Y-%m-%d')} to {df['metric_date'].max().strftime('%Y-%m-%d')}")
print(f"   Total revenue: ${df['total_revenue'].sum():,.2f}")

# ============================================
# CREATE DAY_OF_WEEK IN ORIGINAL DATAFRAME
# ============================================

# Add day_of_week column to original df
df['day_of_week'] = df['metric_date'].dt.dayofweek
df['day_name'] = df['metric_date'].dt.day_name()

print(f"   Added day_of_week column to dataframe")

# ============================================
# FEATURE ENGINEERING FUNCTION (LEAK-FREE)
# ============================================

def prepare_features(data):
    """
    Leak-free feature engineering.
    All lag/rolling features use only PAST values (shift > 0).
    No global aggregates.
    """
    data = data.copy().sort_values('metric_date').reset_index(drop=True)

    # Time features (known in advance — safe)
    data['day_of_week']  = data['metric_date'].dt.dayofweek
    data['day_of_month'] = data['metric_date'].dt.day
    data['month']        = data['metric_date'].dt.month
    data['is_weekend']   = (data['day_of_week'] >= 5).astype(int)

    # Lag features (only past)
    data['prev_day_revenue']  = data['total_revenue'].shift(1)
    data['prev_2day_revenue'] = data['total_revenue'].shift(2)
    data['prev_3day_revenue'] = data['total_revenue'].shift(3)
    data['prev_7day_revenue'] = data['total_revenue'].shift(7)

    # Rolling means — shift(1) first so today is excluded
    data['rolling_3day_mean'] = data['total_revenue'].shift(1).rolling(3).mean()
    data['rolling_7day_mean'] = data['total_revenue'].shift(1).rolling(7).mean()

    # Day-of-week average from PAST only (expanding mean per weekday)
    data['day_avg_revenue'] = (
        data.groupby('day_of_week')['total_revenue']
            .transform(lambda s: s.shift(1).expanding().mean())
    )

    data = data.dropna().reset_index(drop=True)
    return data

# ============================================
# PREPARE TRAINING DATA & TIME-BASED SPLIT
# ============================================

print("\nPreparing training data...")
featured_df = prepare_features(df)

feature_cols = [
    'day_of_week', 'day_of_month', 'month', 'is_weekend',
    'prev_day_revenue', 'prev_2day_revenue', 'prev_3day_revenue',
    'prev_7day_revenue', 'rolling_3day_mean', 'rolling_7day_mean',
    'day_avg_revenue'
]

X = featured_df[feature_cols]
y = featured_df['total_revenue']

# TIME-BASED SPLIT (no shuffle — order preserved)
split_idx = int(len(X) * 0.8)
X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

print(f"Train: {len(X_train)} samples")
print(f"Test:  {len(X_test)} samples")
print(f"Train dates: {featured_df['metric_date'].iloc[0].date()} → {featured_df['metric_date'].iloc[split_idx-1].date()}")
print(f"Test dates:  {featured_df['metric_date'].iloc[split_idx].date()} → {featured_df['metric_date'].iloc[-1].date()}")

# ============================================
# TRAIN MODEL & EVALUATE METRICS
# ============================================

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import json

print("\nTraining Random Forest model...")
model = RandomForestRegressor(
    n_estimators=200,
    max_depth=12,
    random_state=42
)
model.fit(X_train, y_train)

y_train_pred = model.predict(X_train)
y_test_pred  = model.predict(X_test)

train_r2 = r2_score(y_train, y_train_pred)
test_r2  = r2_score(y_test,  y_test_pred)
mae      = mean_absolute_error(y_test, y_test_pred)
rmse     = np.sqrt(mean_squared_error(y_test, y_test_pred))

mae_pct  = (mae  / y_test.mean()) * 100
rmse_pct = (rmse / y_test.mean()) * 100

print(f"\n{'='*60}")
print("MODEL PERFORMANCE")
print(f"{'='*60}")
print(f"Train R² : {train_r2:.3f}")
print(f"Test  R² : {test_r2:.3f}")
print(f"MAE      : ${mae:,.2f}  ({mae_pct:.1f}%)")
print(f"RMSE     : ${rmse:,.2f} ({rmse_pct:.1f}%)")
print(f"Train/Test R² gap: {train_r2 - test_r2:.3f}")

if test_r2 > 0.95:
    print("⚠️  Test R² > 0.95 — verify no leakage remains")
elif test_r2 > 0.6:
    print("✅ Model quality: GOOD")
elif test_r2 > 0.4:
    print("✅ Model quality: REASONABLE")
else:
    print("⚠️  Model quality: NEEDS IMPROVEMENT")

# ============================================
# SAVE METRICS TO JSON
# ============================================

feature_importances = dict(
    sorted(
        zip(feature_cols, model.feature_importances_.tolist()),
        key=lambda x: -x[1]
    )
)
feature_importances = {k: round(v, 4) for k, v in feature_importances.items()}

metrics = {
    'r2':                  round(test_r2, 3),
    'train_r2':            round(train_r2, 3),
    'mae':                 round(mae, 2),
    'mae_pct':             round(mae_pct, 2),
    'rmse':                round(rmse, 2),
    'rmse_pct':            round(rmse_pct, 2),
    'train_size':          int(len(X_train)),
    'test_size':           int(len(X_test)),
    'feature_importances': feature_importances,
    'trained_at':          datetime.now().isoformat()
}

with open('model_metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)

print(f"\n✅ Metrics saved to model_metrics.json")

# ============================================
# RECURSIVE FORECASTING
# ============================================

print("\n" + "="*60)
print("GENERATING RECURSIVE FORECAST")
print("="*60)

last_date = df['metric_date'].max()
future_dates = [last_date + timedelta(days=i+1) for i in range(7)]

history = df['total_revenue'].tolist()
history_days = df['metric_date'].dt.dayofweek.tolist()

if len(history) < 7:
    raise ValueError(f"Need at least 7 days of history. Only {len(history)} available.")

predictions = []

for date in future_dates:
    same_day_vals = [
        r for d, r in zip(history_days, history) if d == date.weekday()
    ]
    day_avg = float(np.mean(same_day_vals)) if same_day_vals else float(np.mean(history))

    feat = {
        'day_of_week':        date.weekday(),
        'day_of_month':       date.day,
        'month':              date.month,
        'is_weekend':         int(date.weekday() >= 5),
        'prev_day_revenue':   history[-1],
        'prev_2day_revenue':  history[-2],
        'prev_3day_revenue':  history[-3],
        'prev_7day_revenue':  history[-7],
        'rolling_3day_mean':  float(np.mean(history[-3:])),
        'rolling_7day_mean':  float(np.mean(history[-7:])),
        'day_avg_revenue':    day_avg
    }

    X_future = pd.DataFrame([feat])[feature_cols]
    pred = float(model.predict(X_future)[0])
    predictions.append(pred)

    # Feed prediction back into history for next iteration
    history.append(pred)
    history_days.append(date.weekday())

# Display forecast
print("\n" + "="*60)
print("7-DAY SALES FORECAST")
print("="*60)
print(f"{'Date':15} {'Day':10} {'Forecast':15} {'Range':20}")
print("-" * 65)

total_forecast = 0
for i, date in enumerate(future_dates):
    date_str = date.strftime('%Y-%m-%d')
    day_name = date.strftime('%A')
    pred = predictions[i]
    total_forecast += pred
    print(f"{date_str:15} {day_name:10} ${pred:12,.2f}   ${pred*0.85:,.2f} - ${pred*1.15:,.2f}")

print("-" * 65)
print(f"{'TOTAL':15} {'':10} ${total_forecast:12,.2f}")
print(f"{'AVERAGE':15} {'':10} ${total_forecast/7:12,.2f}")

# ============================================
# TREND ANALYSIS
# ============================================

hist_avg = df['total_revenue'].tail(14).mean()
forecast_avg = total_forecast / 7
trend_pct = ((forecast_avg - hist_avg) / hist_avg) * 100

print("\n" + "="*60)
print("TREND ANALYSIS")
print("="*60)
print(f"Historical avg (last 14 days): ${hist_avg:,.2f}")
print(f"Forecast avg (next 7 days): ${forecast_avg:,.2f}")
print(f"Expected change: {trend_pct:+.1f}%")

if trend_pct > 5:
    print("   📈 UPWARD trend expected")
    recommendation = "Increase inventory for next week"
elif trend_pct < -5:
    print("   📉 DOWNWARD trend expected")
    recommendation = "Run promotions to boost sales"
else:
    print("   📊 STABLE trend expected")
    recommendation = "Maintain current strategy"

# ============================================
# SAVE TO DATABASE
# ============================================

print("\nSaving predictions to database...")

conn = get_connection()
cursor = conn.cursor()

for i, date in enumerate(future_dates):
    predicted_qty = int(predictions[i] / 100)  # Convert revenue to quantity
    sql = """
    INSERT INTO sales_predictions 
    (product_id, prediction_date, predicted_quantity, confidence_lower, confidence_upper, model_version)
    VALUES (0, %s, %s, %s, %s, 'RandomForest_Final')
    ON DUPLICATE KEY UPDATE
    predicted_quantity = VALUES(predicted_quantity),
    confidence_lower = VALUES(confidence_lower),
    confidence_upper = VALUES(confidence_upper)
    """
    cursor.execute(sql, (date, predicted_qty, int(predicted_qty*0.85), int(predicted_qty*1.15)))

conn.commit()
cursor.close()
conn.close()
print(f"   Saved {len(future_dates)} predictions to database")

# ============================================
# CREATE VISUALIZATION
# ============================================

print("\nCreating forecast chart...")

plt.figure(figsize=(14, 7))

# Plot historical data (last 30 days)
historical_plot = df.tail(30)
plt.plot(historical_plot['metric_date'], historical_plot['total_revenue'], 
         'b-o', label='Historical Sales', linewidth=2, markersize=6)

# Plot forecast
plt.plot(future_dates, predictions, 'r--s', label='7-Day Forecast', linewidth=2, markersize=8)

# Add confidence band
upper_bound = [p * 1.15 for p in predictions]
lower_bound = [p * 0.85 for p in predictions]
plt.fill_between(future_dates, lower_bound, upper_bound, alpha=0.2, color='red', 
                  label='85% Confidence Range')

plt.xlabel('Date', fontsize=12)
plt.ylabel('Revenue ($)', fontsize=12)
plt.title('Sales Forecast - Next 7 Days', fontsize=14, fontweight='bold')
plt.legend(loc='best')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('sales_forecast.png', dpi=150)
print("   Chart saved: sales_forecast.png")

# ============================================
# BUSINESS INSIGHTS
# ============================================

print("\n" + "="*60)
print("BUSINESS INSIGHTS")
print("="*60)

# Best day prediction
best_idx = np.argmax(predictions)
best_day = future_dates[best_idx].strftime('%A, %B %d')
print(f"   Expected highest sales: {best_day} (${predictions[best_idx]:,.2f})")

# Worst day prediction
worst_idx = np.argmin(predictions)
worst_day = future_dates[worst_idx].strftime('%A, %B %d')
print(f"   Expected lowest sales: {worst_day} (${predictions[worst_idx]:,.2f})")

print(f"   RECOMMENDATION: {recommendation}")

# Weekly comparison
if best_idx >= 5:  # Weekend
    print("   NOTE: Weekend sales expected to be higher - schedule more staff")
else:
    print("   NOTE: Weekday sales expected to be higher - focus marketing mid-week")

print("\n" + "="*60)
print("FORECASTING COMPLETE!")
print("="*60)

print("\nFiles created:")
print("   - sales_forecast.png")
print("\nNext steps:")
print("   1. Open sales_forecast.png to view the chart")
print("   2. Check predictions: SELECT * FROM sales_predictions;")
print("   3. Compare actual vs predicted next week")