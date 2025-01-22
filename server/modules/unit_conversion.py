import pandas as pd
import json
import re

# Define regex patterns for common units
UNIT_PATTERNS = {
    "cmm": re.compile(r"/cmm"),
    "gm/dl": re.compile(r"(gm/dl|g/dl)", re.IGNORECASE),
    "109/L": re.compile(r"10/\^?9/L"),
    "%": re.compile(r"%"),
}

# Conversion factors for matched units
CONVERSION_FACTORS = {
    "cmm": 1e-6,  # Conversion factor for cmm
    "gm/dl": 1,   # Conversion factor for gm/dl (no change)
    "109/L": 1,   # Conversion factor for 10^9/L (no change)
    "%": 1        # Conversion factor for percentage (no change)
}

def standardize_unit(unit: str) -> str:
    """
    Standardize a unit string using regex patterns.

    Args:
        unit (str): The detected unit string.

    Returns:
        str: Standardized unit or None if no match is found.
    """
    for standard_unit, pattern in UNIT_PATTERNS.items():
        if pattern.search(unit):
            return standard_unit
    return None

def process_unit_conversion_with_regex(value: float, detected_unit: str, target_unit: str) -> float:
    """
    Convert a value from detected_unit to target_unit using regex.

    Args:
        value (float): The numerical value to convert.
        detected_unit (str): Detected unit of the value.
        target_unit (str): Target unit to convert to.

    Returns:
        float: Converted value or None if conversion is not possible.
    """
    # Standardize the detected unit
    standardized_unit = standardize_unit(detected_unit)
    if not standardized_unit:
        return None  # Return None for unknown units

    # If units are the same, no conversion is needed
    if standardized_unit == target_unit:
        return value

    # Apply conversion factor if defined
    if standardized_unit in CONVERSION_FACTORS:
        conversion_factor = CONVERSION_FACTORS[standardized_unit]
        converted_value = value * conversion_factor
        return converted_value

    return None

def unit_conversion(units_df: pd.DataFrame) -> dict:
    """
    Convert units in a DataFrame using regex patterns and target unit mappings.

    Args:
        units_df (pd.DataFrame): DataFrame containing 'Test', 'Result', and 'Unit' columns.

    Returns:
        dict: Dictionary mapping tests to their converted result values for the target unit.
    """
    # Load target units from a JSON file
    with open("data/unit_conversion_data/unit.json", "r") as unit_file:
        target_units = json.load(unit_file)

    # Normalize target unit keys to lowercase
    target_units_normalized = {key.lower(): value for key, value in target_units.items()}

    # Initialize the final data packet
    converted_results = {}

    # Iterate through each row in the DataFrame
    for _, row in units_df.iterrows():
        test_name_normalized = row["Test"].lower().strip()  # Normalize test name
        target_unit = target_units_normalized.get(test_name_normalized)

        if not target_unit:
            print(f"No target unit defined for {row['Test']}")
            converted_results[row["Test"]] = None
            continue

        # Perform unit conversion
        converted_results[row["Test"]] = process_unit_conversion_with_regex(
            float(row["Result"]),
            row["Unit"].replace(" ", ""),
            target_unit
        )

    return converted_results
