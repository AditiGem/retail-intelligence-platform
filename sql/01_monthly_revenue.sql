SELECT
    DATE_FORMAT(sale_date, '%Y-%m') AS month,
    ROUND(SUM(revenue), 2)          AS total_revenue,
    COUNT(*)                        AS orders,
    ROUND(AVG(revenue), 2)          AS aov
FROM sales
GROUP BY DATE_FORMAT(sale_date, '%Y-%m')
ORDER BY month;
