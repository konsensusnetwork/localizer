from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, UploadFile, File, Form
from typing import Dict, Any, List, Optional
import os
import uuid
import json
from pathlib import Path
import tempfile
import shutil
from pydantic import BaseModel, ConfigDict

from my_app.core import (
    TranslationConfig,
    TranslationJob,
    validate_translation_config,
    translate_book_async,
    get_job_status,
    get_supported_models,
    create_translation_job,
    active_jobs
)
from my_app.routers.auth import get_current_user

router = APIRouter()


class TranslationRequest:
    """Request model for translation"""
    
    model_config = ConfigDict(protected_namespaces=())
    
    def __init__(
        self,
        book_path: str,
        model: str,
        language: str,
        prompt: Optional[str] = None,
        batch_size: int = 1,
        single_translate: bool = False,
        model_list: Optional[str] = None,
        temperature: float = 1.0,
        test: bool = False,
        test_num: int = 10,
        accumulated_num: int = 1,
        block_size: int = -1,
    ):
        self.book_path = book_path
        self.model = model
        self.language = language
        self.prompt = prompt
        self.batch_size = batch_size
        self.single_translate = single_translate
        self.model_list = model_list
        self.temperature = temperature
        self.test = test
        self.test_num = test_num
        self.accumulated_num = accumulated_num
        self.block_size = block_size


@router.get("/models")
async def get_models():
    """Get supported translation models and languages"""
    return get_supported_models()


@router.post("/start")
async def start_translation(
    book_path: str = Form(...),
    model: str = Form(...),
    language: str = Form(...),
    prompt: Optional[str] = Form(None),
    prompt_file: Optional[str] = Form(None),
    batch_size: int = Form(1),
    single_translate: bool = Form(False),
    model_list: Optional[str] = Form(None),
    temperature: float = Form(1.0),
    test: bool = Form(False),
    test_num: int = Form(10),
    accumulated_num: int = Form(1),
    block_size: int = Form(-1),
    use_context: bool = Form(False),
    reasoning_effort: str = Form("medium"),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    user: Dict[str, Any] = Depends(get_current_user),
):
    """Start a translation job"""
    
    try:
        print(f"DEBUG: Starting translation with book_path={book_path}, model={model}, language={language}")
        print(f"DEBUG: User: {user}")
        
        # Use prompt file if provided, otherwise use custom prompt
        final_prompt = prompt_file if prompt_file else prompt
        
        # Create translation configuration
        config = TranslationConfig(
            book_path=book_path,
            model=model,
            language=language,
            prompt=final_prompt,
            batch_size=batch_size,
            single_translate=single_translate,
            model_list=model_list,
            temperature=temperature,
            test=test,
            test_num=test_num,
            accumulated_num=accumulated_num,
            block_size=block_size,
            user_id=user["id"]
        )
        
        print(f"DEBUG: Created config with job_id={config.job_id}")
        
        # Validate configuration
        validation_result = validate_translation_config(config)
        print(f"DEBUG: Validation result: {validation_result}")
        
        if not validation_result["valid"]:
            print(f"DEBUG: Validation failed with errors: {validation_result['errors']}")
            raise HTTPException(
                status_code=400,
                detail={"errors": validation_result["errors"]}
            )
        
        # Create job
        job = create_translation_job(config)
        print(f"DEBUG: Created job with status={job.status}")
        
        # Start translation in background
        async def run_translation():
            await translate_book_async(config, job)
        
        background_tasks.add_task(run_translation)
        
        return {
            "job_id": config.job_id,
            "status": "started",
            "message": "Translation job started successfully"
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"DEBUG: Unexpected error in start_translation: {str(e)}")
        print(f"DEBUG: Error type: {type(e)}")
        import traceback
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/upload-and-translate")
async def upload_and_translate(
    file: UploadFile = File(...),
    model: str = Form(...),
    language: str = Form(...),
    prompt: Optional[str] = Form(None),
    prompt_file: Optional[str] = Form(None),
    batch_size: int = Form(1),
    single_translate: bool = Form(False),
    model_list: Optional[str] = Form(None),
    temperature: float = Form(1.0),
    test: bool = Form(False),
    test_num: int = Form(10),
    accumulated_num: int = Form(1),
    block_size: int = Form(-1),
    use_context: bool = Form(False),
    reasoning_effort: str = Form("medium"),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    user: Dict[str, Any] = Depends(get_current_user),
):
    """Upload a file and start translation"""
    
    try:
        print(f"DEBUG: Starting upload and translate with filename={file.filename}, model={model}, language={language}")
        print(f"DEBUG: User: {user}")
        
        # Validate file type
        allowed_extensions = ['.epub', '.txt', '.srt', '.qmd', '.md']
        file_ext = Path(file.filename).suffix.lower()
        print(f"DEBUG: File extension: {file_ext}")
        
        if file_ext not in allowed_extensions:
            print(f"DEBUG: Unsupported file type: {file_ext}")
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_ext}. Supported types: {', '.join(allowed_extensions)}"
            )
        
        # Create uploads directory if it doesn't exist
        uploads_dir = Path("uploads")
        uploads_dir.mkdir(exist_ok=True)
        print(f"DEBUG: Uploads directory: {uploads_dir.absolute()}")
        
        # Save uploaded file
        file_id = str(uuid.uuid4())
        file_path = uploads_dir / f"{file_id}_{file.filename}"
        print(f"DEBUG: Saving file to: {file_path}")
        
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            print(f"DEBUG: File saved successfully to: {file_path}")
        except Exception as e:
            print(f"DEBUG: Failed to save file: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to save uploaded file: {str(e)}"
            )
        
        # Use prompt file if provided, otherwise use custom prompt
        final_prompt = prompt_file if prompt_file else prompt
        
        # Create translation configuration
        config = TranslationConfig(
            book_path=str(file_path),
            model=model,
            language=language,
            prompt=final_prompt,
            batch_size=batch_size,
            single_translate=single_translate,
            model_list=model_list,
            temperature=temperature,
            test=test,
            test_num=test_num,
            accumulated_num=accumulated_num,
            block_size=block_size,
            user_id=user["id"]
        )
        
        print(f"DEBUG: Created config with job_id={config.job_id}")
        
        # Validate configuration
        validation_result = validate_translation_config(config)
        print(f"DEBUG: Validation result: {validation_result}")
        
        if not validation_result["valid"]:
            print(f"DEBUG: Validation failed with errors: {validation_result['errors']}")
            # Clean up uploaded file if validation fails
            file_path.unlink(missing_ok=True)
            raise HTTPException(
                status_code=400,
                detail={"errors": validation_result["errors"]}
            )
        
        # Create job
        job = create_translation_job(config)
        print(f"DEBUG: Created job with status={job.status}")
        
        # Start translation in background
        async def run_translation():
            await translate_book_async(config, job)
            # Clean up uploaded file after translation
            file_path.unlink(missing_ok=True)
        
        background_tasks.add_task(run_translation)
        
        return {
            "job_id": config.job_id,
            "status": "started",
            "message": "File uploaded and translation job started successfully",
            "uploaded_file": file.filename
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"DEBUG: Unexpected error in upload_and_translate: {str(e)}")
        print(f"DEBUG: Error type: {type(e)}")
        import traceback
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/status/{job_id}")
async def get_translation_status(
    job_id: str,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Get translation job status"""
    
    job_status = get_job_status(job_id)
    
    if "error" in job_status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Check if user owns the job
    if job_id in active_jobs:
        job = active_jobs[job_id]
        if job.config.user_id != user["id"]:
            raise HTTPException(status_code=403, detail="Access denied")
    
    return job_status


@router.get("/jobs")
async def get_user_jobs(user: Dict[str, Any] = Depends(get_current_user)):
    """Get all translation jobs for the current user"""
    
    user_jobs = []
    for job_id, job in active_jobs.items():
        if job.config.user_id == user["id"]:
            user_jobs.append(get_job_status(job_id))
    
    return {
        "jobs": user_jobs,
        "total": len(user_jobs)
    }


@router.delete("/jobs/{job_id}")
async def cancel_job(
    job_id: str,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Cancel a translation job"""
    
    if job_id not in active_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = active_jobs[job_id]
    if job.config.user_id != user["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if job.status in ["completed", "failed"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel job with status: {job.status}"
        )
    
    # Mark job as cancelled
    job.status = "cancelled"
    job.error = "Job cancelled by user"
    
    return {
        "message": "Job cancelled successfully",
        "job_id": job_id
    }


@router.get("/download/{job_id}")
async def download_translation(
    job_id: str,
    user: Dict[str, Any] = Depends(get_current_user)
):
    """Get download link for completed translation"""
    
    if job_id not in active_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = active_jobs[job_id]
    if job.config.user_id != user["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if job.status != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Translation not completed. Status: {job.status}"
        )
    
    if not job.output_file or not os.path.exists(job.output_file):
        raise HTTPException(
            status_code=404,
            detail="Output file not found"
        )
    
    return {
        "download_url": f"/files/{job_id}",
        "filename": os.path.basename(job.output_file),
        "job_id": job_id
    }


@router.post("/validate")
async def validate_config(
    book_path: str = Form(...),
    model: str = Form(...),
    language: str = Form(...),
    user: Dict[str, Any] = Depends(get_current_user),
):
    """Validate translation configuration without starting job"""
    
    config = TranslationConfig(
        book_path=book_path,
        model=model,
        language=language,
        user_id=user["id"]
    )
    
    validation_result = validate_translation_config(config)
    
    return {
        "valid": validation_result["valid"],
        "errors": validation_result.get("errors", []),
        "config": {
            "book_path": config.book_path,
            "model": config.model,
            "language": config.language
        }
    }