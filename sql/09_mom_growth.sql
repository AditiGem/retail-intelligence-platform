WITH monthly AS (
    SELECT DATE_FORMAT(sale_date, '%Y-%m') AS month,
           SUM(revenue) AS revenue
    FROM sales
    GROUP BY DATE_FORMAT(sale_date, '%Y-%m')
),
growth AS (
    SELECT
        month,
        revenue,
        LAG(revenue) OVER (ORDER BY month) AS prev_revenue
    FROM monthly
)
SELECT
    month,
    revenue,
    prev_revenue,
    ROUND((revenue - prev_revenue) / prev_revenue * 100, 2) AS mom_growth_pct,
    CASE
        WHEN revenue > prev_revenue * 1.10 THEN 'Strong Growth'
        WHEN revenue > prev_revenue        THEN 'Growth'
        WHEN revenue = prev_revenue        THEN 'Flat'
        ELSE 'Decline'
    END AS trend_label
FROM growth
ORDER BY month;
