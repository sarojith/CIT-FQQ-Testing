"""Compare the headers of two CSV files.

Usage:
    python compare_headers.py <expected_csv_path> <actual_csv_path>
"""

import os
import sys


def get_headers(filepath):
    """Read the first line of a CSV file and return its trimmed, non-empty headers."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, encoding="utf-8-sig") as f:
        first_line = f.readline()

    if not first_line.strip():
        raise ValueError(f"File is empty: {filepath}")

    headers = [field.strip() for field in first_line.strip().split(",")]
    headers = [h for h in headers if h]

    if not headers:
        raise ValueError(f"Header row exists but contains no valid headers: {filepath}")

    return headers


def compare_headers(expected, actual):
    """Compare two header lists and return only-expected, only-actual, common, and same-order."""
    only_expected = [h for h in expected if h not in actual]
    only_actual = [h for h in actual if h not in expected]

    common = [h for h in expected if h in actual]
    common_in_actual_order = [h for h in actual if h in expected]
    same_order = common == common_in_actual_order

    return only_expected, only_actual, common, same_order


def print_list(title, items):
    print(title)
    for item in items:
        print(item)
    print()


def main():
    if len(sys.argv) != 3:
        print(
            "Usage: python compare_headers.py <expected_csv_path> <actual_csv_path>",
            file=sys.stderr,
        )
        sys.exit(1)

    expected_path, actual_path = sys.argv[1], sys.argv[2]

    try:
        expected_headers = get_headers(expected_path)
        actual_headers = get_headers(actual_path)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    only_expected, only_actual, common, same_order = compare_headers(
        expected_headers, actual_headers
    )

    print_list(f"Only in {os.path.basename(expected_path)}:", only_expected)
    print_list(f"Only in {os.path.basename(actual_path)}:", only_actual)
    print_list("Common headers:", common)
    print("Common headers in same relative order:")
    print(str(same_order).lower())


if __name__ == "__main__":
    main()
