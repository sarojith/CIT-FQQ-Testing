-- SQL Task 3 — Missing Products
-- Find products that existed yesterday but are missing today.
-- Output columns: product_id, product_name, price, status

SELECT
    y.product_id,
    y.product_name,
    y.price,
    y.status
FROM products_yesterday y
LEFT JOIN products_today t
    ON y.product_id = t.product_id
WHERE t.product_id IS NULL;
