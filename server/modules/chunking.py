import pandas as pd
from pprint import pformat
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - Line %(lineno)d: %(message)s"
)
logger = logging.getLogger(__name__)

def batch_chunks(markdown_content: str) -> list[str]:
    """
    Identify and extract entire markdown tables from content.

    Args:
        markdown_content (str): The markdown content containing tables.

    Returns:
        list[str]: A list of markdown table strings.
    """
    try:
        logger.info("Batching chunks from markdown content")
        table_chunks = []
        lines = markdown_content.strip().split("\n")
        
        current_table = []
        recording = False

        for line in lines:
            if "|" in line:  # Start recording when a '|' is found
                recording = True
                current_table.append(line)
            elif recording:  # Stop when there's no '|'
                table_chunks.append("\n".join(current_table))
                current_table = []
                recording = False

        # Append the last table if still recording
        if current_table:
            table_chunks.append("\n".join(current_table))
        logger.info(f"Successfully batched {len(table_chunks)} chunks from markdown content")
        return table_chunks

    except Exception as e:
        logger.error(f"Error while batching chunks from markdown content: {e}")

def parse_chunks(table_content: str) -> pd.DataFrame:
    """
    Parse a markdown table into a Pandas DataFrame, where each row contains:
    - test
    - result
    - unit
    - reference_range.
    
    Args:
        table_content (str): The markdown table content.

    Returns:
        pd.DataFrame: A DataFrame with columns 'test', 'result', 'unit', and 'reference_range'.
    """
    try:
        logger.info("Parsing chunks")
        lines = table_content.strip().split("\n")
        start_index = 2
        data = []

        for line in lines[start_index:]:
            cols = [col.strip() for col in line.split("|")[1:-1]]

            test, result, unit, reference_range = cols
            # test, result, unit, reference_range = cols if len(cols) == 4 else cols + ["-"] # Backup debug

            # Replace "-" entries with None (NULL equivalent in pandas).
            result = None if result == "-" else result
            unit = None if unit == "-" else unit
            reference_range = None if reference_range == "-" else reference_range

            data.append({"test": test, "result": result, "unit": unit, "reference_range": reference_range})

            logger.info(f"Parsed row form chunk: {pformat(data[-1])}")

        # Create a DataFrame from the parsed data.
        df = pd.DataFrame(data)

        # Return None for empty or irrelevant tables.
        if df.empty or df.isnull().all(axis=None):
            logger.warning("Chunk is empty or irrelevant")
            return None
        else:
            logger.info("Successfully parsed chunk")
            return df
    except Exception as e:
        logger.error(f"Error while parsing chunks: {e}")

def bundle_chunks(chunk_dataframes: list[pd.DataFrame]) -> pd.DataFrame:
    """
    Merge a list of DataFrames into a single DataFrame.

    Args:
        dataframes (list): List of Pandas DataFrames to merge.

    Returns:
        pd.DataFrame: A single DataFrame containing all the merged data.
    """
    try:
        logger.info("Bundling chunks")
        if not chunk_dataframes:
            logger.warning("Chunk dataframes is empty")
            return pd.DataFrame()

        # Remove any `None` entries from the list.
        chunk_dataframes = [df for df in chunk_dataframes if df is not None]

        if not chunk_dataframes:
            logger.warning("Chunk dataframes is empty")
            return pd.DataFrame()

        merged_chunk = pd.concat(chunk_dataframes, ignore_index=True)  # Merge all DataFrames.

        logger.info("Successfully bundled chunks")
        return merged_chunk

    except Exception as e:
        logger.error(f"Error while bundling chunks: {e}")
