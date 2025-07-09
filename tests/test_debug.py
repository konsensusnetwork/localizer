#!/usr/bin/env python3
"""
Simple test script to debug translation issues with better error visibility
"""

import sys
import os
import traceback
from pathlib import Path

# Add the book_maker directory to the path
sys.path.insert(0, str(Path(__file__).parent / "book_maker"))

def test_translation_debug():
    """Test translation with debug output"""
    try:
        from book_maker.loader import BOOK_LOADER_DICT
        from book_maker.translator import MODEL_DICT
        from book_maker.cli import get_project_config
        
        print("DEBUG: Testing translation with enhanced error handling")
        
        # Test file path - you can change this to your actual file
        test_file = "test_books/sample-quarto.qmd"  # Adjust this path
        
        if not os.path.exists(test_file):
            print(f"ERROR: Test file not found: {test_file}")
            return
        
        print(f"DEBUG: Using test file: {test_file}")
        
        # Get project config
        project_dir = os.path.dirname(os.path.abspath(test_file))
        config = get_project_config(project_dir)
        
        print(f"DEBUG: Project config: {config}")
        
        # Test with openai model
        model = "openai"
        language = "fr"
        
        print(f"DEBUG: Testing with model: {model}, language: {language}")
        
        # Get API key
        api_key = None
        if model in config:
            api_key = config[model]
        
        if not api_key:
            print(f"ERROR: No API key found for model: {model}")
            return
        
        print(f"DEBUG: API key found: {api_key[:10]}...")
        
        # Create loader
        loader_class = BOOK_LOADER_DICT['txt']  # Treat qmd as txt
        translator_class = MODEL_DICT[model]
        
        print(f"DEBUG: Loader class: {loader_class}")
        print(f"DEBUG: Translator class: {translator_class}")
        
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
        
        print(f"DEBUG: Loader created successfully")
        print(f"DEBUG: Loader type: {type(loader)}")
        print(f"DEBUG: Translator type: {type(loader.translate_model)}")
        
        # Test translation
        print(f"DEBUG: Starting translation test...")
        result = loader.make_bilingual_book()
        print(f"DEBUG: Translation test completed: {result}")
        
    except Exception as e:
        print(f"ERROR in test_translation_debug: {type(e).__name__}: {str(e)}")
        print(f"DEBUG: Full traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    test_translation_debug() 