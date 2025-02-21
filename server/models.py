from pydantic import BaseModel, HttpUrl, field_validator, Field
from typing import Optional, Iterator, Dict, List, Tuple
import os

# Define a Pydantic model for the input data
class Markdown(BaseModel):
    markdown: str

class FilePath(BaseModel):
    file_path: str
    @field_validator("file_path")
    def validate_file_path(cls, value):
        """
        Validates the file path.
        - If it's a local path, checks if the file exists.
        - If it's a URL, checks if it's a valid HTTP(S) URL.
        """
        if value.startswith(("http://", "https://")):
            # Validate URL using Pydantic
            return HttpUrl(value)
        
        # Validate local file path
        if not os.path.exists(value):
            raise ValueError(f"File does not exist: {value}")

        return value

class TestData(BaseModel):
    result: float = Field(..., description="The result of the test.")
    unit: str = Field(..., description="The unit of the test result.")
    reference_range: Optional[Tuple[Optional[float], Optional[float]]] = Field(None, description="The reference range for the test result.")

class MetaData(BaseModel):
    no_of_tests: int = Field(..., description="The total number of tests rows in the Data")

class Data(BaseModel):
    data: Dict[str, TestData] = Field(..., description="The data of the report.")
    meta_data: MetaData = Field(..., description="The meta data of the report.")
