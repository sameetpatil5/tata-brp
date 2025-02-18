import google.generativeai as genai
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - Line %(lineno)d: %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configure the Generative AI model
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def format_markdown(input_markdown: str) -> str:
    """
    Formats a markdown string to ensure proper rendering of medical tables and data.
    
    Args:
        input_markdown (str): The markdown string to be formatted.

    Returns:
        str: The formatted markdown string.
    """
    # Define the AI model to use
    MODEL_NAME = "gemini-2.0-flash-exp"
    model = genai.GenerativeModel(MODEL_NAME)
    logger.info(f"Model {MODEL_NAME} loaded")
    
    # Define the AI prompt
    prompt = f"""
    You are an expert in formatting medical reports in Markdown. The input report comes from an **OCR conversion of an image**, which may contain **unstructured** medical test data.  
    Your task is to **extract, structure, and format** the report while ensuring **no data loss** and maintaining medical accuracy.

    ### **Key Formatting Instructions:**
    1. **Identify and properly format all medical test data** into structured tables.  
    - Even if the OCR output does not contain tables, **reconstruct** them into this strict format:
        ```markdown
        | TEST        | RESULT   | UNIT  | REFERENCE RANGE |
        |-------------|----------|-------|-----------------|
        | ExampleTest | 5.6      | mg/dL | 3.5 - 6.0       |
        ```
    - **Extract and organize** scattered test values into their correct columns.
    - If a value is missing, replace it with `-` (e.g., if `REFERENCE RANGE` is not given, use `-`).

    2. **Ensure all medical values are correctly placed**  
    - The **RESULT** column must contain only numerical values (e.g., `5.6` or `5.6x10^9`).
    - The **UNIT** column must contain **only measurement units** (e.g., `/L` instead of `10^9/L`).
        - If the unit is written as `10^9/L`, **move `10^9` to the RESULT column** and keep `/L` in the UNIT column.

    3. **Preserve all other report sections** (e.g., patient details, doctor's notes)  
    - Improve readability while keeping all content intact.
    - Do not modify any names, numerical values, or medical terminology.

    4. **Handle OCR errors carefully:**  
    - If values appear fragmented, reformat them into structured tables without altering their meaning.
    - **Do not infer missing information**—if a value is unreadable due to OCR errors, **keep it as is**.

    5. **Strictly format all extracted test data into tables**  
    - Even if the OCR output is raw text, all medical values must be **transformed into a structured table**.
    - No test data should remain unformatted.

    ### **Input Markdown (Unstructured OCR Output):**
    ```markdown
    {input_markdown}
    ```

    ### **Provide the properly formatted markdown output below:**
    """

    # Generate the response from the AI model
    try:
        response = model.generate_content(prompt)
        formatted_markdown = response.text
        logger.info("Markdown formatting completed")
        return formatted_markdown
    except Exception as e:
        logger.error(f"Error during formatting markdown using AI: {e}")
