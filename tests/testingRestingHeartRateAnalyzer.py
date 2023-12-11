import unittest
import xml.etree.ElementTree as ET
import pandas as pd
import os
from src.MichelleRestingHeartRateAnalyzer import *


class TestXMLDataExtractor(unittest.TestCase):
    def setUp(self):
        # Create a sample XML file for testing
        self.sample_xml = """
        <HealthData>
            <Record type="HKQuantityTypeIdentifierRestingHeartRate" value="70" startDate="2023-01-01"/>
            <Record type="HKQuantityTypeIdentifierRestingHeartRate" value="75" startDate="2023-02-01"/>
            <Record type="HKQuantityTypeIdentifierRestingHeartRate" value="80" startDate="2023-03-01"/>
        </HealthData>
        """

        with open('test.xml', 'w') as file:
            file.write(self.sample_xml)

        self.extractor = XMLDataExtractor('test.xml')

    def tearDown(self):
        # Clean up the created XML file
        import os
        os.remove('test.xml')

    def test_initialization(self):
        self.assertEqual(self.extractor.xml_file_path, 'test.xml')
        self.assertIsNone(self.extractor.root)
        self.assertListEqual(self.extractor.target_identifiers,
                             ["HKQuantityTypeIdentifierRestingHeartRate", "HKQuantityTypeIdentifierBodyMass",
                              "HKQuantityTypeIdentifierAppleExerciseTime", "HKQuantityTypeIdentifierBasalEnergyBurned",
                              "HKQuantityTypeIdentifierActiveEnergyBurned", "HKQuantityTypeIdentifierDistanceSwimming",
                              "HKQuantityTypeIdentifierDistanceWalkingRunning"])

        self.assertDictEqual(self.extractor.heart_rate_data, {})
        self.assertDictEqual(self.extractor.body_mass_data, {})
        self.assertDictEqual(self.extractor.exercise_time_data, {})
        self.assertDictEqual(self.extractor.basal_energy_data, {})
        self.assertDictEqual(self.extractor.active_energy_data, {})
        self.assertDictEqual(self.extractor.distance_swimming_data, {})
        self.assertDictEqual(self.extractor.distance_walking_running_data, {})

    def test_extract_data(self):
        self.extractor.extract_data()

        # Check if data has been extracted correctly
        expected_heart_rate_data = {'2023-01-01': 70.0, '2023-02-01': 75.0, '2023-03-01': 80.0}
        self.assertDictEqual(self.extractor.heart_rate_data, expected_heart_rate_data)

        # Add more assertions for other data dictionaries if needed


class TestRestingHeartRateAnalyzer(unittest.TestCase):
    def setUp(self):
        # Create a sample XML file for testing
        sample_xml = """
        <HealthData>
            <Record type="HKQuantityTypeIdentifierRestingHeartRate" value="70" startDate="2023-01-01"/>
            <Record type="HKQuantityTypeIdentifierRestingHeartRate" value="75" startDate="2023-02-01"/>
            <Record type="HKQuantityTypeIdentifierRestingHeartRate" value="80" startDate="2023-03-01"/>
        </HealthData>
        """

        with open('test.xml', 'w') as file:
            file.write(sample_xml)

        xml_data_extractor = XMLDataExtractor('test.xml')
        xml_data_extractor.extract_data()

        self.analyzer = RestingHeartRateAnalyzer(xml_data_extractor)

    def tearDown(self):
        # Clean up the created XML file
        os.remove('test.xml')

    def test_initialization(self):
        self.assertEqual(self.analyzer.xml_data_extractor.xml_file_path, 'test.xml')
        self.assertIsNone(self.analyzer.df)

    def test_process_data(self):
        self.analyzer.process_data()
        self.assertIsNotNone(self.analyzer.df)
        self.assertEqual(len(self.analyzer.df), 3)  # Assuming three records in the sample XML

    def test_calculate_monthly_average(self):
        self.analyzer.process_data()
        result = self.analyzer.calculate_monthly_average()

        expected_result = pd.DataFrame({
            'start_time': pd.to_datetime(['2023-01-01', '2023-02-01', '2023-03-01']),
            'heart_rate': [70, 75, 80]
        })
        expected_result['start_time'] = expected_result['start_time'].dt.to_period('M')
        expected_result['heart_rate'] = expected_result['heart_rate'].astype(
            float)  # Ensure the data type is consistent
        pd.testing.assert_frame_equal(result, expected_result)


if __name__ == '__main__':
    unittest.main()
