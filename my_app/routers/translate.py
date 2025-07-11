import logging
import os
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from pydantic import BaseModel
import uuid
from datetime import datetime

from my_app.core import translate_book_job, translate_book, get_supported_languages, get_supported_models, TranslationJob, TranslationConfig
from my_app.supabase_client import get_supabase_client, process_translation_completion

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
    supabase_logged: bool = False


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    progress: int
    message: str
    output_file: Optional[str] = None
    download_url: Optional[str] = None
    error: Optional[str] = None
    created_at: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


class UserTranslationsResponse(BaseModel):
    translations: List[Dict[str, Any]]
    count: int


@router.post("/start", response_model=TranslationResponse)
async def start_translation(request: TranslationRequest, background_tasks: BackgroundTasks):
    """Start a translation job with Supabase integration"""
    job_id = str(uuid.uuid4())
    
    logger.info("=" * 80)
    logger.info("TRANSLATION REQUEST RECEIVED")
    logger.info("=" * 80)
    logger.info(f"Job ID: {job_id}")
    logger.info(f"Book Path: {request.book_path}")
    logger.info(f"Model: {request.model}")
    logger.info(f"Language: {request.language}")
    logger.info(f"User ID: {request.user_id}")
    logger.info("=" * 80)
    
    # Create translation configuration
    config = TranslationConfig(
        job_id=job_id,
        book_path=request.book_path,
        model=request.model,
        language=request.language,
        user_id=request.user_id,
        model_list=request.model_list,
        batch_size=request.batch_size,
        single_translate=request.single_translate,
        test=request.test_mode,
        test_num=request.test_num,
        use_context=request.use_context,
        reasoning_effort=request.reasoning_effort,
        temperature=request.temperature,
        accumulated_num=request.accumulated_num,
        block_size=request.block_size,
        prompt_file=request.prompt_file
    )
    
    # Create translation job
    job = TranslationJob(config=config, status="pending")
    
    # Log initial job creation to Supabase
    supabase_client = get_supabase_client()
    supabase_logged = False
    
    if supabase_client.is_available():
        initial_log = supabase_client.log_translation_run(job)
        supabase_logged = initial_log.get("success", False)
        if supabase_logged:
            logger.info(f"Job {job_id} logged to Supabase database")
        else:
            logger.warning(f"Failed to log job {job_id} to Supabase: {initial_log.get('error')}")
    
    # Add translation task to background
    background_tasks.add_task(run_translation_with_supabase, job)
    
    return TranslationResponse(
        job_id=job_id,
        status="started",
        message="Translation job started",
        supabase_logged=supabase_logged
    )

async def run_translation_with_supabase(job: TranslationJob):
    """Run translation with full Supabase integration"""
    supabase_client = get_supabase_client()
    
    try:
        logger.info(f"Starting translation for job {job.config.job_id}")
        
        # Update job status and log to Supabase
        job.status = "running"
        job.started_at = datetime.now()
        
        if supabase_client.is_available():
            supabase_client.log_translation_run(job)
        
        # Run the translation
        completed_job = await translate_book_job(job)
        
        # Process completion with Supabase (upload files, logs, update database)
        if supabase_client.is_available():
            completion_results = process_translation_completion(completed_job)
            logger.info(f"Translation completion processed: {completion_results}")
        
        logger.info(f"Translation completed for job {job.config.job_id}")
        
    except Exception as e:
        logger.error(f"Translation failed for job {job.config.job_id}: {str(e)}")
        job.status = "failed"
        job.error = str(e)
        job.completed_at = datetime.now()
        
        # Log the failure to Supabase
        if supabase_client.is_available():
            supabase_client.log_translation_run(job)


@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job(job_id: str, user_id: str = Query(..., description="User ID for authorization")):
    """Get a specific translation job from Supabase"""
    supabase_client = get_supabase_client()
    
    if not supabase_client.is_available():
        raise HTTPException(status_code=503, detail="Supabase not available")
    
    result = supabase_client.get_translation_by_job_id(job_id, user_id)
    
    if not result.get("success"):
        raise HTTPException(status_code=404, detail=result.get("error", "Job not found"))
    
    translation = result["translation"]
    
    # Create download URL for output file if available
    download_url = None
    if translation.get("output_file"):
        file_path = f"translations/{user_id}/{job_id}/{os.path.basename(translation['output_file'])}"
        url_result = supabase_client.create_signed_url(file_path)
        if url_result.get("success"):
            download_url = url_result["signed_url"]
    
    return JobStatusResponse(
        job_id=job_id,
        status=translation["status"],
        progress=100 if translation["status"] == "completed" else 0,
        message=f"Translation {translation['status']}",
        output_file=translation.get("output_file"),
        download_url=download_url,
        error=translation.get("error"),
        created_at=translation.get("created_at"),
        started_at=translation.get("started_at"),
        completed_at=translation.get("completed_at")
    )


@router.get("/user/{user_id}/translations", response_model=UserTranslationsResponse)
async def get_user_translations(user_id: str, limit: int = Query(50, le=100)):
    """Get translation history for a user"""
    supabase_client = get_supabase_client()
    
    if not supabase_client.is_available():
        raise HTTPException(status_code=503, detail="Supabase not available")
    
    result = supabase_client.get_user_translations(user_id, limit)
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "Failed to fetch translations"))
    
    return UserTranslationsResponse(
        translations=result["translations"],
        count=result["count"]
    )


@router.get("/download/{job_id}")
async def download_translation(job_id: str, user_id: str = Query(..., description="User ID for authorization")):
    """Get download URL for translation output"""
    supabase_client = get_supabase_client()
    
    if not supabase_client.is_available():
        raise HTTPException(status_code=503, detail="Supabase not available")
    
    # Verify the job belongs to the user
    job_result = supabase_client.get_translation_by_job_id(job_id, user_id)
    if not job_result.get("success"):
        raise HTTPException(status_code=404, detail="Job not found")
    
    translation = job_result["translation"]
    if not translation.get("output_file"):
        raise HTTPException(status_code=404, detail="No output file available")
    
    # Create signed URL
    file_path = f"translations/{user_id}/{job_id}/{os.path.basename(translation['output_file'])}"
    url_result = supabase_client.create_signed_url(file_path, expires_in=3600)
    
    if not url_result.get("success"):
        raise HTTPException(status_code=500, detail="Failed to create download URL")
    
    return {
        "download_url": url_result["signed_url"],
        "expires_in": 3600,
                 "filename": os.path.basename(translation["output_file"])
     }


@router.post("/setup/supabase")
async def setup_supabase():
    """Setup Supabase buckets and verify connection"""
    supabase_client = get_supabase_client()
    
    if not supabase_client.is_available():
        raise HTTPException(status_code=503, detail="Supabase not configured or unavailable")
    
    # Ensure buckets exist
    bucket_result = supabase_client.ensure_buckets_exist()
    
    return {
        "supabase_available": True,
        "bucket_setup": bucket_result,
        "message": "Supabase setup completed"
    }


@router.get("/health/supabase")
async def check_supabase_health():
    """Check Supabase connection and availability"""
    supabase_client = get_supabase_client()
    
    return {
        "supabase_available": supabase_client.is_available(),
        "supabase_url": os.getenv("SUPABASE_URL") is not None,
        "supabase_service_key": os.getenv("SUPABASE_SERVICE_KEY") is not None,
        "storage_bucket": supabase_client.storage_bucket,
        "logs_bucket": supabase_client.logs_bucket
    }


@router.delete("/jobs/{job_id}")
async def delete_translation_job(job_id: str, user_id: str = Query(..., description="User ID for authorization")):
    """Delete a translation job and its associated files"""
    supabase_client = get_supabase_client()
    
    if not supabase_client.is_available():
        raise HTTPException(status_code=503, detail="Supabase not available")
    
    # Verify the job belongs to the user
    job_result = supabase_client.get_translation_by_job_id(job_id, user_id)
    if not job_result.get("success"):
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Delete files from storage
    translation_file_path = f"translations/{user_id}/{job_id}/"
    log_file_path = f"logs/{user_id}/{job_id}/"
    
    deleted_files = []
    
    # Note: This is a simplified deletion - in practice, you'd want to list files first
    try:
        # Delete translation files
        translation_result = supabase_client.delete_file(f"{translation_file_path}*")
        if translation_result.get("success"):
            deleted_files.append("translation_files")
        
        # Delete log files
        log_result = supabase_client.delete_file(f"{log_file_path}*")
        if log_result.get("success"):
            deleted_files.append("log_files")
        
    except Exception as e:
        logger.warning(f"Error deleting files for job {job_id}: {e}")
    
    return {
        "job_id": job_id,
        "deleted": True,
        "deleted_files": deleted_files,
        "message": "Translation job and files deleted"
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