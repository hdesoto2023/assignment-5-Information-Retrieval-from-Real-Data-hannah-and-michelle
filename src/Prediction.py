import pandas as pd
import matplotlib.pyplot as plt
import xmltodatabase
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


class RestingHeartRatePredictor:
    def __init__(self, file_path):
        try:
            self.df = pd.read_csv(file_path)
        except pd.errors.ParserError:
            print("Error reading CSV file. Skipping lines with incorrect number of fields.")
            self.df = pd.read_csv(file_path, error_bad_lines=False)

    def preprocess_data(self):
        # Convert timestamps to datetime objects
        self.df['creationDate'] = pd.to_datetime(self.df['creationDate'])

        # Extract month and year information
        self.df['month'] = self.df['creationDate'].dt.month
        self.df['year'] = self.df['creationDate'].dt.year

    def cluster_data(self, num_clusters=3):
        self.features = self.df[['value']]
        scaler = StandardScaler()
        self.features_standardized = scaler.fit_transform(self.features)

        self.kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        self.df['cluster'] = self.kmeans.fit_predict(self.features_standardized)

    def visualize_clusters(self):
        plt.scatter(self.df['creationDate'], self.df['value'], c=self.df['cluster'], cmap='viridis')
        plt.xlabel('Date')
        plt.ylabel('Resting Heart Rate (count/min)')
        plt.title('Resting Heart Rate Clusters Over Time')
        plt.show()

    def train_regression_model(self):
        X_train, X_test, y_train, y_test = train_test_split(
            self.df[['month', 'year', 'cluster']], self.df['value'], test_size=0.2, random_state=42
        )
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)

        mse = mean_squared_error(y_test, y_pred)
        print(f'Mean Squared Error: {mse}')

    def analyze_resting_heart_rate_pattern(csv_file):
        # Read CSV file into a DataFrame
        df = pd.read_csv(csv_file)

        # Convert 'Date' column to datetime
        df['Date'] = pd.to_datetime(df['Date'])

        # Extract month and year information
        df['Month'] = df['Date'].dt.month
        df['Year'] = df['Date'].dt.year

        # Group by month and calculate the average resting heart rate
        monthly_avg_heart_rate = df.groupby(['Year', 'Month'])['RestingHeartRate'].mean().reset_index()

        # Plot the average resting heart rate by month
        plt.figure(figsize=(10, 6))
        plt.plot(monthly_avg_heart_rate['Month'], monthly_avg_heart_rate['RestingHeartRate'], marker='o')
        plt.xlabel('Month')
        plt.ylabel('Average Resting Heart Rate')
        plt.title('Average Resting Heart Rate by Month')
        plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        plt.grid(True)
        plt.show()

    def predict_future_heart_rate(self, num_years=2):
        # Group data by month and calculate the average resting heart rate
        monthly_avg_heart_rate = self.df.groupby(['year', 'month'])['value'].mean().reset_index()

        # Plot the average resting heart rate by month
        plt.plot(monthly_avg_heart_rate['month'], monthly_avg_heart_rate['value'], marker='o')
        plt.xlabel('Month')
        plt.ylabel('Average Resting Heart Rate (count/min)')
        plt.title('Average Resting Heart Rate by Month')
        plt.show()

        # Predict resting heart rate for the next 2 years
        future_data = pd.DataFrame({
            'month': range(1, 13) * num_years,
            'year': [2022 + i for i in range(num_years)] * 12,
            'cluster': self.kmeans.predict(self.features_standardized.mean(axis=0).reshape(1, -1))
        })
        future_predictions = self.model.predict(future_data[['month', 'year', 'cluster']])

        # Group the future data by month and calculate the average resting heart rate
        future_avg_heart_rate = future_data.groupby(['year', 'month'])['cluster'].count().reset_index()

        # Print predicted averages for each month of the next two years
        print("\nPredicted Monthly Heart Rate Averages for the Next 2 Years:")
        for idx, row in future_avg_heart_rate.iterrows():
            month_year = f"{int(row['year'])}-{int(row['month']):02d}"
            predicted_value = future_predictions[idx]
            print(f"{month_year}: {predicted_value}")

        # Visualize predictions
        plt.plot(self.df['creationDate'], self.df['value'], label='Actual Data', marker='o')
        plt.plot(
            future_avg_heart_rate['month'] + future_avg_heart_rate['year'] * 100,
            future_predictions, label='Predictions', linestyle='--', marker='o'
        )
        plt.xlabel('Month-Year')
        plt.ylabel('Resting Heart Rate (count/min)')
        plt.title('Resting Heart Rate Prediction for the Next 2 Years')
        plt.legend()
        plt.show()


# Provide the file path to your CSV file
file_path = '/Users/michellejee/Desktop/assignment-5-Information-Retrieval-from-Real-Data-hannah-and-michelle/data/apple_health_export/export.xml'
# Create an instance of RestingHeartRatePredictor
predictor = RestingHeartRatePredictor(file_path)

if __name__ == "__main__":
    # Replace 'RestingHeartRate.csv' with the actual path to your CSV file
    file_path = 'RestingHeartRate.csv'

    predictor = RestingHeartRatePredictor(file_path)

# Perform analysis
predictor.preprocess_data()
predictor.cluster_data()
predictor.visualize_clusters()
predictor.train_regression_model()
predictor.predict_future_heart_rate()

def xml_to_dataframe(self, xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extract data from XML and convert to DataFrame
    data_list = []
    for record in root.findall('.//record'):
        data_list.append({
            'creationDate': record.find('creationDate').text,
            'value': float(record.find('value').text)
        })

    df = pd.DataFrame(data_list)

    # Convert 'creationDate' to datetime
    df['creationDate'] = pd.to_datetime(df['creationDate'])

    return df

if __name__ == "__main__":
    # Replace 'input.xml' with the path to your XML file
    xml_file_path = 'input.xml'

    # Replace 'output.csv' with the desired CSV file name
    csv_file_path = 'output.csv'

    xml_to_csv(xml_file_path, csv_file_path)