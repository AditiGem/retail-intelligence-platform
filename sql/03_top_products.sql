SELECT
    p.product_id,
    p.product_name,
    p.category,
    ROUND(SUM(s.revenue), 2)        AS total_revenue,
    SUM(s.quantity_sold)            AS units_sold,
    COUNT(s.sale_id)                AS orders,
    RANK() OVER (ORDER BY SUM(s.revenue) DESC) AS revenue_rank
FROM products p
JOIN sales s ON p.product_id = s.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_revenue DESC
LIMIT 10;
