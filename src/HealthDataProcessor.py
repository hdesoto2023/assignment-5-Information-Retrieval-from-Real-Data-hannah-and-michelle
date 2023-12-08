import json
from datetime import datetime
from collections import OrderedDict


class DistanceSwamProcessor:

    def __init__(self, file_path):
        self.file_path = file_path
        self.health_data = self._read_health_data()

    def _read_health_data(self):
        # Reads health data from a JSON file and returns a list of entries
        with open(self.file_path, "r") as file:
            lines = file.readlines()
            health_data = [json.loads(line) for line in lines]
        return health_data

    def _filter_distance_swimming(self):
        # This filters jsut the swimming distance data from health data
        return [entry for entry in self.health_data if entry["type"] == "HKQuantityTypeIdentifierDistanceSwimming"]

    def _process_and_print(self, process_function, label):
        # Processes the data given the specific distance processor
        processed_data = process_function()
        for date, value in processed_data.items():
            print(f"{label}: {date}, Value: {value}")

    def process_yards_per_day(self):
        yards_per_day = {}

        for entry in self._filter_distance_swimming():
            creation_date = datetime.strptime(entry["creationDate"], "%Y-%m-%d %H:%M:%S %z")
            date_key = creation_date.strftime("%Y-%m-%d")

            if date_key not in yards_per_day:
                yards_per_day[date_key] = 0

            yards_per_day[date_key] += float(entry["value"])

        return yards_per_day

    def process_yards_per_week(self):
        yards_per_week = {}

        for entry in self._filter_distance_swimming():
            creation_date = datetime.strptime(entry["creationDate"], "%Y-%m-%d %H:%M:%S %z")
            week_key = creation_date.isocalendar()[1]  # Get ISO week number

            if week_key not in yards_per_week:
                yards_per_week[week_key] = 0

            yards_per_week[week_key] += float(entry["value"])

        return yards_per_week

    def process_yards_per_month(self):
        yards_per_month = OrderedDict()

        for entry in self._filter_distance_swimming():
            creation_date = datetime.strptime(entry["creationDate"], "%Y-%m-%d %H:%M:%S %z")
            month_key = creation_date.strftime("%B %Y")  # Get full month name and year

            if month_key not in yards_per_month:
                yards_per_month[month_key] = 0

            yards_per_month[month_key] += float(entry["value"])

        return yards_per_month

    def analyze_data(self):
        # Process and print yards per day
        self._process_and_print(self.process_yards_per_day, "Date")

        # Process and print yards per week
        self._process_and_print(self.process_yards_per_week, "Week")

        # Process and print yards per month
        self._process_and_print(self.process_yards_per_month, "Month")


file_path = "/Users/hannahdesoto/PycharmProjects/assignment-5-Information-Retrieval-from-Real-Data-hannah-and-michelle/data/HDhealthdata.json"
health_data_processor = DistanceSwamProcessor(file_path)
health_data_processor.analyze_data()


