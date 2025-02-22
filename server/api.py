from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .routes import router
import logging
import colorlog

logger = logging.getLogger("server")
logger.setLevel(logging.DEBUG)

formatter = colorlog.ColoredFormatter(
    "%(asctime)s - %(log_color)s%(levelname)-8s%(reset)s - "
    "%(module)s - %(funcName)s - %(lineno)d: "
    "%(message_log_color)s%(message)s%(reset)s",
    log_colors={
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "bold_red",
    },
    secondary_log_colors={
        "message": {
            "DEBUG": "cyan",
            "INFO": "light_green",
            "WARNING": "light_yellow",
            "ERROR": "light_red",
            "CRITICAL": "bold_red",
        }
    },
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

if not logger.hasHandlers():
    logger.addHandler(handler)

# Initialize FastAPI app with metadata
app = FastAPI(
    title="TATA Blood Report Processor API",
    description="An API to process blood report markdown and extract structured data.",
    version="1.2.0"
)

# Add CORS middleware (optional but useful)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (NOT recommended for production)
    allow_credentials=True,  # Supports cookies and authentication headers
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers (Authorization, Content-Type, etc.)
)

# Include the router
app.include_router(router)

# Global exception handling (optional)
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal Server Error: {str(exc)}"},
    )
