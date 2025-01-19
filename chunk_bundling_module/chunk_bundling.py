import pandas as pd
import json

def bundle_dataframes(dataframes):
    """
    Merge a list of DataFrames into a single DataFrame and convert to JSON.

    Args:
        dataframes (list): List of Pandas DataFrames.

    Returns:
        str: JSON representation of the merged DataFrame.
    """
    merged_df = pd.concat(dataframes, ignore_index=True)
    return merged_df.to_json(orient="records")

if __name__ == "__main__":
    dfs = [
        pd.DataFrame([
            {"Test": "Haemoglobin", "Result": "11.3", "Unit": "gm/dl"},
            {"Test": "R.B.C. Count", "Result": "3.82", "Unit": "mil./cu.mm"}
        ]),
        pd.DataFrame([
            {"Test": "Packed Cell Volume", "Result": "32.7", "Unit": "%"},
            {"Test": "Mean Corpuscular Volume", "Result": "85.6", "Unit": "cubic micron"}
        ])
    ]
    result_json = bundle_dataframes(dfs)
    
    print(pd.read_json(result_json))
