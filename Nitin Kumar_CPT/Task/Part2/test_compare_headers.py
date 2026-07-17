"""Tests for compare_headers.py

Run with:
    python -m unittest test_compare_headers.py -v
"""

import os
import tempfile
import unittest

from compare_headers import compare_headers, get_headers


class CompareHeadersTests(unittest.TestCase):
    def make_csv(self, content):
        fd, path = tempfile.mkstemp(suffix=".csv")
        with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
            f.write(content)
        self.addCleanup(os.remove, path)
        return path

    def test_identical_headers(self):
        expected = ["order_id", "customer_id", "amount"]
        actual = ["order_id", "customer_id", "amount"]

        only_expected, only_actual, common, same_order = compare_headers(expected, actual)

        self.assertEqual(only_expected, [])
        self.assertEqual(only_actual, [])
        self.assertEqual(common, expected)
        self.assertTrue(same_order)

    def test_missing_header(self):
        expected = ["order_id", "customer_id", "amount"]
        actual = ["order_id", "customer_id"]

        only_expected, only_actual, common, same_order = compare_headers(expected, actual)

        self.assertEqual(only_expected, ["amount"])
        self.assertEqual(only_actual, [])
        self.assertEqual(common, ["order_id", "customer_id"])
        self.assertTrue(same_order)

    def test_headers_only_on_each_side(self):
        expected = ["order_id", "amount", "created_at", "country"]
        actual = ["order_id", "total_amount", "processed_at", "country_code"]

        only_expected, only_actual, common, same_order = compare_headers(expected, actual)

        self.assertEqual(only_expected, ["amount", "created_at", "country"])
        self.assertEqual(only_actual, ["total_amount", "processed_at", "country_code"])
        self.assertEqual(common, ["order_id"])
        self.assertTrue(same_order)

    def test_common_headers_in_different_order(self):
        expected = ["order_id", "customer_id", "currency", "status"]
        actual = ["order_id", "status", "customer_id", "currency"]

        _, _, common, same_order = compare_headers(expected, actual)

        self.assertEqual(set(common), set(expected))
        self.assertFalse(same_order)

    def test_headers_with_extra_spaces_are_trimmed(self):
        path = self.make_csv("order_id,  customer_id ,  amount\n1,C001,100.50\n")

        self.assertEqual(get_headers(path), ["order_id", "customer_id", "amount"])

    def test_windows_line_endings(self):
        path = self.make_csv("order_id,customer_id,amount\r\n1,C001,100.50\r\n")

        self.assertEqual(get_headers(path), ["order_id", "customer_id", "amount"])

    def test_file_does_not_exist(self):
        with self.assertRaises(FileNotFoundError):
            get_headers("this_file_does_not_exist.csv")

    def test_empty_csv_file(self):
        path = self.make_csv("")

        with self.assertRaises(ValueError):
            get_headers(path)

    def test_header_row_with_no_valid_headers(self):
        path = self.make_csv(" , , \n1,2,3\n")

        with self.assertRaises(ValueError):
            get_headers(path)


if __name__ == "__main__":
    unittest.main()
