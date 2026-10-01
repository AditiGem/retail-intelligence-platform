SELECT
    customer_city,
    COUNT(*)                          AS orders,
    COUNT(DISTINCT sale_id)           AS unique_customers,
    ROUND(SUM(revenue), 2)            AS total_revenue,
    ROUND(AVG(revenue), 2)            AS aov,
    ROUND(SUM(revenue) / COUNT(DISTINCT sale_id), 2) AS revenue_per_customer
FROM sales
GROUP BY customer_city
ORDER BY total_revenue DESC;
