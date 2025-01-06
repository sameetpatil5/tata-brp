import pandas as pd
import json
from unit_convert_parser_module.unit_convert_parser import convert_unit

# Load target units from JSON
with open("datasets/unit_conversion_datasets/units.json", "r") as f:
    target_units = json.load(f)

# Load units data from CSV
units_df = pd.read_csv('unit_conversion_module/unit_conv(from phrase detected).csv', index_col=0)

# Initialize the final data packet
final_data_packet = {}

# Iterate through target units to form the data packet
for key, target_unit in target_units.items():
    try:
        # Check if the key exists in the DataFrame
        unit_row = units_df.loc[key]
        detected_unit = unit_row.Unit
        detected_result = unit_row.Results

        # Compare detected unit with target unit
        if detected_unit != target_unit:
            print(f"Unit mismatch for '{key}': Detected '{detected_unit}', Expected '{target_unit}'")
            # Placeholder for unit conversion logic
            final_result = 0
        else:
            final_result = detected_result

        # Add to final data packet
        final_data_packet[key] = final_result

    except KeyError:
        # Handle missing keys
        print(f"Key not found: {key}")
        final_data_packet[key] = "missing"

# Print the final data packet
print("Final Data Packet:", final_data_packet)
