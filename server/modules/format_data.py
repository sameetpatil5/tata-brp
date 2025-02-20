import google.generativeai as genai
from dotenv import load_dotenv
import os
import logging

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
    logger.info("Formatting markdown...")
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
    - There should be always the given 4 columns as (TEST, RESULT, UNIT, REFERENCE RANGE). Even if its out of context or not needed. Fill the values with '-' when they are not present.

    2. **Ensure all medical values are correctly placed**  
    - The **RESULT** column may contain numerical values or a string in format {{num}}x{{multipliers}} (e.g., `5.6` or `5.6x10^9`).
    - The **UNIT** column must contain **only measurement units** (e.g., `/L` instead of `10^9/L`).
        - If the unit is written as `10^9/L`, **move `10^9` to the RESULT column** and keep `/L` in the UNIT column.
        - This just an example if there is any multipliers (e.g., 10^3, or anything else) before '/' in the UNIT **move it to the RESULT column** as {{num}}x{{multipliers}} (e.g., 4.83x10^3) always.

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
        logger.debug(f"Formatted markdown: {formatted_markdown}")
        return formatted_markdown
    except Exception as e:
        logger.error(f"Error during formatting markdown using AI: {e}")

if __name__ == "__main__":
    markdown_content = """
                # **Clinical Analysis Lab**

                ## **Medical Lab Technical Result Sheet**

                ### **Lab**

                ### **Reg No.:**

                ### **NAME:**

                ### **REF BY**

                ### **AGE: Years**

                ### **SEX: Male**

                ### **DATE: 23/11/2024**

                ### **COMPLETE BLOOD COUNT**

                ### **TESTS**

                | **TESTS**       | **RESULTS** | **UNIT**   | **REFERENCE RANGE** |
                | --------------- | ----------- | ---------- | ------------------- |
                | Haemoglobin     | 11.3        | gm/dl      | 14 - 18             |
                | R.B.C. Count    | 3.82        | mil./cu.mm | 4.5 - 6.5           |
                | Total WBC Count | 3.83        | 10^3/µL    | 4 - 10              | 
                | Platelets       | 246000      | /cmm       | 150000 - 450000     |

                ### **RED CELL ABSOLUTE VALUES**

                | **RED CELL ABSOLUTE VALUES** |      |              |         |
                | ---------------------------- | ---- | ------------ | ------- |
                | Packed Cell Volume           | 32.7 | %            | 40 - 54 |
                | Mean Corpuscular Volume      | 85.6 | cubic micron | 76 - 96 |
                | Mean Corpuscular Hemoglobin  | 29.5 | picograms    | 27 - 32 |
                | Mean corpuscular Hb Con.     | 34.5 | g/dl         | 32 - 36 |

                ### **DIFFERENTIAL COUNT**

                | **DIFFERENTIAL COUNT** |     |     |
                | ---------------------- | --- | --- |
                | Neutrophils            | 52  | %   |
                | Lymphocytes            | 39  | %   |
                | Eosinophil             | 01  | %   |
                | Monocytes              | 08  | %   |
                | Basophils              | 00  | %   |

                ### **PERIPHERAL SMEAR EXAMINATION**

                | **PERIPHERAL SMEAR EXAMINATION** |                         |     |
                | -------------------------------- | ----------------------- | --- |
                | Erythrocytes                     | Normocytic Normochromic |     |
                | Leukocytes                       | Normal morphology       |     |

                ### **NOTE - THE ABOVE RESULTS ARE SUBJECT TO VARIATIONS DUE TO TECHNICAL LIMITATIONS HENCE CORRELATION WITH CLINICAL FINDINGS AND OTHER INVESTIGATION SHOULD BE DONE.**

                ### **Condition of reporting : The reported results are for information of the referring doctor.Results of tests may vary from laboratory also in some parameters from time to time for same patients. Only such medical professional who understand reporting units reference range and limitation should interpret the result. Not for iudical use.**

                ### **Medical Lab Technician**

                """

    formatted_content = format_markdown(markdown_content)
    