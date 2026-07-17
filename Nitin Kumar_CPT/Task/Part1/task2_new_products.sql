-- SQL Task 2 — New Products
-- Find products that are new today, meaning they exist in products_today but not in products_yesterday.
-- Output columns: product_id, product_name, price, status

SELECT
    t.product_id,
    t.product_name,
    t.price,
    t.status
FROM products_today t
LEFT JOIN products_yesterday y
    ON t.product_id = y.product_id
WHERE y.product_id IS NULL;
