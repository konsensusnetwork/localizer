import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field

from book_maker.loader import BOOK_LOADER_DICT
from book_maker.translator import MODEL_DICT
from book_maker.utils import LANGUAGES


@dataclass
class TranslationConfig:
    """Configuration for a translation job"""
    book_path: str
    model: str
    language: str
    user_id: str
    job_id: str = field(default_factory=lambda: str(__import__('uuid').uuid4()))
    model_list: Optional[str] = None
    batch_size: Optional[int] = None
    single_translate: bool = False
    test: bool = False
    test_num: int = 10
    use_context: bool = False
    reasoning_effort: str = "medium"
    temperature: float = 1.0
    accumulated_num: int = 1
    block_size: int = -1
    prompt: Optional[str] = None
    prompt_file: Optional[str] = None


@dataclass
class TranslationJob:
    """Translation job with status tracking"""
    config: TranslationConfig
    status: str = "pending"  # pending, running, completed, failed
    progress: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    output_file: Optional[str] = None
    error: Optional[str] = None
    token_usage: Dict[str, Any] = field(default_factory=dict)


# Set up logging
def setup_logging(debug=False):
    """Setup logging configuration"""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level)

# Default to INFO level
setup_logging(debug=False)
logger = logging.getLogger(__name__)

def get_supported_models():
    """Get list of supported models"""
    return list(MODEL_DICT.keys())

def get_supported_languages():
    """Get list of supported languages"""
    return list(LANGUAGES.keys())

async def translate_book_job(job: TranslationJob) -> TranslationJob:
    """
    Translate a book using a TranslationJob for better tracking
    """
    job.status = "running"
    job.started_at = datetime.now()
    
    try:
        result = await translate_book(
            book_path=job.config.book_path,
            model=job.config.model,
            language=job.config.language,
            model_list=job.config.model_list,
            batch_size=job.config.batch_size,
            single_translate=job.config.single_translate,
            test_mode=job.config.test,
            test_num=job.config.test_num,
            use_context=job.config.use_context,
            reasoning_effort=job.config.reasoning_effort,
            temperature=job.config.temperature,
            accumulated_num=job.config.accumulated_num,
            block_size=job.config.block_size,
            prompt_file=job.config.prompt_file,
            user_id=job.config.user_id
        )
        
        job.status = "completed" if result["success"] else "failed"
        job.completed_at = datetime.now()
        job.output_file = result.get("output_file")
        job.progress = 100
        
        if not result["success"]:
            job.error = result.get("message", "Translation failed")
            
    except Exception as e:
        job.status = "failed"
        job.completed_at = datetime.now()
        job.error = str(e)
        job.progress = 0
        logger.error(f"Translation job {job.config.job_id} failed: {e}")
        
    return job


async def translate_book(
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
) -> Dict[str, Any]:
    """
    Translate a book using the same logic as the CLI
    """
    logger.info("=" * 80)
    logger.info("TRANSLATION JOB STARTED")
    logger.info("=" * 80)
    logger.info(f"Book Path: {book_path}")
    logger.info(f"Model: {model}")
    logger.info(f"Language: {language}")
    logger.info(f"Model List: {model_list}")
    logger.info(f"Batch Size: {batch_size}")
    logger.info(f"Single Translate: {single_translate}")
    logger.info(f"Test Mode: {test_mode}")
    logger.info(f"Test Num: {test_num}")
    logger.info(f"Use Context: {use_context}")
    logger.info(f"Reasoning Effort: {reasoning_effort}")
    logger.info(f"Temperature: {temperature}")
    logger.info(f"Accumulated Num: {accumulated_num}")
    logger.info(f"Block Size: {block_size}")
    logger.info("=" * 80)

    # Validate book path
    if not os.path.isfile(book_path):
        raise FileNotFoundError(f"Book file {book_path} does not exist")

    # Get book loader based on file extension
    book_type = book_path.split(".")[-1]
    support_type_list = list(BOOK_LOADER_DICT.keys())
    if book_type not in support_type_list:
        raise Exception(f"Only support files of these formats: {','.join(support_type_list)}")

    book_loader_class = BOOK_LOADER_DICT.get(book_type)
    if book_loader_class is None:
        raise Exception("Unsupported loader")

    # Get translator class
    translate_model_class = MODEL_DICT.get(model)
    if translate_model_class is None:
        raise ValueError(f"Unsupported model: {model}")

    # Get API key based on model type
    api_key = ""
    if model in ["gpt-4", "gpt-4-turbo", "gpt-4-32k", "gpt-4-0613", "gpt-4-32k-0613", 
                 "gpt-4-1106-preview", "gpt-4-0125-preview", "gpt-3.5-turbo", "gpt-3.5-turbo-0125", 
                 "gpt-3.5-turbo-1106", "gpt-3.5-turbo-16k", "gpt-4o", "gpt-4o-mini", 
                 "o1-preview", "o1-mini", "o3-mini"]:
        # Load from environment
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("BBM_OPENAI_API_KEY", "")
        if not api_key:
            raise Exception("OpenAI API key not provided. Please set BBM_OPENAI_API_KEY environment variable.")
    
    # Create book loader instance with proper API key
    book_loader = book_loader_class(
        book_path,
        translate_model_class,
        api_key,
        False,  # resume
        language=language,
        model_api_base=None,
        is_test=test_mode,
        test_num=test_num,
        prompt_config=None,  # Let translator handle prompt parsing
        prompt_file_path=prompt_file,
        single_translate=single_translate,
        context_flag=use_context,
        context_paragraph_limit=0,
        temperature=temperature,
    )

    # Configure model list if provided
    if model_list and hasattr(book_loader.translate_model, 'set_model_list'):
        book_loader.translate_model.set_model_list(model_list.split(","))

    # Set reasoning effort if supported
    if hasattr(book_loader.translate_model, 'reasoning_effort'):
        book_loader.translate_model.reasoning_effort = reasoning_effort

    # Set other options
    if batch_size:
        book_loader.batch_size = batch_size
    if block_size > 0:
        book_loader.block_size = block_size
    if accumulated_num > 1:
        book_loader.accumulated_num = accumulated_num

    logger.info("Starting translation...")
    logger.info("=" * 60)

    # Call make_bilingual_book and let the translator handle everything
    result = book_loader.make_bilingual_book()

    logger.info("Translation completed successfully")
    
    # Find the output file
    output_file = None
    if result:
        # Look for the generated file
        base_name = os.path.splitext(book_path)[0]
        dir_name = os.path.dirname(book_path)
        base_name_only = os.path.basename(base_name)
        
        # Check for files with timestamp pattern
        for file in os.listdir(dir_name):
            if file.startswith(base_name_only) and file.endswith(('.md', '.qmd', '.txt')):
                if '_' in file and any(char.isdigit() for char in file):
                    output_file = os.path.join(dir_name, file)
                    break
        
        if not output_file:
            # Fallback to original name with _bilingual suffix
            output_file = f"{base_name}_bilingual.{book_type}"

    return {
        "success": result,
        "output_file": output_file,
        "message": "Translation completed successfully" if result else "Translation failed"
    }