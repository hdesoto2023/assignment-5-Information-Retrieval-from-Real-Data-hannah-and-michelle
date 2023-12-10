import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA


class RestingHeartRateAnalyzer:

    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_data(self):
        self.df = pd.read_csv(self.file_path)

    def preprocess_data(self):
        if self.df is not None:
            self.df['endDate'] = pd.to_datetime(self.df['endDate'])
            if self.df['endDate'].dt.tz is not None and self.df['endDate'].dt.tz == 'UTC':
                self.df['endDate'] = self.df['endDate'].dt.tz_localize('UTC')
            self.df['month_year'] = self.df['endDate'].dt.strftime('%Y-%m')

    def calculate_monthly_average(self):
        if self.df is not None:
            return self.df.groupby('month_year')['value'].mean().reset_index()

    def save_monthly_average_to_file(self, output_file):
        if self.df is not None:
            monthly_average_hr = self.calculate_monthly_average()
            monthly_average_hr.to_csv(output_file, index=False)
            print(f"Monthly average resting heart rates saved to {output_file}")

    def plot_monthly_average(self):
        if self.df is not None:
            monthly_average_hr = self.calculate_monthly_average()
            plt.figure(figsize=(10, 6))
            plt.plot(monthly_average_hr['month_year'], monthly_average_hr['value'], marker='o', linestyle='-', color='b')
            plt.title('Monthly Average Resting Heart Rate')
            plt.xlabel('Month')
            plt.ylabel('Average Resting Heart Rate')
            plt.grid(True)
            plt.show()

    def forecast_next_24_months(self, output_file=None, forecast_file=None):
        if self.df is not None:
            monthly_average_hr = self.calculate_monthly_average()
            monthly_average_hr['month_year'] = pd.to_datetime(monthly_average_hr['month_year'])

            # Fit an ARIMA model
            model = ARIMA(monthly_average_hr['value'], order=(1, 1, 1))
            fit_model = model.fit()

            # Forecast the next 24 months
            forecast_values = fit_model.get_forecast(steps=24).predicted_mean

            # Create a DataFrame for the forecast
            forecast_df = pd.DataFrame({
                'month_year': pd.date_range(monthly_average_hr['month_year'].max() + pd.DateOffset(months=1),
                                            periods=24, freq='M'),
                'value': forecast_values
            })

            # Print the forecast to the terminal
            print("Monthly Average Resting Heart Rate Forecast:")
            print(forecast_df)

            # Save the forecast to a file
            if forecast_file:
                forecast_df.to_csv(forecast_file, index=False)
                print(f"Forecast saved to {forecast_file}")

            # Save the original monthly averages to a file
            if output_file:
                monthly_average_hr.to_csv(output_file, index=False)
                print(f"Original monthly average resting heart rates saved to {output_file}")

            # Plot the original data and the forecast
            plt.figure(figsize=(10, 6))
            plt.plot(monthly_average_hr['month_year'], monthly_average_hr['value'], marker='o', linestyle='-',
                     color='b', label='Original Data')
            plt.plot(forecast_df['month_year'], forecast_df['value'], marker='o', linestyle='--', color='r',
                     label='Forecast')
            plt.title('Monthly Average Resting Heart Rate Forecast')
            plt.xlabel('Month')
            plt.ylabel('Average Resting Heart Rate')
            plt.grid(True)
            plt.legend()
            plt.xticks(rotation=45)
            plt.show()

if __name__ == "__main__":
    output_file = '/Users/hannahdesoto/PycharmProjects/assignment-5-Information-Retrieval-from-Real-Data-hannah-and-michelle/out/HDAvgHR'
    forecast_file = '/Users/hannahdesoto/PycharmProjects/assignment-5-Information-Retrieval-from-Real-Data-hannah-and-michelle/out/HDForecastHR'
    analyzer = RestingHeartRateAnalyzer(
        '/Users/hannahdesoto/PycharmProjects/assignment-5-Information-Retrieval-from-Real-Data-hannah-and-michelle/data/RestingHeartRate.csv')
    analyzer.load_data()
    analyzer.preprocess_data()
    analyzer.plot_monthly_average()
    analyzer.forecast_next_24_months(output_file, forecast_file)
