# Task Submission — README

This repository is organized into three parts:
- `Part1/` — Part A: SQL Exercise
- `Part2/` — Part B: CSV Header Comparison Tool
- `Part3/` — Part C: API Test Design

## 1. Language Used

- **Part A (SQL)** — Standard ANSI SQL. Written to run on any common RDBMS (PostgreSQL, MySQL, SQL Server, SQLite). Verified against **SQLite 3**.
- **Part B (CSV comparison tool)** — **Python 3** (standard library only: `csv`, `os`, `sys`; tests use `unittest` + `tempfile`).
- **Part C (API tests)** — Test cases are language-agnostic; the automated test is provided as **pseudo-code** styled after Python's `requests` library, as requested.

## 2. How to Run the CSV Comparison Tool

From inside `Part2/`:

```
python compare_headers.py expected_orders.csv actual_orders.csv
```

This prints headers only in the expected file, only in the actual file, the common headers, and whether the common headers appear in the same relative order.

## 3. How to Run the Tests

From inside `Part2/`:

```
python -m unittest test_compare_headers.py -v
```

This runs 9 tests covering identical headers, missing headers, extra whitespace, Windows (`\r\n`) line endings, reordered common headers, headers unique to one side, a missing file, an empty file, and a header row with no valid headers.

## 4. SQL Answers

Full setup and query files are in `Part1/` (`schema.sql`, `task1_price_changes.sql` … `task4_status_changes.sql`), verified to produce the expected output. Summary:

**Task 1 — Price Changes**
```sql
SELECT y.product_id, y.product_name, y.price AS old_price, t.price AS new_price
FROM products_yesterday y
INNER JOIN products_today t ON y.product_id = t.product_id
WHERE y.price <> t.price;
```

**Task 2 — New Products**
```sql
SELECT t.product_id, t.product_name, t.price, t.status
FROM products_today t
LEFT JOIN products_yesterday y ON t.product_id = y.product_id
WHERE y.product_id IS NULL;
```

**Task 3 — Missing Products**
```sql
SELECT y.product_id, y.product_name, y.price, y.status
FROM products_yesterday y
LEFT JOIN products_today t ON y.product_id = t.product_id
WHERE t.product_id IS NULL;
```

**Task 4 — Status Changes**
```sql
SELECT y.product_id, y.product_name, y.status AS old_status, t.status AS new_status
FROM products_yesterday y
INNER JOIN products_today t ON y.product_id = t.product_id
WHERE y.status <> t.status;
```

**Task 5 — Explanation** (full detail in `Part1/README.md`):
- `INNER JOIN` is used for Tasks 1 & 4 because a price/status "change" is only meaningful for a product present in both snapshots. `LEFT JOIN ... IS NULL` is used for Tasks 2 & 3 to express set difference ("in one table but not the other"); `NOT EXISTS` would work identically and is a safer alternative to `NOT IN`.
- If `product_id` were not unique, the joins would multiply rows (a cartesian match between duplicates on each side), producing incorrect/duplicated results — the data would need deduplication or a truly unique key before joining.
- If `price` or `status` can be `NULL`, plain `<>` comparisons silently miss real changes (SQL's three-valued logic means `NULL <> NULL` and `NULL <> <value>` both evaluate to `UNKNOWN`, not `TRUE`), so a NULL-safe comparison is needed instead.

## 5. API Test Cases

Full detail in `Part3/api_test_cases.txt`. Five automated test cases for `GET /api/orders/{order_id}`:

1. **Get existing order returns 200 with correct data** — baseline happy-path check.
2. **Get non-existent order returns 404** — verifies graceful handling of unknown resources.
3. **Get order with invalid order_id format returns 400** — verifies input validation before lookup.
4. **Response schema and data types are correct** — catches contract-breaking changes (missing fields, wrong types).
5. **Unauthorized request is rejected (401)** — verifies order/customer data is protected.

The automated pseudo-code test (`Part3/test_get_order_pseudocode.txt`) validates that `GET /api/orders/ORD-1001` returns HTTP 200 and `status == "PAID"`.

## 6. Assumptions Made

- **Part A:** `product_id` is unique per table (as implied by the sample data acting as a primary key); `price` and `status` are assumed non-NULL in the base queries, with the NULL-handling caveat called out separately in the explanation rather than baked into every query, since the sample data contains no NULLs.
- **Part B:** CSV files are UTF-8 encoded, comma-delimited, and header names do not contain embedded commas requiring quoting beyond what Python's `csv` module already handles. A header field that is blank after trimming (e.g. a trailing comma) is treated as "not a valid header" and excluded from comparison. "Same relative order" is judged only across the headers common to both files, ignoring headers unique to one side.
- **Part C:** The endpoint follows standard REST conventions (200 for success, 404 for not found, 400 for malformed input, 401 for missing/invalid auth) even though only the success example was given in the prompt. `amount` is assumed numeric and `created_at` is assumed to be ISO 8601 formatted, based on the sample response.

## 7. AI Usage Statement

This solution was developed with the assistance of **Claude (Claude Code)**, an AI coding assistant. AI was used to draft the SQL queries, the Python CSV comparison tool and its tests, the API test case designs, and this documentation. All SQL queries were executed against a real SQLite database and all Python code was executed (including the full test suite) to verify correctness before being included here — nothing was submitted without being run and checked against the expected output.
