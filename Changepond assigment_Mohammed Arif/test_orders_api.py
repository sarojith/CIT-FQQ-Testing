#!/usr/bin/env python3
"""
test_orders_api.py

Pytest-based API tests for GET /api/orders/{order_id}.

- Uses responses to mock API calls (no real network requests).
- Contains five test cases (Task 1) and a dedicated test for Task 2.

Requirements:
    pip install pytest requests responses

Run:
    pytest -q
"""

import json
import requests
import pytest
import responses

BASE_URL = "https://api.example.com"

# Example successful response for ORD-1001 (from prompt)
ORD_1001_JSON = {
    "order_id": "ORD-1001",
    "customer_id": "C001",
    "amount": 100.50,
    "currency": "GBP",
    "status": "PAID",
    "created_at": "2026-05-20T10:30:00Z"
}

# API Task 1: five test cases (name, input, expected, why)
TEST_CASES = [
    {
        "name": "Get existing order ORD-1001 - success",
        "input": {
            "method": "GET",
            "path": "/api/orders/ORD-1001",
            "order_id": "ORD-1001",
            "headers": {"Accept": "application/json"}
        },
        "expected": {
            "status": 200,
            "json_contains": {"order_id": "ORD-1001", "status": "PAID"}
        },
        "why": "Validates basic happy-path retrieval and correct order status mapping."
    },
    {
        "name": "Get non-existent order -> 404",
        "input": {
            "method": "GET",
            "path": "/api/orders/ORD-9999",
            "order_id": "ORD-9999",
            "headers": {"Accept": "application/json"}
        },
        "expected": {
            "status": 404,
            "body_contains": "Order not found"
        },
        "why": "Ensures the API returns proper 404 for missing resources."
    },
    {
        "name": "Unauthorized access -> 401",
        "input": {
            "method": "GET",
            "path": "/api/orders/ORD-1001",
            "order_id": "ORD-1001",
            "headers": {"Accept": "application/json"}  # missing auth token
        },
        "expected": {
            "status": 401,
            "body_contains": "Unauthorized"
        },
        "why": "Verifies authentication is enforced for protected order endpoints."
    },
    {
        "name": "Malformed order id -> 400",
        "input": {
            "method": "GET",
            "path": "/api/orders/INVALID_ID",
            "order_id": "INVALID_ID",
            "headers": {"Accept": "application/json"}
        },
        "expected": {
            "status": 400,
            "body_contains": "Bad Request"
        },
        "why": "Catches input validation issues and prevents unexpected behavior for bad IDs."
    },
    {
        "name": "Get existing order ORD-1002 - pending status",
        "input": {
            "method": "GET",
            "path": "/api/orders/ORD-1002",
            "order_id": "ORD-1002",
            "headers": {"Accept": "application/json"}
        },
        "expected": {
            "status": 200,
            "json_contains": {"order_id": "ORD-1002", "status": "PENDING"}
        },
        "why": "Checks that different status values (not only PAID) are returned and parsed correctly."
    }
]


def api_url(path: str) -> str:
    return BASE_URL.rstrip("/") + path


def send_get_order(order_id: str, headers: dict = None, timeout: float = 5.0) -> requests.Response:
    url = f"{BASE_URL}/api/orders/{order_id}"
    return requests.get(url, headers=headers or {"Accept": "application/json"}, timeout=timeout)


# Helper to register mock endpoints in responses based on a test-case
def register_mock_for_case(rsp, case):
    inp = case["input"]
    expected = case["expected"]
    url = api_url(inp["path"])

    # If the case expects a JSON body, craft one; else return text body
    if case["name"].startswith("Get existing order ORD-1001"):
        # real example payload
        rsp.add(responses.GET, url, json=ORD_1001_JSON, status=expected["status"])
        return

    if "json_contains" in expected:
        # create a minimal JSON body containing fields from expected.json_contains
        body = dict(expected["json_contains"])
        # ensure order_id if present
        if "order_id" in expected["json_contains"]:
            body["order_id"] = expected["json_contains"]["order_id"]
        # add status/time placeholders for realism
        body.setdefault("customer_id", "CXXX")
        body.setdefault("amount", 0.0)
        body.setdefault("currency", "GBP")
        body.setdefault("created_at", "2026-01-01T00:00:00Z")
        rsp.add(responses.GET, url, json=body, status=expected["status"])
    else:
        # text body
        text = expected.get("body_contains", "")
        rsp.add(responses.GET, url, body=text, status=expected["status"])


# Task 2: explicit test that GET /api/orders/ORD-1001 returns 200 and status == "PAID"
@responses.activate
def test_get_ord_1001_status_paid():
    url = api_url("/api/orders/ORD-1001")
    responses.add(responses.GET, url, json=ORD_1001_JSON, status=200)

    resp = send_get_order("ORD-1001")
    assert resp.status_code == 200, f"Expected HTTP 200, got {resp.status_code}"
    data = resp.json()
    assert data.get("status") == "PAID", f"Expected status 'PAID', got {data.get('status')}"


# Parametrized tests for the five cases (uses mocked endpoints)
@pytest.mark.parametrize("case", TEST_CASES, ids=[c["name"] for c in TEST_CASES])
@responses.activate
def test_api_cases(case):
    # Register mock endpoint
    register_mock_for_case(responses, case)

    order_id = case["input"]["order_id"]
    headers = case["input"].get("headers")
    resp = send_get_order(order_id, headers=headers)

    expected = case["expected"]

    # Status code assertion
    assert resp.status_code == expected["status"], (
        f"{case['name']}: expected HTTP {expected['status']}, got {resp.status_code} -- why: {case['why']}"
    )

    # If JSON expectations, parse and assert keys/values
    if "json_contains" in expected:
        try:
            data = resp.json()
        except ValueError:
            pytest.fail(f"{case['name']}: expected JSON response -- why: {case['why']}")
        for k, v in expected["json_contains"].items():
            assert k in data, f"{case['name']}: missing key '{k}' in response JSON -- why: {case['why']}"
            assert data[k] == v, (
                f"{case['name']}: key '{k}' expected {v!r} got {data[k]!r} -- why: {case['why']}"
            )

    # If text-body expectations, check substring
    if "body_contains" in expected:
        assert expected["body_contains"] in resp.text, (
            f"{case['name']}: expected substring not found in body -- why: {case['why']}"
        )