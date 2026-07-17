# Orders API Tests and CSV Header Comparator
Language used
- Python 3.9+ (tests use pytest, requests, responses)

1. SQL assignment quetioneries and answers
   In your README, briefly explain:
   Why did you use INNER JOIN, LEFT JOIN, NOT EXISTS, or another approach? Because joins are easy to filer and easy to comparing and filters out any duplicate and nulls
   What would change if product_id was not unique? will use muplti cobination to compare
   What issue could happen if price or status can be NULL? will be filetered out only the matching and unmatching record

2. How to run the CSV comparison tool
- The CSV comparison script is `compare_csv_headers.py` (provided separately).
- Example:
  - pip install (if needed): none required beyond Python stdlib for the simple script
  - Run: `python compare_csv_headers.py file_a.csv file_b.csv`
  - Optional: `--ignore-case` to compare headers case-insensitively.

3. How to run the tests
- Create a virtualenv and install dependencies:
  - pip install pytest requests responses
- Run tests:
  - `pytest -q`
- The tests are offline using the `responses` library; they do not call a real API.

4. SQL answers (example queries relevant to orders)
- Count paid orders:
  - `SELECT COUNT(*) FROM orders WHERE status = 'PAID';`
- Total revenue for GBP paid orders:
  - `SELECT SUM(amount) FROM orders WHERE currency = 'GBP' AND status = 'PAID';`
- Find recent orders in May 2026:
  - `SELECT * FROM orders WHERE created_at >= '2026-05-01' AND created_at < '2026-06-01';`

5. API test cases (summary of the five designed)
- Get existing order ORD-1001 - success
  - Input: GET /api/orders/ORD-1001
  - Expected: 200, JSON includes order_id=ORD-1001 and status=PAID
  - Why: Verify happy-path retrieval.
- Get non-existent order -> 404
  - Input: GET /api/orders/ORD-9999
  - Expected: 404, body contains "Order not found"
  - Why: Validate proper handling of missing resources.
- Unauthorized access -> 401
  - Input: GET /api/orders/ORD-1001 (no auth)
  - Expected: 401
  - Why: Ensure authentication is enforced.
- Malformed order id -> 400
  - Input: GET /api/orders/INVALID_ID
  - Expected: 400, body contains "Bad Request"
  - Why: Check validation and error messaging for bad input.
- Get existing order ORD-1002 - pending status
  - Input: GET /api/orders/ORD-1002
  - Expected: 200, JSON includes status=PENDING
  - Why: Verify handling of non-finalized orders.

6. Assumptions made
- API base URL used in tests: https://api.example.com
- Date/time format follows ISO-8601 with Z suffix (UTC).
- Order IDs use the form ORD-XXXX.
- Authentication is not required for mocked tests; a 401 case is included to verify auth behavior.
- Tests use local mocking (responses) so they are deterministic and offline.

7. AI usage statement
- I used an AI assistant (ChatGPT) to help draft test-case descriptions and example test code. The prompt provided to the assistant was the task text (the "C — Basic API Testing Thinking" block). I reviewed and edited the AI output to ensure correctness and to make tests deterministic (mocked with `responses`). I understand and can explain and modify every line of the code submitted.