import json
from datetime import datetime
from collections import defaultdict

# File path
file_path = "/Users/hannahdesoto/PycharmProjects/assignment-5-Information-Retrieval-from-Real-Data-hannah-and-michelle/data/HDhealthdata.json"

# Read data from the file
with open(file_path, "r") as file:
    # Read lines and parse JSON
    lines = file.readlines()
    health_data = [json.loads(line) for line in lines]

# Filter only running stride length data
running_data = [entry for entry in health_data if entry["type"] == "HKQuantityTypeIdentifierRunningStrideLength"]

# Dictionary to store stride lengths grouped by date
stride_lengths_by_day = defaultdict(list)

# Iterate through each running data entry
for entry in running_data:
    # Parse relevant information
    creation_date = datetime.strptime(entry['creationDate'], "%Y-%m-%d %H:%M:%S %z")
    stride_length = float(entry['value'])

    # Group stride lengths by date
    key = creation_date.strftime("%Y-%m-%d")
    stride_lengths_by_day[key].append(stride_length)

# Calculate average stride length for each day
average_stride_lengths = {}
for key, stride_lengths in stride_lengths_by_day.items():
    average_stride_length = sum(stride_lengths) / len(stride_lengths)
    average_stride_lengths[key] = average_stride_length

# Print the results
for key, average_stride_length in average_stride_lengths.items():
    print(f"Date: {key}, Average Stride Length = {average_stride_length:.2f} meters")
