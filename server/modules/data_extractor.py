import pandas as pd
import logging

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
        logger.info("Extracting phrases...")
        test_list = processed_chunks['test'].tolist()
        logger.info(f"Successfully extracted {len(test_list)} phrases")
        logger.debug(f"Extracted phrases: \n{test_list}")
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
        logger.info("Extracting data...")

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
        logger.debug(f"Extracted data: \n{filtered_data}")

        return filtered_data

    except Exception as e:
        logger.error(f"Error while extracting data: {e}")


if __name__ == "__main__":

    data = [
        {"test": "Haemoglobin", "result": "11.3", "unit": "gm/dl", "reference_range": "14 - 18"},
        {"test": "R.B.C. Count", "result": "3.82", "unit": "mil./cu.mm", "reference_range": "4.5 - 6.5"},
        {"test": "Total WBC Count", "result": "3.83x10^3", "unit": "/µL", "reference_range": "4 - 10"},
        {"test": "Platelets", "result": "246000", "unit": "/cmm", "reference_range": "150000 - 450000"},
        {"test": "Packed Cell Volume", "result": "32.7", "unit": "%", "reference_range": "40 - 54"},
        {"test": "Mean Corpuscular Volume", "result": "85.6", "unit": "cubic micron", "reference_range": "76 - 96"},
        {"test": "Mean Corpuscular Hemoglobin", "result": "29.5", "unit": "picograms", "reference_range": "27 - 32"},
        {"test": "Mean corpuscular Hb Con.", "result": "34.5", "unit": "g/dl", "reference_range": "32 - 36"},
        {"test": "Neutrophils", "result": "52", "unit": "%", "reference_range": None},
        {"test": "Lymphocytes", "result": "39", "unit": "%", "reference_range": None},
        {"test": "Eosinophil", "result": "01", "unit": "%", "reference_range": None},
        {"test": "Monocytes", "result": "08", "unit": "%", "reference_range": None},
        {"test": "Basophils", "result": "00", "unit": "%", "reference_range": None},
        {"test": "Erythrocytes", "result": "Normocytic Normochromic", "unit": None, "reference_range": None},
        {"test": "Leukocytes", "result": "Normal morphology", "unit": None, "reference_range": None}
        ]
    
    processed_chunks = pd.DataFrame(data)

    phrases = extract_phrases(processed_chunks)
    print(phrases)
    classified_phrases = {'Haemoglobin': 'Haemoglobin', 'R.B.C. Count': 'Unknown', 'Total WBC Count': 'WBC count', 'Platelets': 'Platelets', 'Packed Cell Volume': 'Unknown', 'Mean Corpuscular Volume': 'Unknown', 'Mean Corpuscular Hemoglobin': 'Unknown', 'Mean corpuscular Hb Con.': 'Unknown', 'Neutrophils': 'Neutrophil %', 'Lymphocytes': 'Lymphocyte %', 'Eosinophil': 'Unknown', 'Monocytes': 'Unknown', 'Basophils': 'Unknown', 'Erythrocytes': 'Unknown', 'Leukocytes': 'Unknown'}
    valid_phrases = {p: c for p, c in classified_phrases.items() if c != "Unknown"}
    extracted_data = extract_data(processed_chunks, valid_phrases)
    print(extracted_data)