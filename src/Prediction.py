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

    def train_arima_model(self):
        if self.df is not None:
            # Assuming your 'value' column is the heart rate values
            time_series = self.df.set_index('endDate')['value']
            model = ARIMA(time_series, order=(1, 1, 1))  # Adjust order as needed
            fit_model = model.fit()
            return fit_model

    def predict_heart_rate(self, fit_model, num_periods=24):  # Predict next 2 years (24 months)
        if self.df is not None:
            forecast = fit_model.get_forecast(steps=num_periods)
            forecast_index = pd.date_range(self.df['endDate'].max() + pd.DateOffset(1), periods=num_periods, freq='M')
            forecast_values = forecast.predicted_mean.values
            return pd.DataFrame({'endDate': forecast_index, 'value': forecast_values})

if __name__ == "__main__":
    analyzer = RestingHeartRateAnalyzer('/Users/michellejee/Desktop/assignment-5-Information-Retrieval-from-Real-Data-hannah-and-michelle/data/RestingHeartRate.csv')
    analyzer.load_data()
    analyzer.preprocess_data()

    # Train ARIMA model
    fit_model = analyzer.train_arima_model()

    # Save the monthly average resting heart rates to an output file
    output_file = '/path/to/output/average_heart_rates.csv'
    analyzer.save_monthly_average_to_file(output_file)

    # Plot the monthly average resting heart rates
    analyzer.plot_monthly_average()

    # Predict heart rates for the next 2 years
    predictions = analyzer.predict_heart_rate(fit_model, num_periods=24)

    print(predictions)
