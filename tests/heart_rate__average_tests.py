import unittest
import pandas as pd
from unittest.mock import patch
from io import StringIO
import matplotlib.pyplot as plt
from src.AverageHeartRate import RestingHeartRateAnalyzer


class TestRestingHeartRateAnalyzer(unittest.TestCase):

    def setUp(self):
        # Create a sample CSV data for testing
        self.sample_data = """endDate,value
        2022-01-01,60
        2022-02-01,65
        2022-02-15,70
        2022-03-01,75
        2022-03-15,80
        2023-01-01,85
        2023-02-01,90
        2023-03-01,95"""

        self.analyzer = RestingHeartRateAnalyzer(StringIO(self.sample_data))

    @patch('matplotlib.pyplot.show')
    def test_plot_monthly_average(self, mock_show):
        self.analyzer.load_data()
        self.analyzer.preprocess_data()

        # Capture the plot output
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.analyzer.plot_monthly_average()

        # Ensure that the plot is being shown
        mock_show.assert_called_once()

        # Add more specific tests based on your expectations
        # For example, check the output on stdout, or check the plot title, labels, etc.

    def test_calculate_monthly_average(self):
        self.analyzer.load_data()
        self.analyzer.preprocess_data()

        # Test the calculation of monthly averages
        result = self.analyzer.calculate_monthly_average()
        self.assertIsInstance(result, pd.DataFrame)

        # Ensure the resulting DataFrame has the correct columns
        self.assertListEqual(list(result.columns), ['month_year', 'value'])

        # Print the average heart rate for each month
        print("Average Heart Rate for Each Month:")
        print(result)

    def test_preprocess_data(self):
        self.analyzer.load_data()

        # Test the preprocess_data method
        self.analyzer.preprocess_data()

        # Add more specific tests based on your expectations
        # For example, check if the 'month_year' column is created, or if 'endDate' is converted to datetime


if __name__ == '__main__':
    unittest.main()
