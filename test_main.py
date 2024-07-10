import unittest
from unittest.mock import patch
from main import (
    allocate_stocks,
    combine_allocations,
    limit_and_reallocate,
    validate_inputs,
)


class TestStockAllocation(unittest.TestCase):
    def test_allocate_stocks(self):
        stocks = ["AAPL", "GOOGL", "MSFT"]
        total_percentage = 100
        ratio = 0.8
        result = allocate_stocks(stocks, total_percentage, ratio)
        self.assertEqual(len(result), 3)
        self.assertAlmostEqual(sum(result.values()), 100, places=2)

    def test_combine_allocations(self):
        allocations = [{"AAPL": 50, "GOOGL": 30}, {"GOOGL": 20, "MSFT": 40}]
        result = combine_allocations(allocations)
        self.assertEqual(result, {"AAPL": 50, "GOOGL": 50, "MSFT": 40})

    def test_limit_and_reallocate(self):
        allocations = {"AAPL": 40, "GOOGL": 30, "MSFT": 20, "AMZN": 10}
        limit = 3
        ratio = 0.8
        total_amount = 1000
        min_dollar_amount = 0
        result = limit_and_reallocate(
            allocations, limit, ratio, total_amount, min_dollar_amount
        )
        self.assertEqual(len(result), 3)
        self.assertAlmostEqual(sum(result.values()), 100, places=2)

    def test_validate_inputs_valid(self):
        stock_lists = {"A": ["AAPL", "GOOGL"], "B": ["MSFT", "AMZN"]}
        allocations = {"A": 60, "B": 40}
        try:
            validate_inputs(stock_lists, allocations)
        except ValueError:
            self.fail("validate_inputs raised ValueError unexpectedly!")

    def test_validate_inputs_mismatch(self):
        stock_lists = {"A": ["AAPL", "GOOGL"], "B": ["MSFT", "AMZN"]}
        allocations = {"A": 60, "C": 40}
        with self.assertRaises(ValueError):
            validate_inputs(stock_lists, allocations)

    def test_validate_inputs_incorrect_total(self):
        stock_lists = {"A": ["AAPL", "GOOGL"], "B": ["MSFT", "AMZN"]}
        allocations = {"A": 60, "B": 50}
        with self.assertRaises(ValueError):
            validate_inputs(stock_lists, allocations)

    @patch("main.os.environ")
    def test_get_stock_lists(self, mock_environ):
        mock_environ.items.return_value = [
            ("STOCK_LIST_A", "AAPL,GOOGL"),
            ("STOCK_LIST_B", "MSFT,AMZN"),
            ("OTHER_VAR", "IRRELEVANT"),
        ]
        from main import get_stock_lists

        result = get_stock_lists()
        self.assertEqual(result, {"A": ["AAPL", "GOOGL"], "B": ["MSFT", "AMZN"]})

    @patch("main.os.environ")
    def test_get_allocations(self, mock_environ):
        mock_environ.items.return_value = [
            ("ALLOCATION_A", "60"),
            ("ALLOCATION_B", "40"),
            ("OTHER_VAR", "IRRELEVANT"),
        ]
        from main import get_allocations

        result = get_allocations()
        self.assertEqual(result, {"A": 60.0, "B": 40.0})


if __name__ == "__main__":
    unittest.main()
