
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

class HeartRateAnalyzer:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self.features = None
        self.features_standardized = None
        self.kmeans = None
        self.model = None

    def preprocess_data(self):
        # convert timestamps to datetime objects
        self.df['creationDate'] = pd.to_datetime(self.df['creationDate'])
        self.df['startDate'] = pd.to_datetime(self.df['startDate'])
        self.df['endDate'] = pd.to_datetime(self.df['endDate'])

        self.df['duration'] = (self.df['endDate'] - self.df['startDate']).dt.total_seconds() / 60
        self.df['time_of_day'] = self.df['startDate'].dt.hour + self.df['startDate'].dt.minute / 60

    def cluster_data(self, num_clusters=3):
        self.features = self.df[['value', 'duration', 'time_of_day']]
        scaler = StandardScaler()
        self.features_standardized = scaler.fit_transform(self.features)

        self.kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        self.df['cluster'] = self.kmeans.fit_predict(self.features_standardized)

    def visualize_clusters(self):
        plt.scatter(self.df['startDate'], self.df['value'], c=self.df['cluster'], cmap='viridis')
        plt.xlabel('Date')
        plt.ylabel('Resting Heart Rate (count/min)')
        plt.title('Resting Heart Rate Clusters Over Time')
        plt.show()

    def train_regression_model(self):
        self.df['days_since_start'] = (self.df['startDate'] - self.df['startDate'].min()).dt.days
        X_train, X_test, y_train, y_test = train_test_split(
            self.df[['days_since_start', 'cluster']], self.df['value'], test_size=0.2, random_state=42
        )
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)

        mse = mean_squared_error(y_test, y_pred)
        print(f'Mean Squared Error: {mse}')

    def predict_future_heart_rate(self, num_years=20):
        # Group data by month and calculate the average resting heart rate
        monthly_avg_heart_rate = self.df.groupby(self.df['startDate'].dt.to_period("M"))['value'].mean().reset_index()

        # Print monthly averages to terminal
        print("Monthly Heart Rate Averages:")
        print(monthly_avg_heart_rate[['startDate', 'value']])

        # Plot the average resting heart rate by month
        plt.plot(monthly_avg_heart_rate['startDate'].dt.to_timestamp(), monthly_avg_heart_rate['value'], marker='o')
        plt.xlabel('Month')
        plt.ylabel('Average Resting Heart Rate (count/min)')
        plt.title('Average Resting Heart Rate by Month')
        plt.show()

        # Predict resting heart rate for the next 20 years
        days_future = pd.DataFrame({
            'days_since_start': range(self.df['days_since_start'].max() + 1,
                                      self.df['days_since_start'].max() + num_years * 365 + 1),
            'cluster': self.kmeans.predict(self.features_standardized.mean(axis=0).reshape(1, -1))
        })
        future_predictions = self.model.predict(days_future[['days_since_start', 'cluster']])

        # Group the future data by month and calculate the average resting heart rate
        future_avg_heart_rate = days_future.groupby(
            pd.to_datetime(days_future['days_since_start'], unit='D').dt.to_period("M")
        )['cluster'].count().reset_index()

        # Print predicted averages to terminal for each month of the next five years
        print("\nPredicted Monthly Heart Rate Averages for the Next 5 Years:")
        for idx, row in future_avg_heart_rate.iterrows():
            month_year = row['days_since_start'].strftime('%B %Y')
            predicted_value = future_predictions[idx]
            print(f"{month_year}: {predicted_value}")

        # Visualize predictions
        plt.plot(self.df['startDate'], self.df['value'], label='Actual Data', marker='o')
        plt.plot(
            pd.to_datetime(future_avg_heart_rate['days_since_start'], unit='D').dt.to_timestamp(),
            future_predictions, label='Predictions', linestyle='--', marker='o'
        )
        plt.xlabel('Days Since Start')
        plt.ylabel('Resting Heart Rate (count/min)')
        plt.title('Resting Heart Rate Prediction for the Next 20 Years')
        plt.legend()
        plt.show()


# class WorkoutDataClusterer:
#     def __init__(self, file_path):
#         self.df = pd.read_csv(file_path)
#         self.features = None
#         self.features_standardized = None
#         self.kmeans = None
#
#     def preprocess_data(self):
#         # convert timestamps to datetime objects
#         self.df['startDate'] = pd.to_datetime(self.df['startDate'])
#         self.df['endDate'] = pd.to_datetime(self.df['endDate'])
#
#         # Extract month and year information
#         self.df['month'] = self.df['startDate'].dt.month
#         self.df['year'] = self.df['startDate'].dt.year
#
#         self.df['duration'] = (self.df['endDate'] - self.df['startDate']).dt.total_seconds() / 60
#
#     def cluster_data(self, num_clusters=3):
#         self.features = self.df[['year', 'month', 'duration']]
#         scaler = StandardScaler()
#         self.features_standardized = scaler.fit_transform(self.features)
#
#         self.kmeans = KMeans(n_clusters=num_clusters, random_state=42)
#         self.df['cluster'] = self.kmeans.fit_predict(self.features_standardized)
#
#     def visualize_clusters(self):
#         # Plot the clusters
#         plt.scatter(self.df['startDate'], self.df['duration'], c=self.df['cluster'], cmap='viridis')
#         plt.xlabel('Date')
#         plt.ylabel('Workout Duration (min)')
#         plt.title('Workout Duration Clusters Over Time')
#         plt.show()
#
# # Provide the file path to your workout data CSV file
# workout_file_path = '/Users/hannahdesoto/PycharmProjects/assignment-5-Information-Retrieval-from-Real-Data-hannah-and-michelle/data/Workout.csv'
# # Create an instance of WorkoutDataClusterer
# workout_clusterer = WorkoutDataClusterer(workout_file_path)

# # Perform clustering
# workout_clusterer.preprocess_data()
# workout_clusterer.cluster_data()
# workout_clusterer.visualize_clusters()

# Provide the file path to your CSV file
file_path = '/Users/hannahdesoto/PycharmProjects/assignment-5-Information-Retrieval-from-Real-Data-hannah-and-michelle/data/RestingHeartRate.csv'
# Create an instance of HeartRateAnalyzer
analyzer = HeartRateAnalyzer(file_path)

# Perform analysis
analyzer.preprocess_data()
analyzer.cluster_data()
analyzer.visualize_clusters()
analyzer.train_regression_model()
analyzer.predict_future_heart_rate()
