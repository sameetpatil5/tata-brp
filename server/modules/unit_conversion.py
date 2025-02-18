import pandas as pd
import re
from pprint import pformat
import logging

logger = logging.getLogger(__name__)

def process_result(result: str) -> tuple[float, float]:
    """
    Processes a result string of the form '4.5x10^3', '2x5^4', '10x30', etc.,
    and returns the computed value.

    Args:
        result (str): The input string containing a multiplication expression.

    Returns:
        tuple[float, float]: A tuple containing the computed value and its multiplier.
    """
    try:
        logger.debug(f"Processing result string: '{result}'")
        logger.info(f"Processing result...")

        # If the input is a single number, return it directly
        if re.fullmatch(r"[\d\.]+", result):  
            value = float(result)
            logger.debug(f"Result is a single number: {value}")

            logger.info("Processed result")
            return value, 1

        match = re.match(r"([\d\.]+)\s*x\s*([\d\.]+)\^?(\d+)?", result)
        if match:
            base_num = float(match.group(1))  # First number before 'x'
            multiplier = float(match.group(2)) if match.group(2) else 1  # Number after 'x'
            exponent = int(match.group(3)) if match.group(3) else 1  # Exponent

            final_multiplier = pow(multiplier, exponent)

            result_value = base_num * final_multiplier
            logger.debug(f"Parsed result: base={base_num}, multiplier={multiplier}, exponent={exponent}, computed={result_value}")
            
            logger.info("Processed result")
            return base_num, final_multiplier
        
        logger.error(f"Invalid format for result: '{result}'")
    except Exception as e:
        logger.error(f"Error while processing result: {e}")

def process_reference_range(reference_range: str, multiplier: float) -> tuple[float, float]:
    """
    Processes a reference range string of the form '3.5 - 6.0' and returns
    the minimum and maximum values.

    Args:
        reference_range (str): The input string containing a range of values.

    Returns:
        tuple[float, float]: A tuple containing the minimum and maximum values.
    """
    try:
        logger.info("Processing reference range...")
        logger.debug(f"Processing reference range string: '{reference_range}' with multiplier: {multiplier}")

        match = re.match(r"([\d\.]+)\s*-\s*([\d\.]+)", reference_range)
        if match:
            min_value = float(match.group(1)) * multiplier
            max_value = float(match.group(2)) * multiplier
            logger.debug(f"Parsed reference range: min={min_value}, max={max_value}")

            logger.info("Processed reference range")
            return min_value, max_value
        else:
            logger.error(f"Invalid format for reference range: '{reference_range}'")
    except Exception as e:
        logger.error(f"Error while processing reference range: {e}")

def unit_conversion(units_df: pd.DataFrame) -> dict:
    """
    Convert units in a DataFrame using regex patterns and target unit mappings.

    Args:
        units_df (pd.DataFrame): DataFrame containing 'test', 'result', 'unit', and 'reference_range' columns.

    Returns:
        dict: Dictionary mapping tests to their converted result values for the target unit.
    """
    try:
        logger.info(f"Starting unit conversion for {len(units_df)} rows.")

        converted_results = []

        for index, row in units_df.iterrows():
            try:
                logger.info(f"Processing row {index}...")
                logger.debug(f"Processing row {index}: {pformat(row.to_dict())}")

                base_num, multiplier = process_result(row["result"])
                min_value, max_value = process_reference_range(row["reference_range"], multiplier) if row["reference_range"] else (None, None)

                converted_entry = {
                    row["test"]: {
                        "result": base_num * multiplier,
                        "unit": row["unit"],
                        "reference-range": (min_value, max_value)
                    },
                }

                logger.debug(f"Converted row {index} successfully: {pformat(converted_entry)}")
                converted_results.append(converted_entry)

            except ValueError as e:
                logger.error(f"Error processing row {index}: {e}")

        logger.info("Unit conversion completed for all rows.")
        return converted_results

    except Exception as e:
        logger.error(f"Error during unit conversion: {e}")


if __name__ == "__main__":
    data = {
    "test": ["Haemoglobin", "WBC count", "Platelets", "Neutrophil %", "Lymphocyte %"],
    "result": ["11.3", "3.83x10^3", "246000", "52", "39"],
    "unit": ["gm/dl", "/µL", "/cmm", "%", "%"],
    "reference_range": ["14 - 18", "4 - 10", "150000 - 450000", None, None]
}

    df = pd.DataFrame(data)

    converted_units = unit_conversion(df)

    print(converted_units)