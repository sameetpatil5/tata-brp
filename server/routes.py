# routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .ocrprocessor import OCRProcessor

# Define a Pydantic model for the input data
class OCRInput(BaseModel):
    markdown: str

# Create a router for OCR processing
router = APIRouter()

# Initialize the OCRProcessor
ocr_processor = OCRProcessor()

@router.post("/process", tags=["OCR Processing"])
async def process_markdown(input_data: OCRInput):
    """
    Process the markdown string received from LlamaOCR and return the processed output.
    """
    try:
        # Process the input markdown
        ocr_processor.set_markdown(input_data.markdown)
        converted_units = ocr_processor.process_ocr()

        return {
            "processed_output": converted_units
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing markdown: {str(e)}")
