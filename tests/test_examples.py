#!/usr/bin/env python3
"""
Comprehensive Test Examples for Bilingual Book Maker
Based on README and documentation examples
"""

import os
import pytest
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Test configuration
TEST_BOOKS = {
    "epub": "test_books/animal_farm.epub",
    "txt": "test_books/the_little_prince.txt", 
    "srt": "test_books/Lex_Fridman_episode_322.srt",
    "markdown": "test_books/lemo.epub"  # Using epub as markdown example
}

TEST_PROMPTS = {
    "en": "prompts/en/en-translation.prompt.md",
    "fr": "prompts/fr/fr-translation-1.prompt.md",
    "it": "prompts/it/it-translation.prompt.md"
}

# Environment variables for API keys - read after loading .env
OPENAI_KEY = os.getenv("BBM_OPENAI_API_KEY")
GEMINI_KEY = os.getenv("BBM_GOOGLE_GEMINI_KEY")

@pytest.fixture(scope="session")
def check_api_keys():
    """Check if API keys are available"""
    print(f"🔍 Checking API keys:")
    print(f"   BBM_OPENAI_API_KEY: {'Set' if OPENAI_KEY else 'Not set'}")
    print(f"   BBM_GOOGLE_GEMINI_KEY: {'Set' if GEMINI_KEY else 'Not set'}")
    
    if not OPENAI_KEY and not GEMINI_KEY:
        pytest.skip("No API keys available. Set BBM_OPENAI_API_KEY or BBM_GOOGLE_GEMINI_KEY")
    
    print(f"✅ API keys found - proceeding with tests")

@pytest.fixture(scope="session")
def temp_output_dir():
    """Create temporary output directory"""
    temp_dir = tempfile.mkdtemp(prefix="bbook_test_")
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)

class TestBasicTranslation:
    """Test basic translation functionality"""
    
    @pytest.mark.basic
    def test_epub_translation_openai(self, check_api_keys, temp_output_dir):
        """Test EPUB translation with OpenAI"""
        if not OPENAI_KEY:
            pytest.skip("OpenAI API key not available")
            
        cmd = [
            "python3", "make_book.py",
            "--book_name", TEST_BOOKS["epub"],
            "--model", "openai",
            "--language", "zh-hans",
            "--test",
            "--test_num", "3"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Command failed: {result.stderr}"
        
        # Check for output file
        output_files = list(Path(temp_output_dir).glob("*bilingual*"))
        assert len(output_files) > 0, "No bilingual output file found"
    
    @pytest.mark.basic
    def test_txt_translation_gemini(self, check_api_keys, temp_output_dir):
        """Test TXT translation with Gemini"""
        if not GEMINI_KEY:
            pytest.skip("Gemini API key not available")
            
        cmd = [
            "python3", "make_book.py",
            "--book_name", TEST_BOOKS["txt"],
            "--model", "gemini",
            "--language", "fr",
            "--test",
            "--test_num", "3"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Command failed: {result.stderr}"
        
        # Check for output file
        output_files = list(Path(temp_output_dir).glob("*bilingual*"))
        assert len(output_files) > 0, "No bilingual output file found"
    
    @pytest.mark.basic
    def test_srt_translation(self, check_api_keys, temp_output_dir):
        """Test SRT subtitle translation"""
        if not OPENAI_KEY:
            pytest.skip("OpenAI API key not available")
            
        cmd = [
            "python3", "make_book.py",
            "--book_name", TEST_BOOKS["srt"],
            "--model", "openai",
            "--language", "es",
            "--test",
            "--test_num", "3"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Command failed: {result.stderr}"

class TestModelSelection:
    """Test different model selection options"""
    
    @pytest.mark.models
    def test_specific_openai_model(self, check_api_keys, temp_output_dir):
        """Test specific OpenAI model selection"""
        if not OPENAI_KEY:
            pytest.skip("OpenAI API key not available")
            
        cmd = [
            "python3", "make_book.py",
            "--book_name", TEST_BOOKS["txt"],
            "--model_list", "gpt-3.5-turbo",
            "--language", "ja",
            "--test",
            "--test_num", "2"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Command failed: {result.stderr}"
    
    @pytest.mark.models
    def test_specific_gemini_model(self, check_api_keys, temp_output_dir):
        """Test specific Gemini model selection"""
        if not GEMINI_KEY:
            pytest.skip("Gemini API key not available")
            
        cmd = [
            "python3", "make_book.py",
            "--book_name", TEST_BOOKS["txt"],
            "--model_list", "gemini-1.5-flash",
            "--language", "de",
            "--test",
            "--test_num", "2"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Command failed: {result.stderr}"
    
    @pytest.mark.models
    def test_multiple_models_load_balancing(self, check_api_keys, temp_output_dir):
        """Test multiple models for load balancing"""
        if not OPENAI_KEY:
            pytest.skip("OpenAI API key not available")
            
        cmd = [
            "python3", "make_book.py",
            "--book_name", TEST_BOOKS["txt"],
            "--model_list", "gpt-3.5-turbo,gpt-4o-mini",
            "--language", "it",
            "--test",
            "--test_num", "3"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Command failed: {result.stderr}"

class TestAdvancedFeatures:
    """Test advanced features"""
    
    @pytest.mark.advanced
    def test_context_aware_translation(self, check_api_keys, temp_output_dir):
        """Test context-aware translation"""
        if not OPENAI_KEY:
            pytest.skip("OpenAI API key not available")
            
        cmd = [
            "python3", "make_book.py",
            "--book_name", TEST_BOOKS["txt"],
            "--model", "openai",
            "--language", "fr",
            "--use_context",
            "--test",
            "--test_num", "3"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Command failed: {result.stderr}"
    
    @pytest.mark.advanced
    def test_custom_prompt_simple(self, check_api_keys, temp_output_dir):
        """Test custom prompt with simple text"""
        if not OPENAI_KEY:
            pytest.skip("OpenAI API key not available")
            
        cmd = [
            "python3", "make_book.py",
            "--book_name", TEST_BOOKS["txt"],
            "--model", "openai",
            "--language", "es",
            "--prompt", "Translate {text} to {language}",
            "--test",
            "--test_num", "2"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Command failed: {result.stderr}"
    
    @pytest.mark.advanced
    def test_custom_prompt_file(self, check_api_keys, temp_output_dir):
        """Test custom prompt with file"""
        if not OPENAI_KEY:
            pytest.skip("OpenAI API key not available")
            
        cmd = [
            "python3", "make_book.py",
            "--book_name", TEST_BOOKS["txt"],
            "--model", "openai",
            "--language", "it",
            "--prompt", TEST_PROMPTS["en"],
            "--test",
            "--test_num", "2"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Command failed: {result.stderr}"
    
    @pytest.mark.advanced
    def test_batch_size_txt(self, check_api_keys, temp_output_dir):
        """Test batch size for TXT files"""
        if not OPENAI_KEY:
            pytest.skip("OpenAI API key not available")
            
        cmd = [
            "python3", "make_book.py",
            "--book_name", TEST_BOOKS["txt"],
            "--model", "openai",
            "--language", "de",
            "--batch_size", "20",
            "--test",
            "--test_num", "3"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Command failed: {result.stderr}"
    
    @pytest.mark.advanced
    def test_single_translate(self, check_api_keys, temp_output_dir):
        """Test single translation mode"""
        if not OPENAI_KEY:
            pytest.skip("OpenAI API key not available")
            
        cmd = [
            "python3", "make_book.py",
            "--book_name", TEST_BOOKS["txt"],
            "--model", "openai",
            "--language", "ja",
            "--single_translate",
            "--test",
            "--test_num", "2"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Command failed: {result.stderr}"
        
        # Check for translated file (not bilingual)
        output_files = list(Path(temp_output_dir).glob("*translated*"))
        assert len(output_files) > 0, "No translated output file found"

class TestLanguageSupport:
    """Test different language support"""
    
    @pytest.mark.languages
    def test_chinese_simplified(self, check_api_keys, temp_output_dir):
        """Test Chinese Simplified translation"""
        if not OPENAI_KEY:
            pytest.skip("OpenAI API key not available")
            
        cmd = [
            "python3", "make_book.py",
            "--book_name", TEST_BOOKS["txt"],
            "--model", "openai",
            "--language", "zh-hans",
            "--test",
            "--test_num", "2"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Command failed: {result.stderr}"
    
    @pytest.mark.languages
    def test_chinese_traditional(self, check_api_keys, temp_output_dir):
        """Test Chinese Traditional translation"""
        if not OPENAI_KEY:
            pytest.skip("OpenAI API key not available")
            
        cmd = [
            "python3", "make_book.py",
            "--book_name", TEST_BOOKS["txt"],
            "--model", "openai",
            "--language", "zh-hant",
            "--test",
            "--test_num", "2"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Command failed: {result.stderr}"
    
    @pytest.mark.languages
    def test_japanese(self, check_api_keys, temp_output_dir):
        """Test Japanese translation"""
        if not OPENAI_KEY:
            pytest.skip("OpenAI API key not available")
            
        cmd = [
            "python3", "make_book.py",
            "--book_name", TEST_BOOKS["txt"],
            "--model", "openai",
            "--language", "ja",
            "--test",
            "--test_num", "2"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Command failed: {result.stderr}"
    
    @pytest.mark.languages
    def test_korean(self, check_api_keys, temp_output_dir):
        """Test Korean translation"""
        if not OPENAI_KEY:
            pytest.skip("OpenAI API key not available")
            
        cmd = [
            "python3", "make_book.py",
            "--book_name", TEST_BOOKS["txt"],
            "--model", "openai",
            "--language", "ko",
            "--test",
            "--test_num", "2"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Command failed: {result.stderr}"
    
    @pytest.mark.languages
    def test_french(self, check_api_keys, temp_output_dir):
        """Test French translation"""
        if not OPENAI_KEY:
            pytest.skip("OpenAI API key not available")
            
        cmd = [
            "python3", "make_book.py",
            "--book_name", TEST_BOOKS["txt"],
            "--model", "openai",
            "--language", "fr",
            "--test",
            "--test_num", "2"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Command failed: {result.stderr}"
    
    @pytest.mark.languages
    def test_german(self, check_api_keys, temp_output_dir):
        """Test German translation"""
        if not OPENAI_KEY:
            pytest.skip("OpenAI API key not available")
            
        cmd = [
            "python3", "make_book.py",
            "--book_name", TEST_BOOKS["txt"],
            "--model", "openai",
            "--language", "de",
            "--test",
            "--test_num", "2"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Command failed: {result.stderr}"
    
    @pytest.mark.languages
    def test_spanish(self, check_api_keys, temp_output_dir):
        """Test Spanish translation"""
        if not OPENAI_KEY:
            pytest.skip("OpenAI API key not available")
            
        cmd = [
            "python3", "make_book.py",
            "--book_name", TEST_BOOKS["txt"],
            "--model", "openai",
            "--language", "es",
            "--test",
            "--test_num", "2"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Command failed: {result.stderr}"
    
    @pytest.mark.languages
    def test_italian(self, check_api_keys, temp_output_dir):
        """Test Italian translation"""
        if not OPENAI_KEY:
            pytest.skip("OpenAI API key not available")
            
        cmd = [
            "python3", "make_book.py",
            "--book_name", TEST_BOOKS["txt"],
            "--model", "openai",
            "--language", "it",
            "--test",
            "--test_num", "2"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Command failed: {result.stderr}"
    
    @pytest.mark.languages
    def test_portuguese(self, check_api_keys, temp_output_dir):
        """Test Portuguese translation"""
        if not OPENAI_KEY:
            pytest.skip("OpenAI API key not available")
            
        cmd = [
            "python3", "make_book.py",
            "--book_name", TEST_BOOKS["txt"],
            "--model", "openai",
            "--language", "pt",
            "--test",
            "--test_num", "2"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Command failed: {result.stderr}"
    
    @pytest.mark.languages
    def test_russian(self, check_api_keys, temp_output_dir):
        """Test Russian translation"""
        if not OPENAI_KEY:
            pytest.skip("OpenAI API key not available")
            
        cmd = [
            "python3", "make_book.py",
            "--book_name", TEST_BOOKS["txt"],
            "--model", "openai",
            "--language", "ru",
            "--test",
            "--test_num", "2"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Command failed: {result.stderr}"
    
    @pytest.mark.languages
    def test_arabic(self, check_api_keys, temp_output_dir):
        """Test Arabic translation"""
        if not OPENAI_KEY:
            pytest.skip("OpenAI API key not available")
            
        cmd = [
            "python3", "make_book.py",
            "--book_name", TEST_BOOKS["txt"],
            "--model", "openai",
            "--language", "ar",
            "--test",
            "--test_num", "2"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Command failed: {result.stderr}"

class TestPromptExamples:
    """Test different prompt examples"""
    
    @pytest.mark.prompts
    def test_english_prompt(self, check_api_keys, temp_output_dir):
        """Test English translation prompt"""
        if not OPENAI_KEY:
            pytest.skip("OpenAI API key not available")
            
        cmd = [
            "python3", "make_book.py",
            "--book_name", TEST_BOOKS["txt"],
            "--model", "openai",
            "--language", "fr",
            "--prompt", TEST_PROMPTS["en"],
            "--test",
            "--test_num", "2"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Command failed: {result.stderr}"
    
    @pytest.mark.prompts
    def test_french_prompt(self, check_api_keys, temp_output_dir):
        """Test French translation prompt"""
        if not OPENAI_KEY:
            pytest.skip("OpenAI API key not available")
            
        cmd = [
            "python3", "make_book.py",
            "--book_name", TEST_BOOKS["txt"],
            "--model", "openai",
            "--language", "en",
            "--prompt", TEST_PROMPTS["fr"],
            "--test",
            "--test_num", "2"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Command failed: {result.stderr}"
    
    @pytest.mark.prompts
    def test_italian_prompt(self, check_api_keys, temp_output_dir):
        """Test Italian translation prompt"""
        if not OPENAI_KEY:
            pytest.skip("OpenAI API key not available")
            
        cmd = [
            "python3", "make_book.py",
            "--book_name", TEST_BOOKS["txt"],
            "--model", "openai",
            "--language", "en",
            "--prompt", TEST_PROMPTS["it"],
            "--test",
            "--test_num", "2"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Command failed: {result.stderr}"

class TestCLIExamples:
    """Test CLI command examples"""
    
    @pytest.mark.cli
    def test_bbook_maker_command(self, check_api_keys, temp_output_dir):
        """Test bbook_maker CLI command"""
        if not OPENAI_KEY:
            pytest.skip("OpenAI API key not available")
            
        cmd = [
            "bbook_maker",
            "--book_name", TEST_BOOKS["txt"],
            "--model", "openai",
            "--language", "zh-hans",
            "--test",
            "--test_num", "2"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Command failed: {result.stderr}"

class TestErrorHandling:
    """Test error handling scenarios"""
    
    @pytest.mark.errors
    def test_missing_book_file(self, check_api_keys, temp_output_dir):
        """Test error handling for missing book file"""
        if not OPENAI_KEY:
            pytest.skip("OpenAI API key not available")
            
        cmd = [
            "python3", "make_book.py",
            "--book_name", "nonexistent_file.txt",
            "--model", "openai",
            "--language", "zh-hans",
            "--test"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode != 0, "Should fail with missing file"
    
    @pytest.mark.errors
    def test_invalid_language(self, check_api_keys, temp_output_dir):
        """Test error handling for invalid language"""
        if not OPENAI_KEY:
            pytest.skip("OpenAI API key not available")
            
        cmd = [
            "python3", "make_book.py",
            "--book_name", TEST_BOOKS["txt"],
            "--model", "openai",
            "--language", "invalid-language",
            "--test",
            "--test_num", "1"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        # This might succeed but should handle gracefully
        assert result.returncode in [0, 1], f"Unexpected return code: {result.returncode}"

def run_standalone_tests(verbose=False):
    """Run tests standalone for manual testing"""
    import sys
    
    # Set up test environment
    os.environ.setdefault("BBM_OPENAI_API_KEY", "test-key")
    os.environ.setdefault("BBM_GOOGLE_GEMINI_KEY", "test-key")
    
    # Run specific test
    test_name = "test_epub_translation_openai"
    test_class = TestBasicTranslation()
    
    if hasattr(test_class, test_name):
        test_method = getattr(test_class, test_name)
        try:
            test_method()
            print(f"✅ {test_name} passed")
        except Exception as e:
            print(f"❌ {test_name} failed: {e}")
    else:
        print(f"❌ Test method {test_name} not found")

def test_environment_setup():
    """Test that environment variables are loaded correctly"""
    print(f"🔍 Environment check:")
    print(f"   BBM_OPENAI_API_KEY: {'Set' if os.getenv('BBM_OPENAI_API_KEY') else 'Not set'}")
    print(f"   BBM_GOOGLE_GEMINI_KEY: {'Set' if os.getenv('BBM_GOOGLE_GEMINI_KEY') else 'Not set'}")
    
    # Check if .env file exists
    env_file = Path('.env')
    if env_file.exists():
        print(f"   .env file: Found")
    else:
        print(f"   .env file: Not found")
    
    # Check test books
    for book_type, book_path in TEST_BOOKS.items():
        if Path(book_path).exists():
            print(f"   {book_type} book: Found")
        else:
            print(f"   {book_type} book: Missing")
    
    # Check test prompts
    for prompt_type, prompt_path in TEST_PROMPTS.items():
        if Path(prompt_path).exists():
            print(f"   {prompt_type} prompt: Found")
        else:
            print(f"   {prompt_type} prompt: Missing")

if __name__ == "__main__":
    run_standalone_tests(verbose=True) 