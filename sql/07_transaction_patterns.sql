-- NOTE: The sales table does not contain a customer_id column.
-- This query segments by transaction signature
-- (composite of customer_city + payment_method), NOT by unique
-- customer. Do not interpret results as customer retention or RFM.

WITH customer_orders AS (
    SELECT CONCAT(customer_city, '-', payment_method) AS customer_id, COUNT(*) AS order_count, SUM(revenue) AS total_spent
    FROM sales
    GROUP BY customer_city, payment_method
)
SELECT
    CASE
        WHEN order_count = 1 THEN 'One-time'
        WHEN order_count BETWEEN 2 AND 5 THEN 'Repeat (2-5)'
        WHEN order_count BETWEEN 6 AND 10 THEN 'Loyal (6-10)'
        ELSE 'VIP (10+)'
    END AS customer_segment,
    COUNT(*)                    AS customers,
    SUM(order_count)            AS total_orders,
    ROUND(SUM(total_spent), 2)  AS total_revenue,
    ROUND(AVG(total_spent), 2)  AS avg_spend
FROM customer_orders
GROUP BY customer_segment
ORDER BY total_revenue DESC;
