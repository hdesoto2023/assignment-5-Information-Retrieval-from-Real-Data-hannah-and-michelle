import xml.etree.ElementTree as ET

xml_file_path = '/Users/hannahdesoto/PycharmProjects/assignment-5-Information-Retrieval-from-Real-Data-hannah-and-michelle/data/hannahHealthDataexport.xml'

tree = ET.parse(xml_file_path)
root = tree.getroot()

# Define the HKQuantityTypeIdentifiers you want to extract
target_identifiers = ["HKQuantityTypeIdentifierRestingHeartRate", "HKQuantityTypeIdentifierBodyMass",
                      "HKQuantityTypeIdentifierAppleExerciseTime", "HKQuantityTypeIdentifierBasalEnergyBurned",
                      "HKQuantityTypeIdentifierActiveEnergyBurned", "HKQuantityTypeIdentifierDistanceSwimming",
                      "HKQuantityTypeIdentifierDistanceWalkingRunning"]

# Initialize dictionaries to store data
heart_rate_data = {}
body_mass_data = {}
exercise_time_data = {}
basal_energy_data = {}
active_energy_data = {}
distance_swimming_data = {}
distance_walking_running_data = {}

# Iterate through the 'Record' elements and extract the ones with the desired identifiers
for record in root.findall(".//Record"):
    record_type = record.get("type")
    if record_type in target_identifiers:
        value = float(record.get("value"))  # Assuming the value is numeric; convert to the appropriate type
        start_time = record.get("startDate")

        # Store data in respective dictionaries
        if record_type == "HKQuantityTypeIdentifierRestingHeartRate":
            heart_rate_data[start_time] = value
        elif record_type == "HKQuantityTypeIdentifierBodyMass":
            body_mass_data[start_time] = value
        elif record_type == "HKQuantityTypeIdentifierAppleExerciseTime":
            exercise_time_data[start_time] = value
        elif record_type == "HKQuantityTypeIdentifierBasalEnergyBurned":
            basal_energy_data[start_time] = value
        elif record_type == "HKQuantityTypeIdentifierActiveEnergyBurned":
            active_energy_data[start_time] = value
        elif record_type == "HKQuantityTypeIdentifierDistanceSwimming":
            distance_swimming_data[start_time] = value
        elif record_type == "HKQuantityTypeIdentifierDistanceWalkingRunning":
            distance_walking_running_data[start_time] = value

# Now you have dictionaries with organized data, and you can perform further analysis.
# For example, you can calculate average values, plot graphs, etc., based on your analysis needs.
