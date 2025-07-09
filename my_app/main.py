import logging
import sys
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("DEBUG: Loaded environment variables from .env file")
except ImportError:
    print("DEBUG: python-dotenv not available, using system environment variables")

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('translation_debug.log')
    ]
)

# Create logger for this module
logger = logging.getLogger(__name__)

from my_app.routers import auth, translate
from my_app.core import get_supported_models

app = FastAPI(title="Book Translation Service", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(translate.router, prefix="/translate", tags=["translation"])

@app.get("/")
async def read_root():
    """Get service information"""
    return {
        "service": "Book Translation Service",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/models")
async def get_models():
    """Get supported models"""
    try:
        models = get_supported_models()
        logger.info(f"Retrieved {len(models)} supported models")
        return models
    except Exception as e:
        logger.error(f"Error getting models: {str(e)}")
        raise

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler to log all errors"""
    logger.error(f"Unhandled exception: {type(exc).__name__}: {str(exc)}")
    logger.error(f"Request URL: {request.url}")
    import traceback
    logger.error(f"Traceback: {traceback.format_exc()}")
    raise exc

def main():
    """Entry point for the start_api script"""
    import uvicorn
    logger.info("Starting translation service...")
    uvicorn.run("my_app.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()