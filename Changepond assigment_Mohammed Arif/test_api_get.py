#!/usr/bin/env python3
"""
test_api_get.py

Simple parametrized GET-request API tests driven by test-case dicts.

Run: pytest test_api_get.py
"""

import requests
import pytest

# Define test cases
TEST_CASES = [
    {
        "name": "Get user 1",
        "input": {
            "url": "https://api.example.com/users/1",
            "params": {},
            "headers": {"Accept": "application/json"},
            "timeout": 5
        },
        "expected": {
            "status": 200,
            "json_contains": {"id": 1, "username": "alice"}
        },
        "why": "Verifies basic user retrieval endpoint and stable id mapping."
    },
    {
        "name": "Get missing resource returns 404",
        "input": {
            "url": "https://api.example.com/users/99999",
            "params": {},
            "headers": {"Accept": "application/json"},
            "timeout": 5
        },
        "expected": {
            "status": 404,
            "body_contains": "Not Found"
        },
        "why": "Ensures server returns correct status for non-existent resources."
    },
]

# Use pytest parametrize so each case shows as a separate test
@pytest.mark.parametrize("case", TEST_CASES, ids=[c["name"] for c in TEST_CASES])
def test_get_api(case):
    inp = case["input"]
    exp = case["expected"]

    # Send GET request (safe defaults)
    resp = requests.get(inp["url"],
                        params=inp.get("params"),
                        headers=inp.get("headers"),
                        timeout=inp.get("timeout", 10))

    # Check status code
    assert resp.status_code == exp["status"], f"{case['name']}: expected status {exp['status']} got {resp.status_code} -- why: {case['why']}"

    # If expected JSON fields, validate them
    if "json_contains" in exp:
        try:
            data = resp.json()
        except ValueError:
            pytest.fail(f"{case['name']}: response not JSON as expected -- why: {case['why']}")

        for k, v in exp["json_contains"].items():
            assert k in data, f"{case['name']}: missing key '{k}' in response JSON -- why: {case['why']}"
            assert data[k] == v, f"{case['name']}: key '{k}' expected {v!r} got {data[k]!r} -- why: {case['why']}"

    # If expected body substring, validate it
    if "body_contains" in exp:
        assert exp["body_contains"] in resp.text, f"{case['name']}: expected substring not found in body -- why: {case['why']}"