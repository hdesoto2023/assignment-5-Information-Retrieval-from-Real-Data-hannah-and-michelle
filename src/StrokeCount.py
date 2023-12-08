import json
from datetime import datetime

def process_stroke_count_per_day(data):
    strokes_per_day = {}

    for entry in data:
        creation_date = datetime.strptime(entry["creationDate"], "%Y-%m-%d %H:%M:%S %z")
        date_key = creation_date.strftime("%Y-%m-%d")

        if date_key not in strokes_per_day:
            strokes_per_day[date_key] = 0

        strokes_per_day[date_key] += int(entry["value"])

    return strokes_per_day

def process_stroke_count_per_week(data):
    strokes_per_week = {}

    for entry in data:
        creation_date = datetime.strptime(entry["creationDate"], "%Y-%m-%d %H:%M:%S %z")
        week_key = creation_date.isocalendar()[1]  # Get ISO week number

        if week_key not in strokes_per_week:
            strokes_per_week[week_key] = 0

        strokes_per_week[week_key] += int(entry["value"])

    return strokes_per_week

def process_stroke_count_per_month(data):
    strokes_per_month = {}

    for entry in data:
        creation_date = datetime.strptime(entry["creationDate"], "%Y-%m-%d %H:%M:%S %z")
        month_key = creation_date.strftime("%B %Y")  # Get full month name and year

        if month_key not in strokes_per_month:
            strokes_per_month[month_key] = 0

        strokes_per_month[month_key] += int(entry["value"])

    return strokes_per_month


# File path
file_path = "/Users/hannahdesoto/PycharmProjects/assignment-5-Information-Retrieval-from-Real-Data-hannah-and-michelle/data/HDhealthdata.json"

# Read data from the file
with open(file_path, "r") as file:
    # Read lines and parse JSON
    lines = file.readlines()
    health_data = [json.loads(line) for line in lines]

# Filter only swimming stroke count data
stroke_count_data = [entry for entry in health_data if entry["type"] == "HKQuantityTypeIdentifierSwimmingStrokeCount"]

# Process stroke count data
strokes_per_day = process_stroke_count_per_day(stroke_count_data)

# Print strokes per day
for date, strokes in strokes_per_day.items():
    print(f"Date: {date}, Strokes: {strokes}")

# Process strokes per week
strokes_per_week = process_stroke_count_per_week(stroke_count_data)

# Print strokes per week
for week, strokes in strokes_per_week.items():
    print(f"Week: {week}, Strokes: {strokes}")

# Process strokes per month
strokes_per_month = process_stroke_count_per_month(stroke_count_data)

# Print strokes per month
for month, strokes in strokes_per_month.items():
    print(f"Month: {month}, Strokes: {strokes}")

