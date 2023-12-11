import xml.etree.ElementTree as ET
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from google.cloud import storage
import os

class XMLDataExtractor:
    def __init__(self, xml_file_path):
        self.xml_file_path = xml_file_path
        self.root = None
        self.target_identifiers = ["HKQuantityTypeIdentifierRestingHeartRate", "HKQuantityTypeIdentifierBodyMass",
                                   "HKQuantityTypeIdentifierAppleExerciseTime", "HKQuantityTypeIdentifierBasalEnergyBurned",
                                   "HKQuantityTypeIdentifierActiveEnergyBurned", "HKQuantityTypeIdentifierDistanceSwimming",
                                   "HKQuantityTypeIdentifierDistanceWalkingRunning"]

        # Initialize dictionaries to store data
        self.heart_rate_data = {}
        self.body_mass_data = {}
        self.exercise_time_data = {}
        self.basal_energy_data = {}
        self.active_energy_data = {}
        self.distance_swimming_data = {}
        self.distance_walking_running_data = {}

    def extract_data(self):
        tree = ET.parse(self.xml_file_path)
        self.root = tree.getroot()

        # goes through each line and extracts the desired data
        for record in self.root.findall(".//Record"):
            record_type = record.get("type")
            if record_type in self.target_identifiers:
                value = float(record.get("value"))  # Assuming the value is numeric; convert to the appropriate type
                start_time = record.get("startDate")

                # Store data in respective dictionaries
                if record_type == "HKQuantityTypeIdentifierRestingHeartRate":
                    self.heart_rate_data[start_time] = value
                elif record_type == "HKQuantityTypeIdentifierBodyMass":
                    self.body_mass_data[start_time] = value
                elif record_type == "HKQuantityTypeIdentifierAppleExerciseTime":
                    self.exercise_time_data[start_time] = value
                elif record_type == "HKQuantityTypeIdentifierBasalEnergyBurned":
                    self.basal_energy_data[start_time] = value
                elif record_type == "HKQuantityTypeIdentifierActiveEnergyBurned":
                    self.active_energy_data[start_time] = value
                elif record_type == "HKQuantityTypeIdentifierDistanceSwimming":
                    self.distance_swimming_data[start_time] = value
                elif record_type == "HKQuantityTypeIdentifierDistanceWalkingRunning":
                    self.distance_walking_running_data[start_time] = value

    def download_from_gcs(bucket_name, source_blob_name, destination_file_name):
        """Downloads a blob from the bucket."""
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)

        home_directory = os.path.expanduser("~")
        destination_file_path = os.path.join(home_directory, destination_file_name)

        blob.download_to_filename(destination_file_path)

    bucket_name = "heart-export"
    source_blob_name = "heart-export/export.xml"  # Path within the bucket
    destination_file_name = "/Users/michellejee/Desktop/assignment-5-Information-Retrieval-from-Real-Data-hannah-and-michelle/data/export.xml"

    download_from_gcs(bucket_name, source_blob_name, destination_file_name)


class RestingHeartRateAnalyzer:
    def __init__(self, xml_data_extractor):
        self.xml_data_extractor = xml_data_extractor
        self.df = None

    def process_data(self):
        # converts the extracted data into a DataFrama using pandas
        data = {
            'start_time': list(self.xml_data_extractor.heart_rate_data.keys()), # grabs the key values of the heart rate dictionary  = time
            'heart_rate': list(self.xml_data_extractor.heart_rate_data.values()) # grabs the values of the heart rate dictionary = hr
        }
        self.df = pd.DataFrame(data)
        self.df['start_time'] = pd.to_datetime(self.df['start_time'], errors='coerce')

        # drops any rows without a timestamp
        self.df = self.df.dropna(subset=['start_time'])

    def calculate_monthly_average(self):
        if self.df is not None:
            result = self.df.copy()
            result['start_time'] = result['start_time'].dt.to_period('M')
            result = result.groupby('start_time')['heart_rate'].mean().reset_index()
            result['heart_rate'] = result['heart_rate'].astype(float)  # Ensure the data type is consistent
            return result

    def plot_monthly_average(self):
        if self.df is not None:
            monthly_average_hr = self.calculate_monthly_average()
            plt.figure(figsize=(10, 6))
            plt.plot(monthly_average_hr['start_time'].dt.to_timestamp(), monthly_average_hr['heart_rate'],
                     marker='o', linestyle='-', color='b')
            plt.title('Monthly Average Resting Heart Rate')
            plt.xlabel('Month')
            plt.ylabel('Average Resting Heart Rate')
            plt.grid(True)
            plt.show()

    # uses ARIMA (AutoRegressive Integrated Moving Average)
    # time series forecasting to predict the next 24 months of resting heart rate
    # it also plots the original data and the forecasted values.
    def forecast_next_24_months(self, output_file=None, forecast_file=None):
        if self.df is not None:
            monthly_average_hr = self.calculate_monthly_average()
            monthly_average_hr['start_time'] = monthly_average_hr['start_time'].dt.to_timestamp()

            model = ARIMA(monthly_average_hr['heart_rate'], order=(1, 1, 1))
            fit_model = model.fit()

            forecast_values = fit_model.get_forecast(steps=24).predicted_mean

            forecast_df = pd.DataFrame({
                'start_time': pd.date_range(monthly_average_hr['start_time'].max() + pd.DateOffset(months=1),
                                            periods=24, freq='M'),
                'heart_rate': forecast_values
            })

            print("Monthly Average Resting Heart Rate Forecast:")
            print(forecast_df)

            if forecast_file:
                forecast_df.to_csv(forecast_file, index=False)
                print(f"Forecast saved to {forecast_file}")

            if output_file:
                monthly_average_hr.to_csv(output_file, index=False)
                print(f"Original monthly average resting heart rates saved to {output_file}")

            plt.figure(figsize=(10, 6))
            plt.plot(monthly_average_hr['start_time'], monthly_average_hr['heart_rate'],
                     marker='o', linestyle='-', color='b', label='Original Data')
            plt.plot(forecast_df['start_time'], forecast_df['heart_rate'], marker='o', linestyle='--', color='r',
                     label='Forecast')
            plt.title('Monthly Average Resting Heart Rate Forecast')
            plt.xlabel('Month')
            plt.ylabel('Average Resting Heart Rate')
            plt.grid(True)
            plt.legend()
            plt.xticks(rotation=45)
            plt.show()


if __name__ == "__main__":
    xml_file_path = '/Users/michellejee/Desktop/assignment-5-Information-Retrieval-from-Real-Data-hannah-and-michelle/data/export.xml'
    output_file = '/Users/michellejee/PycharmProjects/assignment-5-Information-Retrieval-from-Real-Data-hannah-and-michelle/out/MeeshMonthlyAvg.csv'
    forecast_file = '/Users/michellejee/PycharmProjects/assignment-5-Information-Retrieval-from-Real-Data-hannah-and-michelle/out/MeeshForecast.csv'

    xml_data_extractor = XMLDataExtractor(xml_file_path)
    xml_data_extractor.extract_data()

    analyzer = RestingHeartRateAnalyzer(xml_data_extractor)
    analyzer.process_data()
    analyzer.plot_monthly_average()
    analyzer.forecast_next_24_months(output_file, forecast_file)

