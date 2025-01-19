import pandas as pd
import re

def parse_table(table_content):
    """
    Parse a markdown table into a Pandas DataFrame.

    Args:
        table_content (str): The markdown table content.

    Returns:
        pd.DataFrame: Parsed DataFrame with columns: 'Test', 'Result', 'Unit'.
    """
    lines = table_content.strip().split("\n")
    start_index = 2 if ("| -" or "|-") in lines[1].strip() else 1 if ("| -" or "|-") in lines[0].strip() else 0

    headers = [col.strip() for col in lines[0].split("|")[1:-1]]

    data = []
    for line in lines[start_index:]:  # Skip header and separator lines
        cols = [col.strip() for col in line.split("|")[1:-1]]
        if len(cols) == 4:  # Handle properly formatted tables
            test, result, unit, _ = cols
        elif len(cols) == 3:  # Handle merged columns
            test, result_unit, _ = cols

            # Use regex to separate numeric result and unit
            match = re.match(r"([\d.]+)\s+(\S.*)", result_unit)

            if match:
                result = match.group(1)  # Extract the numeric part
                unit = match.group(2)    # Extract the unit part
            else:
                result = result_unit
                unit = _ or None
        # elif len(cols) == 2:  # Handle missing columns
        #     test, result = cols
        #     unit = None
        else:
            continue
        data.append({"Test": test, "Result": result, "Unit": unit})

    # Create DataFrame and filter out irrelevant tables
    df = pd.DataFrame(data)

    # Drop tables where all columns have empty or missing values
    if df.empty or df.isnull().all(axis=None):
        return None

    return pd.DataFrame(data)

if __name__ == "__main__":
    table = """
    | Packed Cell Volume           | 32.7 %            | 40 - 54 |
    | Mean Corpuscular Volume      | 85.6 cubic micron | 76 - 96 |
    | Mean Corpuscular Hemoglobin  | 29.5 picograms    | 27 - 32 |
    | Mean corpuscular Hb Con.     | 34.5 g/dl         | 32 - 36 |
    """
    # table = "| **DIFFERENTIAL COUNT** |     |     |\n| ---------------------- | --- | --- |\n| Neutrophils            | 52  | %   |\n| Lymphocytes            | 39  | %   |\n| Eosinophil             | 01  | %   |\n| Monocytes              | 08  | %   |\n| Basophils              | 00  | %   |"
    df = parse_table(table)
    print(df)
