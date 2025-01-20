import pandas as pd
import re

def batch_chunks(markdown_content: str) -> list:
    """
    Identify and extract tables from markdown content.

    Args:
        markdown_content (str): The markdown content containing tables and text.

    Returns:
        list: A list of markdown table strings.
    """
    table_chunks = []
    table_pattern = re.compile(r"\|.*?\|\n(?:\|.*?\|\n)*")  # Regex to match markdown tables.

    for match in table_pattern.finditer(markdown_content):
        table = match.group().strip()  # Extract the table content.
        table_chunks.append(table)

    return table_chunks

def parse_chunks(table_content: str) -> pd.DataFrame:
    """
    Parse a markdown table into a Pandas DataFrame.

    Args:
        table_content (str): The markdown table content.

    Returns:
        pd.DataFrame: A DataFrame with columns 'Test', 'Result', and 'Unit'.
    """
    lines = table_content.strip().split("\n")

    # Determine where the data starts by checking for header separator lines.
    if len(lines) > 1 and ("|-" in lines[1] or "| -" in lines[1]):
        start_index = 2  # Skip header and separator.
    elif len(lines) > 0 and ("|-" in lines[0] or "| -" in lines[0]):
        start_index = 1  # Skip separator line only.
    else:
        start_index = 0  # No header separator, include all lines.

    headers = [col.strip() for col in lines[0].split("|")[1:-1]]  # Extract column headers.

    data = []
    for line in lines[start_index:]:
        cols = [col.strip() for col in line.split("|")[1:-1]]

        if len(cols) == 4:  # Handle properly formatted tables.
            test, result, unit, _ = cols
        elif len(cols) == 3:  # Handle merged columns.
            test, result_unit, _ = cols

            # Use regex to separate numeric result and unit.
            match = re.match(r"([\d.]+)\s+(\S.*)", result_unit)
            if match:
                result = match.group(1)  # Extract numeric result.
                unit = match.group(2)    # Extract unit.
            else:
                result = result_unit
                unit = _ or None
        else:
            continue  # Skip rows with unexpected formatting.

        data.append({"Test": test, "Result": result, "Unit": unit})

    # Create a DataFrame from the extracted data.
    df = pd.DataFrame(data)

    # Return None for empty or irrelevant tables.
    if df.empty or df.isnull().all(axis=None):
        return None

    return df

def bundle_chunks(chunk_dataframes: list[pd.DataFrame]) -> pd.DataFrame:
    """
    Merge a list of DataFrames into a single DataFrame.

    Args:
        dataframes (list): List of Pandas DataFrames to merge.

    Returns:
        pd.DataFrame: A single DataFrame containing all the merged data.
    """
    if not chunk_dataframes:
        return pd.DataFrame()  # Return an empty DataFrame if the list is empty.

    merged_chunk = pd.concat(chunk_dataframes, ignore_index=True)  # Merge all DataFrames.
    return merged_chunk
