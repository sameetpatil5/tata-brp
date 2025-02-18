from pydantic import BaseModel, HttpUrl, field_validator
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
