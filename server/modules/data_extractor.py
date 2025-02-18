import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - Line %(lineno)d: %(message)s"
)
logger = logging.getLogger(__name__)

def extract_phrases(processed_chunks: pd.DataFrame) -> list[str]:
    """
    Extract a list of phrases from the 'test' column of a processed DataFrame.

    Args:
        processed_chunks (pd.DataFrame): DataFrame containing a 'test' column with phrases.

    Returns:
        list[str]: List of phrases extracted from the 'test' column.
    """
    try:
        test_list = processed_chunks['test'].tolist()
        logger.info(f"Successfully extracted {len(test_list)} phrases")
        return test_list
    except Exception as e:
        logger.error(f"Error while extracting phrases: {e}")

def extract_data(processed_chunks: pd.DataFrame, classified_phrases: dict) -> pd.DataFrame:
    """
    Filter and rename rows in a DataFrame based on classified phrases.

    Args:
        processed_chunks (pd.DataFrame): Input DataFrame with columns ['test', 'Result', 'Unit'].
        classified_phrases (dict): Dictionary mapping original phrases to target names.

    Returns:
        pd.DataFrame: Processed DataFrame with renamed and filtered rows.
    """
    try:
        # Create a reverse mapping from classified_phrases.
        reverse_mapping = {key.lower(): value for key, value in classified_phrases.items()}

        # Normalize the 'test' column for matching.
        processed_chunks['normalized_test'] = processed_chunks['test'].str.lower().str.strip()

        # Map normalized test names to their target names.
        processed_chunks['mapped_test'] = processed_chunks['normalized_test'].map(reverse_mapping)

        # Filter rows where 'mapped_test' is not null.
        filtered_data = processed_chunks[processed_chunks['mapped_test'].notnull()].copy()

        # Rename the 'test' column to the target name.
        filtered_data['test'] = filtered_data['mapped_test']

        # Drop temporary columns used for processing.
        filtered_data = filtered_data.drop(columns=['normalized_test', 'mapped_test'])

        # Reset the index for the resulting DataFrame.
        filtered_data = filtered_data.reset_index(drop=True)

        logger.info(f"Successfully extracted {len(filtered_data)} data rows")

        return filtered_data

    except Exception as e:
        logger.error(f"Error while extracting data: {e}")