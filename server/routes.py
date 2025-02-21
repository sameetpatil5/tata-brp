from fastapi import APIRouter, HTTPException, Depends
from .models import Markdown, FilePath
from .processor import Processor
from phi.workflow import RunResponse
from typing import Optional, Iterator
import logging
import json


logger = logging.getLogger(__name__)

# Create a router for OCR processing
router = APIRouter()

# Initialize the OCRProcessor
processor = Processor()

def validate_input(file_path: Optional[FilePath] = None, input_data: Optional[Markdown] = None):
    """
    Validates the input parameters for the OCR processing route.

    Args:
        file_path (Optional[FilePath]): Path to the file to be processed.
        input_data (Optional[Markdown]): Markdown input to be processed.

    Returns:
        A dictionary containing the file_path and input_data if the input is valid.

    Raises:
        HTTPException: If the input is invalid.
    """
    try:
        if not file_path and not input_data:
            raise HTTPException(status_code=400, detail="Either file_path or input_data must be provided.")
        
        if file_path and input_data:
            raise HTTPException(status_code=400, detail="Provide either file_path or input_data, not both.")
        
        valid_input = {"file_path": file_path, "input_data": input_data}
        logger.info("Successfully validated the input")
        return valid_input
    except Exception as e:
        logger.error(f"Error while validating the input: {e}")

@router.get("/", tags=["Root"])
async def root():
    """
    Root endpoint for the API.

    Returns a message with the status of the API.

    """
    
    logger.info("ROOT route hit")
    return {
        "message": "tata-brp is up and running!"
    }

@router.post("/process", tags=["Blood Report Processing"])
async def process(input_params: dict = Depends(validate_input)) -> dict:
    """
    Process a blood report either from a markdown string or a file path.

    This endpoint accepts a JSON object with either a 'file_path' or 'input_data' key.
    The value for 'file_path' should be a string representing a valid file path.
    The value for 'input_data' should be another JSON object with a 'markdown' key
    whose value is a string representing the markdown input to be processed.

    Returns a JSON object with a single key 'data' containing the processed result.

    Raises an HTTPException with status code 400 if the input is invalid.
    Raises an HTTPException with status code 500 if an error occurs during processing.
    """

    file_path = input_params.get("file_path", None)
    file_path = file_path.file_path if file_path else None  

    input_data = input_params.get("input_data", None)
    input_data = input_data.markdown if input_data else None

    logger.info("PROCESS route hit")

    try:
        data = {}

        response: Iterator[RunResponse] = processor.run(file=file_path, markdown=input_data)

        response_data = list(response)[-1].content

        data = json.loads(response_data)["content"]

        return data if data else logger.error("Returned data is empty"); raise HTTPException(status_code=204, detail=f"Processing the input returned No Content: {e}")
    
    except Exception as e:
        logger.error(f"Error processing markdown: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing markdown: {str(e)}")