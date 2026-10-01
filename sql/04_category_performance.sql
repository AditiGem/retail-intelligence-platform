SELECT
    p.category,
    COUNT(DISTINCT p.product_id)     AS products,
    ROUND(SUM(s.revenue), 2)         AS total_revenue,
    SUM(s.quantity_sold)             AS units_sold,
    ROUND(AVG(s.revenue), 2)         AS avg_order_value,
    ROUND(
        SUM(s.revenue) * 100.0 / (SELECT SUM(revenue) FROM sales), 2
    ) AS revenue_share_pct
FROM products p
JOIN sales s ON p.product_id = s.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;
