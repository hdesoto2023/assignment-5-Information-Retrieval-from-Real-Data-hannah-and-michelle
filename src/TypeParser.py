import json

# File path
file_path = "/Users/hannahdesoto/PycharmProjects/assignment-5-Information-Retrieval-from-Real-Data-hannah-and-michelle/data/HDhealthdata.json"

# Read data from the file
with open(file_path, "r") as file:
    # Read lines and parse JSON
    lines = file.readlines()
    health_data = [json.loads(line) for line in lines]

# Extract unique types
unique_types = set(entry["type"] for entry in health_data)



# Print all unique types
print("Unique Types:")
for entry_type in unique_types:
    print(entry_type)
