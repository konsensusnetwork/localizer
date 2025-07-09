#!/usr/bin/env python3
"""
Test script for translation with enhanced debugging
"""

import os
import sys
import logging
from pathlib import Path

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
        logging.FileHandler('test_translation_debug.log')
    ]
)

logger = logging.getLogger(__name__)

def get_api_key_for_model(model: str) -> str:
    """Get API key from environment variables or config"""
    # Try environment variables first
    env_key = os.getenv(f"{model.upper()}_API_KEY")
    if env_key:
        logger.info(f"Using API key from environment variable {model.upper()}_API_KEY")
        return env_key
    
    # Try common environment variable names
    common_keys = [
        "BBM_OPENAI_API_KEY",  # Project-specific key
        "OPENAI_API_KEY",
        "OPENAI_KEY", 
        "API_KEY"
    ]
    
    for key in common_keys:
        env_key = os.getenv(key)
        if env_key:
            logger.info(f"Using API key from environment variable {key}")
            return env_key
    
    # If no environment variable found, try to read from a simple config file
    config_file = Path.home() / ".localizer_config"
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                for line in f:
                    if line.strip() and '=' in line:
                        key, value = line.strip().split('=', 1)
                        if key.strip() == model:
                            logger.info(f"Using API key from config file")
                            return value.strip()
        except Exception as e:
            logger.warning(f"Could not read config file: {e}")
    
    return None

def test_translation():
    """Test translation with debug output"""
    try:
        # Add book_maker to path
        sys.path.insert(0, str(Path(__file__).parent / "book_maker"))
        
        from book_maker.loader import BOOK_LOADER_DICT
        from book_maker.translator import MODEL_DICT
        
        logger.info("Starting translation test with enhanced debugging")
        
        # Test parameters
        test_file = "books/bm-it/ch01.qmd"
        model = "openai"
        language = "fr"
        
        logger.info(f"Test file: {test_file}")
        logger.info(f"Model: {model}")
        logger.info(f"Language: {language}")
        
        # Check if file exists
        if not os.path.exists(test_file):
            logger.error(f"Test file not found: {test_file}")
            # Try alternative test files
            alternative_files = [
                "books/bm-en/ch01.qmd",
                "books/bm-fr/ch01.qmd", 
                "books/bm-nl/ch01.qmd",
                "test_books/sample_quarto.qmd"
            ]
            
            for alt_file in alternative_files:
                if os.path.exists(alt_file):
                    test_file = alt_file
                    logger.info(f"Using alternative test file: {test_file}")
                    break
            else:
                logger.error("No suitable test file found")
                return False
        
        # Get API key using our workaround
        api_key = get_api_key_for_model(model)
        if not api_key:
            logger.error(f"No API key found for model: {model}")
            logger.error("Please set one of these environment variables:")
            logger.error("  - OPENAI_API_KEY")
            logger.error("  - OPENAI_KEY") 
            logger.error("  - API_KEY")
            logger.error("Or create a config file at ~/.localizer_config with:")
            logger.error(f"  {model}=your_api_key_here")
            return False
        
        logger.info(f"API key found: {api_key[:10]}...")
        
        # Create loader
        loader_class = BOOK_LOADER_DICT['txt']
        translator_class = MODEL_DICT[model]
        
        logger.info(f"Loader class: {loader_class}")
        logger.info(f"Translator class: {translator_class}")
        
        # Create loader instance
        loader = loader_class(
            test_file,
            translator_class,
            api_key,
            resume=False,
            language=language,
            model_api_base=None,
            is_test=True,
            test_num=1,  # Just test 1 line
            prompt_config=None,
            prompt_file_path=None,
            single_translate=False,
            context_flag=False,
            context_paragraph_limit=0,
            temperature=1.0,
        )
        
        logger.info("Loader created successfully")
        logger.info(f"Loader type: {type(loader)}")
        logger.info(f"Translator type: {type(loader.translate_model)}")
        
        # Initialize model list for ChatGPT API translator
        if hasattr(loader.translate_model, 'set_gpt35_models'):
            logger.info("Initializing GPT-3.5 models for ChatGPT API translator")
            loader.translate_model.set_gpt35_models()
        elif hasattr(loader.translate_model, 'set_model_list'):
            logger.info("Setting default model list for translator")
            loader.translate_model.set_model_list(["gpt-3.5-turbo"])
        
        logger.info(f"Model list initialized: {getattr(loader.translate_model, 'model_list', 'Not available')}")
        
        # Test translation
        logger.info("Starting translation test...")
        result = loader.make_bilingual_book()
        logger.info(f"Translation test completed: {result}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error in test_translation: {type(e).__name__}: {str(e)}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = test_translation()
    if success:
        print("✅ Translation test completed successfully")
    else:
        print("❌ Translation test failed")
        sys.exit(1) 