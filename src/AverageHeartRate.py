import pandas as pd
import matplotlib.pyplot as plt

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

if __name__ == "__main__":
    analyzer = RestingHeartRateAnalyzer('/Users/michellejee/Desktop/assignment-5-Information-Retrieval-from-Real-Data-hannah-and-michelle/data/RestingHeartRate.csv')
    analyzer.load_data()
    analyzer.preprocess_data()
    analyzer.plot_monthly_average()
