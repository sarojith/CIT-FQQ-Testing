-- SQL Task 4 — Status Changes
-- Find products whose status changed from yesterday to today.
-- Output columns: product_id, product_name, old_status, new_status

SELECT
    y.product_id,
    y.product_name,
    y.status AS old_status,
    t.status AS new_status
FROM products_yesterday y
INNER JOIN products_today t
    ON y.product_id = t.product_id
WHERE y.status <> t.status;
