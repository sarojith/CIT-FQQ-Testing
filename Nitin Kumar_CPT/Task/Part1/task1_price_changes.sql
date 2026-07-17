-- SQL Task 1 — Price Changes
-- Find products whose price changed from yesterday to today.
-- Output columns: product_id, product_name, old_price, new_price

SELECT
    y.product_id,
    y.product_name,
    y.price AS old_price,
    t.price AS new_price
FROM products_yesterday y
INNER JOIN products_today t
    ON y.product_id = t.product_id
WHERE y.price <> t.price;
