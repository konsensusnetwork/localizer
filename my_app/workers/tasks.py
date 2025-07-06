import os
import asyncio
from typing import Dict, Any
from datetime import datetime

try:
    from celery import Celery
    CELERY_AVAILABLE = True
except ImportError:
    CELERY_AVAILABLE = False

from my_app.core import (
    TranslationConfig,
    TranslationJob,
    translate_book_async,
    active_jobs
)

# Celery configuration
if CELERY_AVAILABLE:
    BROKER_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    celery_app = Celery("translation_tasks", broker=BROKER_URL)
    
    # Celery configuration
    celery_app.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        result_expires=3600,
    )
else:
    celery_app = None


def create_translation_config_dict(config: TranslationConfig) -> Dict[str, Any]:
    """Convert TranslationConfig to dictionary for Celery serialization"""
    return {
        "book_path": config.book_path,
        "model": config.model,
        "language": config.language,
        "prompt": config.prompt,
        "batch_size": config.batch_size,
        "single_translate": config.single_translate,
        "model_list": config.model_list,
        "temperature": config.temperature,
        "test": config.test,
        "test_num": config.test_num,
        "accumulated_num": config.accumulated_num,
        "block_size": config.block_size,
        "user_id": config.user_id,
        "job_id": config.job_id
    }


def create_translation_config_from_dict(config_dict: Dict[str, Any]) -> TranslationConfig:
    """Create TranslationConfig from dictionary"""
    return TranslationConfig(**config_dict)


if CELERY_AVAILABLE and celery_app:
    @celery_app.task(bind=True)
    def run_translation_task(self, config_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Celery task for running translation"""
        try:
            # Convert dict back to TranslationConfig
            config = create_translation_config_from_dict(config_dict)
            
            # Create job if it doesn't exist
            if config.job_id not in active_jobs:
                job = TranslationJob(config)
                active_jobs[config.job_id] = job
            else:
                job = active_jobs[config.job_id]
            
            # Update task status
            job.status = "started"
            job.started_at = datetime.now()
            
            # Update task state
            self.update_state(
                state='PROGRESS',
                meta={'job_id': config.job_id, 'status': 'started'}
            )
            
            # Run translation synchronously in the worker
            # Note: Celery tasks are already running in background, so we don't need async here
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(translate_book_async(config, job))
                return result
            finally:
                loop.close()
                
        except Exception as e:
            # Update job status on error
            if config.job_id in active_jobs:
                job = active_jobs[config.job_id]
                job.status = "failed"
                job.error = str(e)
                job.completed_at = datetime.now()
            
            # Update task state
            self.update_state(
                state='FAILURE',
                meta={'job_id': config.job_id, 'error': str(e)}
            )
            
            raise


# Alternative implementation using Celery with better error handling
if CELERY_AVAILABLE and celery_app:
    @celery_app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60})
    def run_translation_task_with_retry(self, config_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Celery task for running translation with retry logic"""
        try:
            config = create_translation_config_from_dict(config_dict)
            
            # Update task progress
            self.update_state(
                state='PROGRESS',
                meta={
                    'job_id': config.job_id,
                    'status': 'started',
                    'progress': 0
                }
            )
            
            # Create or get job
            if config.job_id not in active_jobs:
                job = TranslationJob(config)
                active_jobs[config.job_id] = job
            else:
                job = active_jobs[config.job_id]
            
            # Run translation
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(translate_book_async(config, job))
                
                # Update final state
                self.update_state(
                    state='SUCCESS',
                    meta={
                        'job_id': config.job_id,
                        'status': 'completed',
                        'progress': 100,
                        'result': result
                    }
                )
                
                return result
                
            finally:
                loop.close()
                
        except Exception as e:
            # Update job status
            if config.job_id in active_jobs:
                job = active_jobs[config.job_id]
                job.status = "failed"
                job.error = str(e)
                job.completed_at = datetime.now()
            
            # Update task state
            self.update_state(
                state='FAILURE',
                meta={
                    'job_id': config.job_id,
                    'error': str(e),
                    'status': 'failed'
                }
            )
            
            raise


def start_translation_with_celery(config: TranslationConfig) -> str:
    """Start translation using Celery if available"""
    if not CELERY_AVAILABLE or not celery_app:
        raise Exception("Celery not available")
    
    config_dict = create_translation_config_dict(config)
    task = run_translation_task_with_retry.delay(config_dict)
    
    return task.id


def get_celery_task_status(task_id: str) -> Dict[str, Any]:
    """Get Celery task status"""
    if not CELERY_AVAILABLE or not celery_app:
        return {"error": "Celery not available"}
    
    task = celery_app.AsyncResult(task_id)
    
    if task.state == 'PENDING':
        return {
            "task_id": task_id,
            "status": "pending",
            "progress": 0
        }
    elif task.state == 'PROGRESS':
        return {
            "task_id": task_id,
            "status": "running",
            "progress": task.info.get('progress', 0),
            "job_id": task.info.get('job_id')
        }
    elif task.state == 'SUCCESS':
        return {
            "task_id": task_id,
            "status": "completed",
            "progress": 100,
            "result": task.info.get('result'),
            "job_id": task.info.get('job_id')
        }
    elif task.state == 'FAILURE':
        return {
            "task_id": task_id,
            "status": "failed",
            "error": str(task.info),
            "job_id": task.info.get('job_id') if isinstance(task.info, dict) else None
        }
    else:
        return {
            "task_id": task_id,
            "status": task.state,
            "info": task.info
        }


def is_celery_available() -> bool:
    """Check if Celery is available and configured"""
    return CELERY_AVAILABLE and celery_app is not None