import re

# Unit conversion factors (example values; add more as needed)
CONVERSION_FACTORS = {
    "/cmm": 1e-6,  # Convert `/cmm` to `109/L`
    "gm/dl": 1,    # `gm/dl` to `g/dL` (already matching)
    "g/dL": 1,     # Identity conversion
}

# Standardize unit names to match the target units
STANDARD_UNIT_MAPPING = {
    "/cmm": "109/L",
    "gm/dl": "g/dL",
    "g/dL": "g/dL",
    "%": "%",
}

def convert_unit(value, current_unit, target_unit):
    """
    Convert a value from current_unit to target_unit.
    
    Args:
        value (float): The numerical value to convert.
        current_unit (str): The unit of the given value.
        target_unit (str): The desired unit to convert to.
    
    Returns:
        float: Converted value or None if conversion not possible.
    """
    # Standardize the current unit
    standardized_unit = STANDARD_UNIT_MAPPING.get(current_unit)
    if standardized_unit != target_unit:
        # Check if conversion factor exists
        if current_unit in CONVERSION_FACTORS:
            conversion_factor = CONVERSION_FACTORS[current_unit]
            return value * conversion_factor
        else:
            print(f"Conversion not defined for unit: {current_unit}")
            return None
    return value  # No conversion needed if units match


def process_data_row(test_name, result, unit, target_units):
    """
    Process a single row of test data, converting the unit if necessary.
    
    Args:
        test_name (str): Name of the test (e.g., "Haemoglobin").
        result (float): Result value of the test.
        unit (str): Current unit of the result.
        target_units (dict): Mapping of test names to target units.
    
    Returns:
        tuple: (test_name, converted_result, target_unit)
    """
    target_unit = target_units.get(test_name)
    if not target_unit:
        print(f"No target unit specified for: {test_name}")
        return test_name, result, unit

    converted_result = convert_unit(result, unit, target_unit)
    return test_name, converted_result, target_unit


# Example usage
if __name__ == "__main__":
    # Example test data
    test_data = [
        ("Haemoglobin", 11.3, "gm/dl"),
        ("WBC Count", 5800, "/cmm"),
        ("Platelets", 246000, "/cmm"),
        ("Neutrophil %", 52, "%"),
        ("Lymphocyte %", 39, "%"),
    ]

    # Target units
    target_units = {
        "WBC Count": "109/L",
        "Platelets": "109/L",
        "Neutrophil %": "%",
        "Lymphocyte %": "%",
        "Haemoglobin": "g/dL",
        "WBC Count x Neutrophil %": "109/L",
        "WBC Count x Lymphocyte %": "109/L",
    }

    # Process each test result
    for test_name, result, unit in test_data:
        processed_data = process_data_row(test_name, result, unit, target_units)
        print(processed_data)
