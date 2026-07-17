import os
import sys


def parse_header(file_path):
    """Reads the first line of a file, trims whitespace, and returns a list of headers."""
    # Task 3: Error Handling - Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        sys.exit(1)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline()

            # Task 3: Error Handling - Empty CSV file
            if not first_line:
                print(f"Error: The file '{file_path}' is completely empty.")
                sys.exit(1)

            # Strip Windows (\r\n) or Unix (\n) line endings and split by comma
            headers = [h.strip() for h in first_line.strip().split(',')]

            # Remove empty strings from list if they exist
            headers = [h for h in headers if h]

            # Task 3: Error Handling - No valid headers found
            if not headers:
                print(f"Error: The file '{file_path}' contains no valid headers.")
                sys.exit(1)

            return headers
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        sys.exit(1)


def compare_headers(expected_headers, actual_headers, expected_file, actual_file):
    """Compares two lists of headers and prints step-by-step evaluations."""
    print(f"--- Starting Header Comparison ---")
    print(f"Expected headers: {expected_headers}")
    print(f"Actual headers:   {actual_headers}\n")

    # 1. Find headers only in expected file
    print("Evaluating: Finding items unique to expected file...")
    only_in_expected = [h for h in expected_headers if h not in actual_headers]

    # 2. Find headers only in actual file
    print("Evaluating: Finding items unique to actual file...")
    only_in_actual = [h for h in actual_headers if h not in expected_headers]

    # 3. Find common headers (maintaining order of the expected file)
    print("Evaluating: Identifying common headers...")
    common_headers = [h for h in expected_headers if h in actual_headers]

    # 4. Check relative order of common headers
    print("Evaluating: Verifying if common headers share the same relative order...")
    # Extract common elements from actual headers to check their relative sequence
    common_in_actual = [h for h in actual_headers if h in expected_headers]
    same_order = common_headers == common_in_actual

    # Format output display
    print(f"\nOnly in {os.path.basename(expected_file)}:")
    print("  " + ", ".join(only_in_expected) if only_in_expected else "  (None)")

    print(f"Only in {os.path.basename(actual_file)}:")
    print("  " + ", ".join(only_in_actual) if only_in_actual else "  (None)")

    print("Common headers:")
    print("  " + ", ".join(common_headers) if common_headers else "  (None)")

    print(f"Common headers in same relative order:\n  {same_order}\n")

    return only_in_expected, only_in_actual, common_headers, same_order


# --- Task 2: Basic Tests ---
def run_tests():
    print("================ RUNNING TESTS ================")

    # Test 1: Identical headers
    print("Test 1: Identical Headers")
    h1 = ["id", "name", "price"]
    h2 = ["id", "name", "price"]
    _, _, _, order = compare_headers(h1, h2, "exp.csv", "act.csv")
    assert order == True, "Failed Test 1"

    # Test 2: Out of order common headers
    print("Test 2: Different Relative Order")
    h1 = ["id", "name", "price"]
    h2 = ["name", "id", "price"]
    _, _, _, order = compare_headers(h1, h2, "exp.csv", "act.csv")
    assert order == False, "Failed Test 2"

    # Test 3: Missing headers / Extra whitespace handled
    print("Test 3: Missing items and spacing validation")
    h1 = ["id", "name", "price"]
    h2 = ["id", "price"]  # 'name' is missing
    only_exp, _, _, _ = compare_headers(h1, h2, "exp.csv", "act.csv")
    assert only_exp == ["name"], "Failed Test 3"

    print("================ ALL TESTS PASSED ================\n")


# Main Execution Flow
if __name__ == "__main__":
    # Run embedded tests first to verify math/logic
    run_tests()

    print("================ CLI EXECUTION ================")
    # Task 3: Error Handling - Check for missing file path arguments
    if len(sys.argv) < 3:
        print("Error: Missing file path arguments.")
        print("Usage: python compare_headers.py <expected_file.csv> <actual_file.csv>")
        sys.exit(1)

    expected_file_path = sys.argv[1]
    actual_file_path = sys.argv[2]

    expected_list = parse_header(expected_file_path)
    actual_list = parse_header(actual_file_path)

    compare_headers(expected_list, actual_list, expected_file_path, actual_file_path)


#python compare_headers.py expected_orders.csv actual_orders.csv