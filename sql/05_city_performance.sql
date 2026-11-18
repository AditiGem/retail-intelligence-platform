SELECT
    customer_city,
    COUNT(*)                                              AS total_orders,
    SUM(quantity_sold)                                    AS total_units,
    ROUND(SUM(revenue), 2)                                AS total_revenue,
    ROUND(AVG(revenue), 2)                                AS avg_order_value,
    ROUND(SUM(revenue) / NULLIF(SUM(quantity_sold), 0), 2) AS avg_revenue_per_unit
FROM sales
GROUP BY customer_city
ORDER BY total_revenue DESC;
