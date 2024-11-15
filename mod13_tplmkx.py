import unittest
import re
from datetime import datetime

class TestStockVisualizerInputs(unittest.TestCase):

    def test_symbol(self):
        valid_symbols = ["AAPL", "GOOG", "MSFT"]
        invalid_symbols = ["aapl", "123", "TOOLONGSYM", "SYM&"]

        for symbol in valid_symbols:
            self.assertTrue(re.match(r'^[A-Z]{1,7}$', symbol), f"Valid symbol {symbol} failed")
        
        for symbol in invalid_symbols:
            self.assertFalse(re.match(r'^[A-Z]{1,7}$', symbol), f"Invalid symbol {symbol} passed")

    def test_chart_type(self):
        valid_chart_types = ["1", "2"]
        invalid_chart_types = ["0", "3", "10", "abc"]

        for chart_type in valid_chart_types:
            self.assertTrue(chart_type in ["1", "2"], f"Valid chart type {chart_type} failed")
        
        for chart_type in invalid_chart_types:
            self.assertFalse(chart_type in ["1", "2"], f"Invalid chart type {chart_type} passed")

    def test_time_series(self):
        valid_time_series = ["1", "2", "3", "4"]
        invalid_time_series = ["0", "5", "a", "12"]

        for ts in valid_time_series:
            self.assertTrue(ts in ["1", "2", "3", "4"], f"Valid time series {ts} failed")
        
        for ts in invalid_time_series:
            self.assertFalse(ts in ["1", "2", "3", "4"], f"Invalid time series {ts} passed")

    def test_start_date(self):
        valid_dates = ["2023-01-01", "2024-11-07"]
        invalid_dates = ["01-01-2023", "2024/11/07", "20241107", "abcd-ef-gh"]

        for date in valid_dates:
            try:
                datetime.strptime(date, "%Y-%m-%d")
                valid = True
            except ValueError:
                valid = False
            self.assertTrue(valid, f"Valid start date {date} failed")

        for date in invalid_dates:
            try:
                datetime.strptime(date, "%Y-%m-%d")
                valid = True
            except ValueError:
                valid = False
            self.assertFalse(valid, f"Invalid start date {date} passed")

    def test_end_date(self):
        valid_dates = ["2023-12-31", "2024-01-01"]
        invalid_dates = ["12/31/2023", "20240101", "2023-13-01", "abcd-ef-gh"]

        for date in valid_dates:
            try:
                datetime.strptime(date, "%Y-%m-%d")
                valid = True
            except ValueError:
                valid = False
            self.assertTrue(valid, f"Valid end date {date} failed")

        for date in invalid_dates:
            try:
                datetime.strptime(date, "%Y-%m-%d")
                valid = True
            except ValueError:
                valid = False
            self.assertFalse(valid, f"Invalid end date {date} passed")

if __name__ == "__main__":
    unittest.main()
