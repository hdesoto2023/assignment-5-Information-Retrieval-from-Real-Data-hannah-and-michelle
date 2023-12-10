import unittest
import pandas as pd
from io import StringIO
from src.Prediction import RestingHeartRateAnalyzer

class TestRestingHeartRateAnalyzer(unittest.TestCase):

    def setUp(self):
        # Example data for testing
        self.sample_data = """endDate,value
        2022-01-01,60
        2022-02-01,65
        2022-02-15,70
        2022-03-01,75
        2022-03-15,80
        2023-01-01,85
        2023-02-01,90
        2023-03-01,95"""

        # Create an instance of RestingHeartRateAnalyzer for testing
        self.analyzer = RestingHeartRateAnalyzer(StringIO(self.sample_data))

    def test_load_data(self):
        self.analyzer.load_data()
        self.assertIsNotNone(self.analyzer.df)
        self.assertEqual(len(self.analyzer.df), 8)

    def test_preprocess_data(self):
        self.analyzer.load_data()
        self.analyzer.preprocess_data()
        self.assertIn('month_year', self.analyzer.df.columns)
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(self.analyzer.df['endDate']))

    def test_calculate_monthly_average(self):
        self.analyzer.load_data()
        self.analyzer.preprocess_data()
        monthly_average_hr = self.analyzer.calculate_monthly_average()
        self.assertEqual(len(monthly_average_hr), 6)
        self.assertEqual(monthly_average_hr['month_year'].nunique(), 6)

    def test_save_monthly_average_to_file(self):
        self.analyzer.load_data()
        self.analyzer.preprocess_data()
        output_file = '/path/to/test_output/average_heart_rates_test.csv'
        self.analyzer.save_monthly_average_to_file(output_file)
        self.assertTrue(pd.read_csv(output_file).shape, (6, 2))

    def test_predict_heart_rate(self):
        self.analyzer.load_data()
        self.analyzer.preprocess_data()
        fit_model = self.analyzer.train_arima_model()
        predictions = self.analyzer.predict_heart_rate(fit_model, num_periods=3)
        self.assertEqual(predictions.shape, (3, 2))
        self.assertEqual(predictions['endDate'].min(), pd.to_datetime('2023-03-31'))


if __name__ == '__main__':
    unittest.main()
