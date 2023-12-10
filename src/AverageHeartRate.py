import pandas as pd
import matplotlib.pyplot as plt

# Load your resting heart rate data from a CSV file
# Replace 'your_data.csv' with the actual file path or URL of your data
file_path = ('/Users/michellejee/Desktop/assignment-5-Information-Retrieval-from-Real-Data-hannah-and-michelle/data/'
             'RestingHeartRate.csv')
df = pd.read_csv(file_path)
print(df.head())

# Convert the 'endDate' column to datetime if not already datetime
df['endDate'] = pd.to_datetime(df['endDate'])

# Ensure 'endDate' is tz-aware (assuming it's already in UTC, modify accordingly)
if df['endDate'].dt.tz is not None and df['endDate'].dt.tz == 'UTC':
    df['endDate'] = df['endDate'].dt.tz_localize('UTC')

# Calculate the average resting heart rate for each month
monthly_average_hr = df.groupby(df['endDate'].dt.to_period('M')).agg({'value': 'mean'}).reset_index()

# Plotting the data
plt.figure(figsize=(10, 6))
plt.plot(monthly_average_hr['endDate'].dt.to_timestamp(), monthly_average_hr['value'], marker='o', linestyle='-', color='b')
plt.title('Monthly Average Resting Heart Rate')
plt.xlabel('Month')
plt.ylabel('Average Resting Heart Rate')
plt.grid(True)
plt.show()