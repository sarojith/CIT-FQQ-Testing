# AI Transcript

This document is a transparency record of how an AI assistant (Claude Code) was used to complete this task. It summarizes each request made and what the assistant produced/did in response, including verification steps. The rephrased prompt text itself is in [prompt.md](prompt.md).

---

### 1. Part A — SQL Exercise

**Request:** Create `Part1/` containing the SQL exercise: price changes, new products, missing products, status changes, and a short explanation.

**AI actions:**
- Created `Part1/schema.sql` with `CREATE TABLE` statements and the sample data for `products_yesterday` and `products_today`.
- Wrote one `.sql` file per task (`task1_price_changes.sql` … `task4_status_changes.sql`) using `INNER JOIN` (Tasks 1 & 4) and `LEFT JOIN ... IS NULL` (Tasks 2 & 3).
- Wrote `Part1/README.md` covering the Task 5 explanation (join/lookup rationale, non-unique `product_id` implications, NULL-comparison pitfalls).
- **Verified** by loading `schema.sql` into a real SQLite database and executing all four queries, confirming the output matched the expected rows exactly before considering the task done.

---

### 2. Part B — CSV Header Comparison Tool

**Request:** Create `Part2/` with the two sample CSVs and a CLI tool that reads only the header row of each file, trims whitespace, and reports differences/order; plus tests and explicit error handling for four failure cases.

**AI actions:**
- Created `Part2/expected_orders.csv` and `Part2/actual_orders.csv` from the given data.
- Wrote `Part2/compare_headers.py` (Python 3, standard library `csv`/`os`/`sys` only) with separate functions for reading, parsing, validating, and comparing headers, plus a CLI `main()`.
- Wrote `Part2/test_compare_headers.py` (`unittest`) with 9 tests covering identical headers, a missing header, extra whitespace, Windows (`\r\n`) line endings, reordered common headers, headers unique to each side, missing file, empty file, and a header row with no valid headers.
- Wrote `Part2/README.md` documenting usage, sample output, internal logic, and the error-handling table.
- **Verified** by running the tool against the sample CSVs (output matched the spec's expected console output exactly), running the full test suite (9/9 passed), and manually triggering all four required error scenarios via the CLI to confirm clear messages and a non-zero exit code instead of a crash or silent failure.

---

### 3. Part C — API Test Design

**Request:** Create `Part3/` with exactly five automated test cases for `GET /api/orders/{order_id}` (name, input, expected result, rationale for each), and pseudo-code (not real code) for one automated test checking that `GET /api/orders/ORD-1001` returns HTTP 200 with `status = PAID`.

**AI actions:**
- Wrote `Part3/api_test_cases.txt` with exactly five test cases: valid order lookup (200), non-existent order (404), invalid `order_id` format (400), response schema/type validation, and unauthorized access (401).
- Wrote `Part3/test_get_order_pseudocode.txt` with pseudo-code only, styled after Python's `requests` library, asserting status code 200 and `status == "PAID"`.

---

### 4. Run and Verify Everything

**Request:** Run all tasks created so far, confirm there are no errors, and provide the exact run commands.

**AI actions:**
- Re-ran the full SQL setup and all four queries against a fresh SQLite database — exit code 0, output matched expectations.
- Re-ran `compare_headers.py` against the sample CSVs and the full `unittest` suite — exit code 0, all 9 tests passed.
- Reported back the exact commands for both parts (`sqlite3 ... < *.sql`, `python compare_headers.py ...`, `python -m unittest ...`).

---

### 5. Part D — Overall README

**Request:** Create a top-level `README.md` covering: language(s) used, how to run the CSV tool, how to run the tests, the SQL answers, the API test cases, assumptions made, and an AI usage disclosure statement.

**AI actions:**
- Authored `README.md` (later relocated by the user into `Part4/`) consolidating all seven required sections, including the full SQL query text, a summary of the five API test cases, explicit assumptions for each part, and an AI usage statement.

---

### 6. Prompt Log

**Request:** Rephrase and record all prompts given so far into a separate `prompt.md` file.

**AI actions:**
- Authored `prompt.md` (later relocated by the user into `Part4/`) with a rephrased, numbered log of every prompt in the conversation up to that point.

---

### 7. This File

**Request:** Create an `AI_TRANSCRIPT.md` file.

**AI actions:**
- Authored this file, `Part4/AI_TRANSCRIPT.md`, summarizing each prompt and the corresponding AI actions/verification across the whole task, as a transparency record of AI involvement in the submission.

---

## Summary Disclosure

All code, SQL, and documentation in this submission were drafted with the assistance of **Claude (Claude Code)**. Every runnable artifact (the SQL queries and the Python CSV tool with its test suite) was actually executed by the assistant and its output checked against the expected results before being included — nothing here is unverified AI output.
