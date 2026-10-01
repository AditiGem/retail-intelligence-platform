SELECT
    sale_date,
    ROUND(SUM(revenue), 2) AS daily_revenue,
    ROUND(SUM(SUM(revenue)) OVER (ORDER BY sale_date), 2) AS running_total
FROM sales
GROUP BY sale_date
ORDER BY sale_date;
