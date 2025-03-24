import re
from typing import Dict, Union, Tuple, Optional
from pprint import pformat
import logging

import pandas as pd

logger = logging.getLogger(__name__)

TestData = Dict[str, Union[float, str, Tuple[Optional[float], Optional[float]]]]

def process_result(result: str) -> Optional[Tuple[float, float]]:
    """
    Processes a result string of the form '4.5x10^3', '2x5^4', '10x30', etc.,
    and returns the computed value.

    Args:
        result (str): The input string containing a multiplication expression.

    Returns:
        Tuple(float, float): A tuple containing the computed value and its multiplier.
    """
    logger.debug(f"Processing result: '{result}'")
    
    if not isinstance(result, str) or not result.strip():
        logger.error("Invalid result format: Input is not a string or empty.")
        return None
    
    if re.fullmatch(r"\d+(\.\d+)?", result):  # Single number case
        return float(result), 1
    
    match = re.match(r"(\d+(?:\.\d+)?)\s*x\s*(\d+(?:\.\d+)?)\^?(\d+)?", result)
    if match:
        base_num = float(match.group(1))  # First number before 'x'
        multiplier = float(match.group(2)) if match.group(2) else 1  # Number after 'x'
        exponent = int(match.group(3)) if match.group(3) else 1  # Exponent

        return base_num, pow(multiplier, exponent)
    
    logger.error(f"Invalid result format: '{result}'")
    return None

def process_reference_range(reference_range: str, multiplier: float) -> Optional[Tuple[float, float]]:
    """
    Processes a reference range string of the form '3.5 - 6.0' and returns
    the minimum and maximum values.

    Args:
        reference_range (str): The input string containing a range of values.

    Returns:
        Tuple(float, float): A tuple containing the minimum and maximum values.
    """
    if not reference_range:
        return None
    
    match = re.match(r"(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)", reference_range)
    if match:
        return float(match.group(1)) * multiplier, float(match.group(2)) * multiplier
    
    logger.error(f"Invalid reference range format: '{reference_range}'")
    return None

def process_unit(data: pd.DataFrame) -> Dict[str, TestData]:
    """
    Convert units in a DataFrame using regex patterns and target unit mappings.

    Args:
        units_df (pd.DataFrame): DataFrame containing 'test', 'result', 'unit', and 'reference_range' columns.

    Returns:
        dict: Dictionary mapping tests to their converted result values for the target unit.
    """
    if not isinstance(data, pd.DataFrame) or data.empty:
        logger.error("Invalid input: Expected a non-empty pandas DataFrame.")
        return {}
    
    logger.info(f"Processing {len(data)} rows for unit conversion...")
    converted_results = {}
    
    for index, row in data.iterrows():
        test_name = row.get("test")
        result = row.get("result")
        unit = row.get("unit")
        reference_range = row.get("reference_range")
        
        if not test_name or not result or not unit:
            logger.warning(f"Skipping row {index} due to missing required fields.")
            continue
        
        processed_result = process_result(result)
        if not processed_result:
            logger.warning(f"Skipping row {index}: Invalid result format.")
            continue
        
        base_num, multiplier = processed_result
        ref_range = process_reference_range(reference_range, multiplier) if reference_range else (None, None)
        
        converted_results[test_name] = {
            "result": base_num * multiplier,
            "unit": unit,
            "reference-range": ref_range
        }
        logger.debug(f"Converted row {index}:{test_name} successfully: {pformat(converted_results[test_name])}")

    logger.info("Unit conversion completed successfully.")
    return converted_results

def add_derived_tests(converted_units: Dict[str, TestData]) -> Dict[str, TestData]:
    """
    Add derived tests to the converted units dictionary.

    Args:
        converted_units (dict): Dictionary mapping tests to their converted result values for the target unit.

    Returns:
        dict: Updated dictionary with additional derived tests.
    """
    data = converted_units.copy()

    if "WBC count" in converted_units and "Neutrophil %" in converted_units:
        data["Absolute Neutrophil count"] = {
            "result": converted_units["WBC count"]["result"] * converted_units["Neutrophil %"]["result"] / 100,
            "unit": converted_units["WBC count"]["unit"],
            "reference-range": (None, None),
        }

    if "WBC count" in converted_units and "Lymphocyte %" in converted_units:
        data["Absolute Lymphocyte count"] = {
            "result": converted_units["WBC count"]["result"] * converted_units["Lymphocyte %"]["result"] / 100,
            "unit": converted_units["WBC count"]["unit"],
            "reference-range": (None, None),
        }

    return data

# Test
if __name__ == "__main__":
    data = {
    "test": ["Haemoglobin", "WBC count", "Platelets", "Neutrophil %", "Lymphocyte %"],
    "result": ["11.3", "3.83x10^3", "246000", "52", "39"],
    "unit": ["gm/dl", "/µL", "/cmm", "%", "%"],
    "reference_range": ["14 - 18", "4 - 10", "150000 - 450000", None, None]
}

    df = pd.DataFrame(data)
    converted_units = process_unit(df)
    data = add_derived_tests(converted_units)
    print(data)