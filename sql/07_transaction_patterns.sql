-- NOTE: The sales table does not contain a customer_id column.
-- This query segments by transaction signature pattern
-- (composite of customer_city + payment_method) to analyze channel frequency,
-- NOT unique individuals. Do not interpret results as customer retention or RFM.

WITH transaction_signatures AS (
    SELECT
        CONCAT(customer_city, ' / ', payment_method) AS signature,
        COUNT(*) AS transaction_count,
        SUM(revenue) AS total_revenue
    FROM sales
    GROUP BY customer_city, payment_method
)
SELECT
    CASE
        WHEN transaction_count = 1 THEN 'Single Transaction (1)'
        WHEN transaction_count BETWEEN 2 AND 5 THEN 'Low Volume (2-5)'
        WHEN transaction_count BETWEEN 6 AND 10 THEN 'Medium Volume (6-10)'
        ELSE 'High Volume (10+)'
    END AS volume_tier,
    COUNT(*)                     AS signature_count,
    SUM(transaction_count)       AS total_transactions,
    ROUND(SUM(total_revenue), 2) AS total_revenue,
    ROUND(AVG(total_revenue), 2) AS avg_revenue_per_signature
FROM transaction_signatures
GROUP BY volume_tier
ORDER BY total_revenue DESC;
