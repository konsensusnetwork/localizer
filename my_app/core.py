import os
import uuid
import json
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from book_maker.loader import BOOK_LOADER_DICT
from book_maker.translator import MODEL_DICT
from book_maker.cli import parse_prompt_arg, get_project_config
from book_maker.utils import LANGUAGES, TO_LANGUAGE_CODE


class TranslationConfig:
    """Configuration for translation jobs"""
    
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
        user_id: str = "",
        job_id: Optional[str] = None,
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
        self.user_id = user_id
        self.job_id = job_id or str(uuid.uuid4())


class TranslationJob:
    """Represents a translation job with status tracking"""
    
    def __init__(self, config: TranslationConfig):
        self.config = config
        self.status = "pending"
        self.progress = 0
        self.error: Optional[str] = None
        self.output_file: Optional[str] = None
        self.log_file: Optional[str] = None
        self.created_at = datetime.now()
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.token_usage: Dict[str, Any] = {}


def get_supported_models() -> Dict[str, Any]:
    """Get list of supported translation models"""
    return {
        "models": list(MODEL_DICT.keys()),
        "languages": {
            "choices": sorted(LANGUAGES.keys()) + sorted([k.title() for k in TO_LANGUAGE_CODE]),
            "default": "zh-hans"
        }
    }


def validate_translation_config(config: TranslationConfig) -> Dict[str, Any]:
    """Validate translation configuration"""
    errors = []
    
    # Validate book path
    if not os.path.exists(config.book_path):
        errors.append(f"Book file not found: {config.book_path}")
    
    # Validate model
    if config.model not in MODEL_DICT:
        errors.append(f"Unsupported model: {config.model}. Supported models: {list(MODEL_DICT.keys())}")
    
    # Validate language
    all_languages = sorted(LANGUAGES.keys()) + sorted([k.title() for k in TO_LANGUAGE_CODE])
    if config.language not in all_languages:
        errors.append(f"Unsupported language: {config.language}. Supported languages: {all_languages}")
    
    # Validate file extension
    file_ext = Path(config.book_path).suffix.lower()
    if file_ext not in ['.epub', '.txt', '.srt', '.qmd', '.md']:
        errors.append(f"Unsupported file type: {file_ext}. Supported types: .epub, .txt, .srt, .qmd, .md")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


async def translate_book_async(config: TranslationConfig, job: TranslationJob) -> Dict[str, Any]:
    """
    Asynchronous wrapper for book translation
    This function adapts the existing CLI-based translation to work with FastAPI
    """
    try:
        job.status = "started"
        job.started_at = datetime.now()
        
        # Parse prompt if provided
        prompt_config = None
        prompt_file_path = None
        
        if config.prompt:
            prompt_config, prompt_file_path = parse_prompt_arg(config.prompt)
        
        # Get API key for the model
        project_dir = os.path.dirname(os.path.abspath(config.book_path))
        api_key = get_api_key_for_model(config.model, project_dir)
        
        if not api_key:
            raise ValueError(f"API key not found for model: {config.model}")
        
        # Determine file type and select appropriate loader
        file_ext = Path(config.book_path).suffix.lower()
        
        if file_ext == '.epub':
            loader_class = BOOK_LOADER_DICT['epub']
        elif file_ext == '.txt':
            loader_class = BOOK_LOADER_DICT['txt']
        elif file_ext == '.srt':
            loader_class = BOOK_LOADER_DICT['srt']
        else:
            # For .qmd and .md files, treat as txt
            loader_class = BOOK_LOADER_DICT['txt']
        
        # Get translator model
        translator_class = MODEL_DICT[config.model]
        
        # Create loader instance
        loader = loader_class(
            config.book_path,
            translator_class,
            api_key,
            resume=False,
            language=config.language,
            model_api_base=None,
            is_test=config.test,
            test_num=config.test_num,
            prompt_config=prompt_config,
            prompt_file_path=prompt_file_path,
            single_translate=config.single_translate,
            context_flag=False,
            context_paragraph_limit=0,
            temperature=config.temperature,
        )
        
        # Set additional parameters
        if hasattr(loader, 'accumulated_num'):
            loader.accumulated_num = config.accumulated_num
        if hasattr(loader, 'block_size'):
            loader.block_size = config.block_size
        
        # Run translation in executor to avoid blocking
        loop = asyncio.get_event_loop()
        output_file = await loop.run_in_executor(None, run_translation_sync, loader)
        
        job.status = "completed"
        job.completed_at = datetime.now()
        job.output_file = output_file
        job.progress = 100
        
        return {
            "success": True,
            "output_file": output_file,
            "job_id": config.job_id,
            "status": "completed"
        }
        
    except Exception as e:
        job.status = "failed"
        job.error = str(e)
        job.completed_at = datetime.now()
        
        return {
            "success": False,
            "error": str(e),
            "job_id": config.job_id,
            "status": "failed"
        }


def run_translation_sync(loader) -> str:
    """Synchronous translation runner"""
    try:
        if hasattr(loader, 'make_bilingual_book'):
            # For EPUB files
            loader.make_bilingual_book()
            return loader.epub_name.replace('.epub', '_bilingual.epub')
        else:
            # For other file types
            loader.translate_book()
            # Generate output filename based on input
            name, ext = os.path.splitext(loader.book_path)
            return f"{name}_{loader.language}{ext}"
    except Exception as e:
        raise Exception(f"Translation failed: {str(e)}")


def get_api_key_for_model(model: str, project_dir: Optional[str] = None) -> Optional[str]:
    """Get API key for the specified model"""
    if model in ["openai", "chatgptapi", "gpt4", "gpt4omini", "gpt4o"]:
        return get_project_config("BBM_OPENAI_API_KEY", project_dir)
    elif model == "caiyun":
        return get_project_config("BBM_CAIYUN_API_KEY", project_dir)
    elif model == "deepl":
        return get_project_config("BBM_DEEPL_API_KEY", project_dir)
    elif model.startswith("claude"):
        return get_project_config("BBM_CLAUDE_API_KEY", project_dir)
    elif model == "customapi":
        return get_project_config("BBM_CUSTOM_API", project_dir)
    elif model in ["gemini", "geminipro"]:
        return get_project_config("BBM_GOOGLE_GEMINI_KEY", project_dir)
    elif model == "groq":
        return get_project_config("BBM_GROQ_API_KEY", project_dir)
    elif model == "xai":
        return get_project_config("BBM_XAI_API_KEY", project_dir)
    else:
        return None


# Global job storage (in production, use Redis or database)
active_jobs: Dict[str, TranslationJob] = {}


def get_job_status(job_id: str) -> Dict[str, Any]:
    """Get status of a translation job"""
    if job_id not in active_jobs:
        return {"error": "Job not found"}
    
    job = active_jobs[job_id]
    return {
        "job_id": job_id,
        "status": job.status,
        "progress": job.progress,
        "error": job.error,
        "output_file": job.output_file,
        "created_at": job.created_at.isoformat(),
        "started_at": job.started_at.isoformat() if job.started_at else None,
        "completed_at": job.completed_at.isoformat() if job.completed_at else None,
        "config": {
            "book_path": job.config.book_path,
            "model": job.config.model,
            "language": job.config.language,
            "single_translate": job.config.single_translate,
        }
    }


def create_translation_job(config: TranslationConfig) -> TranslationJob:
    """Create a new translation job"""
    job = TranslationJob(config)
    active_jobs[config.job_id] = job
    return job