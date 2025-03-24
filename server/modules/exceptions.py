# exceptions.py
class AppBaseException(Exception):
    """Base class for all application-specific exceptions."""
    status_code = 500  # Default to Internal Server Error

    def __init__(self, detail="An error occurred"):
        self.detail = detail
        super().__init__(detail)

class DataProcessingError(AppBaseException):
    """Raised when data processing fails."""
    status_code = 400

class UnitConversionError(AppBaseException):
    """Raised when unit conversion fails."""
    status_code = 422

class FileProcessingError(AppBaseException):
    """Raised when file processing fails."""
    status_code = 415
