import unittest
import os
import pandas as pd
from io import StringIO
from unittest.mock import patch
from src.Prediction import RestingHeartRatePredictor, xml_to_csv


class TestRestingHeartRatePredictor(unittest.TestCase):
    def setUp(self):
        self.file_path = 'test_data.csv'
        self.xml_file_path = 'test_input.xml'
        self.csv_file_path = 'test_output.csv'

        # Sample data for testing
        test_data = {
            'creationDate': ['2022-01-01', '2022-01-02', '2022-01-03'],
            'value': [60, 65, 70],
        }
        pd.DataFrame(test_data).to_csv(self.file_path, index=False)

        # Sample XML data for testing
        xml_content = """
        <root>
            <record>
                <field1>value1</field1>
                <field2>value2</field2>
            </record>
            <record>
                <field1>value3</field1>
                <field2>value4</field2>
            </record>
        </root>
        """
        with open(self.xml_file_path, 'w') as xml_file:
            xml_file.write(xml_content)

    def tearDown(self):
        # Remove temporary files created during testing
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        if os.path.exists(self.xml_file_path):
            os.remove(self.xml_file_path)
        if os.path.exists(self.csv_file_path):
            os.remove(self.csv_file_path)

    def test_resting_heart_rate_predictor(self):
        predictor = RestingHeartRatePredictor(self.file_path)

        # Test preprocess_data method
        predictor.preprocess_data()
        self.assertTrue('month' in predictor.df.columns)
        self.assertTrue('year' in predictor.df.columns)

        # Test cluster_data method
        predictor.cluster_data()
        self.assertTrue('cluster' in predictor.df.columns)

        # Test train_regression_model method
        predictor.train_regression_model()
        self.assertTrue(hasattr(predictor, 'model'))

        # Test predict_future_heart_rate method
        with patch('matplotlib.pyplot.show') as mock_show:
            predictor.predict_future_heart_rate(num_years=2)
            self.assertEqual(mock_show.call_count, 3)  # One for visualize_clusters, two for plt.show in the method

    def test_xml_to_csv(self):
        # Test xml_to_csv function
        xml_to_csv(self.xml_file_path, self.csv_file_path)
        self.assertTrue(os.path.exists(self.csv_file_path))

        # Check if the CSV file has the expected content
        with open(self.csv_file_path, 'r') as csv_file:
            csv_content = csv_file.read()
            self.assertIn('field1,field2', csv_content)
            self.assertIn('value1,value2', csv_content)
            self.assertIn('value3,value4', csv_content)


if __name__ == '__main__':
    unittest.main()
