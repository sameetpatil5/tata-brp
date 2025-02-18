from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .routes import router
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - Line %(lineno)d: %(message)s"
)
logger = logging.getLogger(__name__)


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
