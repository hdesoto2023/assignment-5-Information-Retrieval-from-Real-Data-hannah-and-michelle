import json
from collections import OrderedDict
from datetime import datetime


def process_yards_per_day(data):
    yards_per_day = {}

    for entry in data:
        creation_date = datetime.strptime(entry["creationDate"], "%Y-%m-%d %H:%M:%S %z")
        date_key = creation_date.strftime("%Y-%m-%d")

        if date_key not in yards_per_day:
            yards_per_day[date_key] = 0

        yards_per_day[date_key] += float(entry["value"])

    return yards_per_day

def process_yards_per_week(data):
    yards_per_week = {}

    for entry in data:
        creation_date = datetime.strptime(entry["creationDate"], "%Y-%m-%d %H:%M:%S %z")
        week_key = creation_date.isocalendar()[1]  # Get ISO week number

        if week_key not in yards_per_week:
            yards_per_week[week_key] = 0

        yards_per_week[week_key] += float(entry["value"])

    return yards_per_week

def process_yards_per_month(data):
    yards_per_month = OrderedDict()

    for entry in data:
        creation_date = datetime.strptime(entry["creationDate"], "%Y-%m-%d %H:%M:%S %z")
        month_key = creation_date.strftime("%B %Y")  # Get full month name and year

        if month_key not in yards_per_month:
            yards_per_month[month_key] = 0

        yards_per_month[month_key] += float(entry["value"])

    return yards_per_month



# File path
file_path = "/Users/hannahdesoto/PycharmProjects/assignment-5-Information-Retrieval-from-Real-Data-hannah-and-michelle/data/HDhealthdata.json"



# Read data from the file
with open(file_path, "r") as file:
    # Read lines and parse JSON
    lines = file.readlines()
    health_data = [json.loads(line) for line in lines]

distance_swam_data = [entry for entry in health_data if entry["type"] == "HKQuantityTypeIdentifierDistanceSwimming"]

# Process stroke count data
distance_swam_per_day = process_yards_per_day(distance_swam_data)

# Print strokes per day
for date, yards in distance_swam_per_day.items():
    print(f"Date: {date}, Yards: {yards}")

# Process strokes per week
yards_per_week = process_yards_per_week(distance_swam_data)

# Print strokes per week
for week, yards in yards_per_week.items():
    print(f"Week: {week}, Yards: {yards}")

# Process strokes per month
monthly_yards = process_yards_per_month(distance_swam_data)

# Print strokes per month
for month, yards in monthly_yards.items():
    print(f"Month: {month}, Yards: {yards}")
