import pandas as pd
import json
import re

# Define regex patterns for common units
UNIT_PATTERNS = {
    "cmm": re.compile(r"/cmm"),
    "gm/dl": re.compile(r"(gm/dl|g/dl)", re.IGNORECASE),
    "109/L": re.compile(r"10\^?9/L"),
    "%": re.compile(r"%"),
}

# Conversion factors for matched units
CONVERSION_FACTORS = {
    "cmm": 1e-6,  
    "gm/dl": 1,   
    "109/L": 1,   
    "%": 1        
}

def standardize_unit(unit):
    """
    Standardize a unit string using regex patterns.
    
    Args:
        unit (str): The detected unit string.
    
    Returns:
        str: Standardized unit or None if no match.
    """
    for standard_unit, pattern in UNIT_PATTERNS.items():
        if pattern.search(unit):
            return standard_unit
    print(f"Unknown unit: {unit}")
    return None

def process_unit_conversion_with_regex(value, detected_unit, target_unit):
    """
    Convert a value from detected_unit to target_unit using regex.

    Args:
        value (float): The numerical value to convert.
        detected_unit (str): Detected unit of the value.
        target_unit (str): Target unit to convert to.

    Returns:
        float: Converted value or None if conversion not possible.
    """
    # Standardize units
    standardized_unit = standardize_unit(detected_unit)
    if not standardized_unit:
        return None  # Unknown unit

    if standardized_unit == target_unit:
        print(f"No conversion needed for {value} {detected_unit}")
        return value

    # Apply conversion factor
    if standardized_unit in CONVERSION_FACTORS:
        conversion_factor = CONVERSION_FACTORS[standardized_unit]
        converted_value = value * conversion_factor
        print(f"Converting {value} {detected_unit} to {converted_value} {target_unit}")
        return converted_value
    else:
        print(f"Conversion factor not defined for unit: {detected_unit}")
        return None


# Load target units from JSON
with open("datasets/unit_conversion_datasets/unit.json", "r") as f:
    target_units = json.load(f)

# Load units data from CSV
units_df = pd.read_csv('unit_conversion_module/unit_conv(from phrase detected).csv', index_col=0)

# Initialize the final data packet
final_data_packet = {}

# print(units_df)
for index, row in units_df.iterrows():
    final_data_packet[index] = process_unit_conversion_with_regex(row["Results"], row["Unit"], target_units.get(index))

print(final_data_packet)
