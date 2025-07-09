import logging
import os
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel

from my_app.core import translate_book, get_supported_languages, get_supported_models

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()

class TranslationRequest(BaseModel):
    model_config = {"protected_namespaces": ()}
    
    book_path: str
    model: str
    language: str
    model_list: Optional[str] = None
    batch_size: Optional[int] = None
    single_translate: bool = False
    test_mode: bool = False
    test_num: int = 10
    use_context: bool = False
    reasoning_effort: str = "medium"
    temperature: float = 1.0
    accumulated_num: int = 1
    block_size: int = -1
    prompt_file: Optional[str] = None
    user_id: str = "mock_user"

class TranslationResponse(BaseModel):
    job_id: str
    status: str
    message: str

# Store jobs in memory (in production, use a database)
jobs: Dict[str, Dict[str, Any]] = {}

@router.post("/start", response_model=TranslationResponse)
async def start_translation(request: TranslationRequest, background_tasks: BackgroundTasks):
    """Start a translation job"""
    import uuid
    
    job_id = str(uuid.uuid4())
    
    logger.info("=" * 80)
    logger.info("TRANSLATION REQUEST RECEIVED")
    logger.info("=" * 80)
    logger.info(f"Job ID: {job_id}")
    logger.info(f"Book Path: {request.book_path}")
    logger.info(f"Model: {request.model}")
    logger.info(f"Language: {request.language}")
    logger.info(f"Model List: {request.model_list}")
    logger.info(f"Batch Size: {request.batch_size}")
    logger.info(f"Single Translate: {request.single_translate}")
    logger.info(f"Test Mode: {request.test_mode}")
    logger.info(f"Test Num: {request.test_num}")
    logger.info(f"Use Context: {request.use_context}")
    logger.info(f"Reasoning Effort: {request.reasoning_effort}")
    logger.info(f"Temperature: {request.temperature}")
    logger.info(f"Accumulated Num: {request.accumulated_num}")
    logger.info(f"Block Size: {request.block_size}")
    logger.info(f"Prompt File: {request.prompt_file}")
    logger.info("=" * 80)
    
    # Initialize job status
    jobs[job_id] = {
        "status": "running",
        "progress": 0,
        "message": "Translation started",
        "result": None,
        "error": None
    }
    
    # Add translation task to background
    background_tasks.add_task(
        run_translation,
        job_id,
        request.book_path,
        request.model,
        request.language,
        request.model_list,
        request.batch_size,
        request.single_translate,
        request.test_mode,
        request.test_num,
        request.use_context,
        request.reasoning_effort,
        request.temperature,
        request.accumulated_num,
        request.block_size,
        request.prompt_file,
        request.user_id
    )
    
    return TranslationResponse(
        job_id=job_id,
        status="started",
        message="Translation job started"
    )

async def run_translation(
    job_id: str,
    book_path: str,
    model: str,
    language: str,
    model_list: Optional[str] = None,
    batch_size: Optional[int] = None,
    single_translate: bool = False,
    test_mode: bool = False,
    test_num: int = 10,
    use_context: bool = False,
    reasoning_effort: str = "medium",
    temperature: float = 1.0,
    accumulated_num: int = 1,
    block_size: int = -1,
    prompt_file: Optional[str] = None,
    user_id: str = "mock_user"
):
    """Run the translation in background"""
    try:
        logger.info(f"Starting translation for job {job_id}")
        
        # Call the core translation function with all parameters
        result = await translate_book(
            book_path=book_path,
            model=model,
            language=language,
            model_list=model_list,
            batch_size=batch_size,
            single_translate=single_translate,
            test_mode=test_mode,
            test_num=test_num,
            use_context=use_context,
            reasoning_effort=reasoning_effort,
            temperature=temperature,
            accumulated_num=accumulated_num,
            block_size=block_size,
            prompt_file=prompt_file,
            user_id=user_id
        )
        
        # Update job status
        jobs[job_id].update({
            "status": "completed" if result["success"] else "failed",
            "progress": 100,
            "result": result,
            "message": result["message"]
        })
        
        logger.info(f"Translation completed for job {job_id}: {result['message']}")
        
    except Exception as e:
        logger.error(f"Translation failed for job {job_id}: {str(e)}")
        jobs[job_id].update({
            "status": "failed",
            "error": str(e),
            "message": f"Translation failed: {str(e)}"
        })

@router.get("/jobs")
async def get_jobs():
    """Get all translation jobs"""
    return {
        "jobs": [
            {
                "job_id": job_id,
                **job_data
            }
            for job_id, job_data in jobs.items()
        ]
    }

@router.get("/jobs/{job_id}")
async def get_job(job_id: str):
    """Get a specific translation job"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {
        "job_id": job_id,
        **jobs[job_id]
    }

@router.get("/models")
async def get_models():
    """Get supported models"""
    try:
        models = get_supported_models()
        logger.info(f"Retrieved {len(models)} supported models")
        return models
    except Exception as e:
        logger.error(f"Error getting models: {str(e)}")
        raise

@router.get("/languages")
async def get_languages():
    """Get supported languages"""
    try:
        languages = get_supported_languages()
        logger.info(f"Retrieved {len(languages)} supported languages")
        return languages
    except Exception as e:
        logger.error(f"Error getting languages: {str(e)}")
        raise

@router.get("/validate")
async def validate_translation(
    model: str,
    language: str,
    model_list: Optional[str] = None,
    prompt_file: Optional[str] = None
):
    """Validate translation parameters"""
    try:
        # Basic validation
        if not model:
            raise ValueError("Model is required")
        
        if not language:
            raise ValueError("Language is required")
        
        # Check if model is supported
        from book_maker.translator import MODEL_DICT
        if model not in MODEL_DICT:
            raise ValueError(f"Unsupported model: {model}")
        
        # Check if language is supported
        from book_maker.utils import LANGUAGES
        if language not in LANGUAGES and language not in [k.title() for k in LANGUAGES.keys()]:
            raise ValueError(f"Unsupported language: {language}")
        
        # Check prompt file if provided
        if prompt_file and not os.path.exists(prompt_file):
            raise ValueError(f"Prompt file not found: {prompt_file}")
        
        return {
            "valid": True,
            "message": "Parameters are valid"
        }
        
    except Exception as e:
        return {
            "valid": False,
            "message": str(e)
        }