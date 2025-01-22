from pydantic import BaseModel

# Define a Pydantic model for the input data
class OCRInput(BaseModel):
    markdown: str