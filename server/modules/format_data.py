import google.generativeai as genai
from dotenv import load_dotenv
import os

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
    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    
    # Define the AI prompt
    prompt = f"""
    You are tasked with formatting medical data in markdown format.
    The input markdown contains tables and other data related to medical reports.  
    Ensure that:
    - Tables are properly formatted and aligned.  
    - Tables don't have any full empty columns, or rows.
    (Remove them while making sure no data is lost).  
    - No numerical or textual data is changed.  
    - Subtle errors in formatting are corrected.  
    - The final output adheres to the standard format of medical blood reports.  

    Input markdown:  
    ```
    {input_markdown}  
    ```
    
    Provide the formatted markdown output below:
    """

    # Generate the response from the AI model
    try:
        response = model.generate_content(prompt)
        formatted_markdown = response.text
        return formatted_markdown
    except Exception as e:
        raise RuntimeError(f"Error during AI formatting: {str(e)}")