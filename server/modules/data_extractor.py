import pandas as pd

def extract_phrases(processed_chunks: pd.DataFrame) -> list[str]:
    """
    Extract a list of phrases from the 'Test' column of a processed DataFrame.

    Args:
        processed_chunks (pd.DataFrame): DataFrame containing a 'Test' column with phrases.

    Returns:
        list[str]: List of phrases extracted from the 'Test' column.
    """
    return processed_chunks['Test'].tolist()

def extract_data(processed_chunks: pd.DataFrame, classified_phrases: dict) -> pd.DataFrame:
    """
    Filter and rename rows in a DataFrame based on classified phrases.

    Args:
        processed_chunks (pd.DataFrame): Input DataFrame with columns ['Test', 'Result', 'Unit'].
        classified_phrases (dict): Dictionary mapping original phrases to target names.

    Returns:
        pd.DataFrame: Processed DataFrame with renamed and filtered rows.
    """
    # Create a reverse mapping from classified_phrases.
    reverse_mapping = {key.lower(): value for key, value in classified_phrases.items()}

    # Normalize the 'Test' column for matching.
    processed_chunks['Normalized Test'] = processed_chunks['Test'].str.lower().str.strip()

    # Map normalized test names to their target names.
    processed_chunks['Mapped Test'] = processed_chunks['Normalized Test'].map(reverse_mapping)

    # Filter rows where 'Mapped Test' is not null.
    filtered_data = processed_chunks[processed_chunks['Mapped Test'].notnull()].copy()

    # Rename the 'Test' column to the target name.
    filtered_data['Test'] = filtered_data['Mapped Test']

    # Drop temporary columns used for processing.
    filtered_data = filtered_data.drop(columns=['Normalized Test', 'Mapped Test'])

    # Reset the index for the resulting DataFrame.
    filtered_data = filtered_data.reset_index(drop=True)

    return filtered_data
