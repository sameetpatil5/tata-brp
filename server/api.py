# api.py
from fastapi import FastAPI
from .routes import router as OCRRouter

# Initialize FastAPI app
app = FastAPI()

# Include the router from routes.py
app.include_router(OCRRouter, prefix="/ocr")

@app.get("/", tags=["Root"])
async def read_root():
    return {
        "message": "Welcome to the TATA Project OCR API!"
    }
