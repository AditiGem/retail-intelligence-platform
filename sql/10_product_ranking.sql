WITH product_revenue AS (
    SELECT
        p.category,
        p.product_name,
        SUM(s.revenue) AS revenue,
        SUM(s.quantity_sold) AS units
    FROM products p
    JOIN sales s ON p.product_id = s.product_id
    GROUP BY p.category, p.product_name
)
SELECT
    category,
    product_name,
    ROUND(revenue, 2) AS revenue,
    units,
    RANK()       OVER (PARTITION BY category ORDER BY revenue DESC) AS rank_in_category,
    DENSE_RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS dense_rank_in_category,
    ROUND(revenue * 100.0 / SUM(revenue) OVER (PARTITION BY category), 2) AS pct_of_category
FROM product_revenue
ORDER BY category, rank_in_category;
