import re
from typing import Dict, Union, Tuple, Optional
from pprint import pformat
import logging

import pandas as pd

logger = logging.getLogger(__name__)

TestData = Dict[str, Union[float, str, Tuple[Optional[float], Optional[float]]]]

def process_result(result: str) -> Optional[Tuple[float, float]]:
    """
    Parses and evaluates a numerical result string that may include multipliers 
    (e.g., '4.5x10^3', '2x5^4', '10x30'). Extracts the base value and its multiplier.

    Args:
        result (str): The input string containing a numeric value with potential multipliers.

    Returns:
        Optional[Tuple[float, float]]: A tuple containing the base numeric value and its computed multiplier.
        Returns None if the input format is invalid.
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
    Parses a reference range string (e.g., '3.5 - 6.0') and scales it by a given multiplier.

    Args:
        reference_range (str): A string representing a range of numerical values.
        multiplier (float): The scaling factor to apply to the extracted range values.

    Returns:
        Optional[Tuple[float, float]]: A tuple containing the minimum and maximum values after scaling.
        Returns None if the input format is invalid.
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
    Processes a DataFrame containing test results, converting units and extracting 
    relevant numerical values.

    Args:
        data (pd.DataFrame): A DataFrame with 'test', 'result', 'unit', and 'reference_range' columns.

    Returns:
        Dict[str, TestData]: A dictionary mapping test names to their converted values, 
        including computed results and reference ranges.
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
    Computes and adds derived tests (e.g., Absolute Neutrophil Count, Absolute Lymphocyte Count)
    based on existing test values.

    Args:
        converted_units (Dict[str, TestData]): A dictionary containing test results with converted units.

    Returns:
        Dict[str, TestData]: An updated dictionary with additional derived test values.
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

    logger.info("Derived tests added successfully.")

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