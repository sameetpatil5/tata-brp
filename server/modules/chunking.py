import pandas as pd
from pprint import pformat
import logging

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
        logger.info("Batching chunks from markdown content...")
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
        logger.debug(f"Batched chunks: \n{pformat(table_chunks)}")
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
        logger.info("Parsing chunks...")
        lines = table_content.strip().split("\n")
        start_index = 2
        data = []

        for line in lines[start_index:]:
            cols = [col.strip() for col in line.split("|")[1:-1]]

            test, result, unit, reference_range = cols

            # Replace "-" entries with None (NULL equivalent in pandas).
            result = None if result == "-" else result
            unit = None if unit == "-" else unit
            reference_range = None if reference_range == "-" else reference_range

            data.append({"test": test, "result": result, "unit": unit, "reference_range": reference_range})

            logger.debug(f"Parsed row form chunk: \n{pformat(data[-1])}")

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
        logger.info("Bundling chunks...")
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
        logger.debug(f"Bundled chunks: \n{pformat(merged_chunk)}")
        return merged_chunk

    except Exception as e:
        logger.error(f"Error while bundling chunks: {e}")

if __name__ == "__main__":
    formatted_markdown = """
        # **Clinical Analysis Lab**

        ## **Medical Lab Technical Result Sheet**

        ### **Lab Details**
        - **Reg No.:** -
        - **NAME:** -
        - **REF BY:** -
        - **AGE:** - Years
        - **SEX:** Male
        - **DATE:** 23/11/2024

        ---

        ## **COMPLETE BLOOD COUNT**

        | TEST                   | RESULT         | UNIT          | REFERENCE RANGE     |
        |------------------------|---------------|--------------|---------------------|
        | Haemoglobin           | 11.3          | gm/dl        | 14 - 18             |
        | R.B.C. Count          | 3.82          | mil./cu.mm   | 4.5 - 6.5           |
        | Total WBC Count       | 3.83x10^3     | /µL         | 4 - 10              |
        | Platelets            | 246000        | /cmm        | 150000 - 450000     |

        ---

        ## **RED CELL ABSOLUTE VALUES**

        | TEST                              | RESULT  | UNIT          | REFERENCE RANGE |
        |-----------------------------------|--------|--------------|-----------------|
        | Packed Cell Volume               | 32.7   | %            | 40 - 54         |
        | Mean Corpuscular Volume          | 85.6   | cubic micron | 76 - 96         |
        | Mean Corpuscular Hemoglobin      | 29.5   | picograms    | 27 - 32         |
        | Mean corpuscular Hb Con.         | 34.5   | g/dl         | 32 - 36         |

        ---

        ## **DIFFERENTIAL COUNT**

        | TEST          | RESULT | UNIT | REFERENCE RANGE |
        |--------------|--------|------|-----------------|
        | Neutrophils  | 52     | %    | -               |
        | Lymphocytes  | 39     | %    | -               |
        | Eosinophil   | 01     | %    | -               |
        | Monocytes    | 08     | %    | -               |
        | Basophils    | 00     | %    | -               |

        ---

        ## **PERIPHERAL SMEAR EXAMINATION**

        | TEST          | RESULT                     | UNIT | REFERENCE RANGE |
        |--------------|---------------------------|------|-----------------|
        | Erythrocytes | Normocytic Normochromic   | -    | -               |
        | Leukocytes   | Normal morphology         | -    | -               |

        ---

        ### **NOTE:**
        The above results are subject to variations due to technical limitations. Correlation with clinical findings and other investigations should be performed.

        **Condition of reporting:**  
        Results are for the referring doctor's information. Test results may vary between laboratories or over time for the same patient. Only medical professionals familiar with reporting units, reference ranges, and limitations should interpret the results. **Not for judicial use.**

        ---

        ### **Medical Lab Technician**
        """

    raw_chunks = batch_chunks(formatted_markdown)
    processed_chunks = [parse_chunks(chunk) for chunk in raw_chunks]
    bundled_chunks = bundle_chunks(processed_chunks)
    print(bundled_chunks)