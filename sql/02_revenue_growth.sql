WITH monthly AS (
    SELECT DATE_FORMAT(sale_date, '%Y-%m') AS month,
           SUM(revenue) AS revenue
    FROM sales
    GROUP BY DATE_FORMAT(sale_date, '%Y-%m')
)
SELECT
    month,
    revenue,
    LAG(revenue) OVER (ORDER BY month) AS prev_month,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY month))
        / LAG(revenue) OVER (ORDER BY month) * 100, 2
    ) AS growth_pct
FROM monthly
ORDER BY month;
