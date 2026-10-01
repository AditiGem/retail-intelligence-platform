SELECT
    DATE_FORMAT(sale_date, '%Y-%m') AS month,
    COUNT(*)                        AS orders,
    ROUND(SUM(revenue), 2)          AS revenue,
    ROUND(AVG(revenue), 2)          AS aov,
    ROUND(
        AVG(revenue) - LAG(AVG(revenue)) OVER (ORDER BY DATE_FORMAT(sale_date, '%Y-%m')),
        2
    ) AS aov_change
FROM sales
GROUP BY DATE_FORMAT(sale_date, '%Y-%m')
ORDER BY month;
