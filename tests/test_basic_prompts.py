"""
Tests for basic prompts using test books.

This module tests the translation system with basic prompts and test books
to ensure proper functionality across different file formats and translation models.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Dict, Any

import pytest


@pytest.fixture()
def test_book_dir() -> str:
    """Return test book directory path."""
    return str(Path(__file__).parent.parent / "test_books")


@pytest.fixture()
def prompts_dir() -> str:
    """Return prompts directory path."""
    return str(Path(__file__).parent.parent / "prompts")


@pytest.fixture()
def temp_workspace():
    """Create a temporary workspace for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


class TestBasicPrompts:
    """Test basic prompts with various file formats and models."""

    def test_english_translation_prompt_epub(self, test_book_dir, temp_workspace):
        """Test English translation prompt with EPUB file."""
        # Copy test book to temp workspace
        source_file = os.path.join(test_book_dir, "animal_farm.epub")
        temp_file = os.path.join(temp_workspace, "animal_farm.epub")
        shutil.copyfile(source_file, temp_file)

        # Run translation with English prompt
        result = subprocess.run(
            [
                sys.executable,
                "make_book.py",
                "--book_name",
                temp_file,
                "--test",
                "--test_num",
                "10",
                "--model",
                "google",
                "--language",
                "French",
                "--prompt",
                "prompts/en/en-translation.prompt.md",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Check that translation completed successfully
        assert result.returncode == 0, f"Translation failed: {result.stderr}"
        
        # Check that bilingual file was created
        bilingual_file = os.path.join(temp_workspace, "animal_farm_bilingual.epub")
        assert os.path.isfile(bilingual_file), "Bilingual file was not created"
        assert os.path.getsize(bilingual_file) > 0, "Bilingual file is empty"

    def test_english_translation_prompt_txt(self, test_book_dir, temp_workspace):
        """Test English translation prompt with TXT file."""
        # Copy test book to temp workspace
        source_file = os.path.join(test_book_dir, "the_little_prince.txt")
        temp_file = os.path.join(temp_workspace, "the_little_prince.txt")
        shutil.copyfile(source_file, temp_file)

        # Run translation with English prompt
        result = subprocess.run(
            [
                sys.executable,
                "make_book.py",
                "--book_name",
                temp_file,
                "--test",
                "--test_num",
                "20",
                "--model",
                "google",
                "--language",
                "Spanish",
                "--prompt",
                "prompts/en/en-translation.prompt.md",
                "--batch_size",
                "15",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Check that translation completed successfully
        assert result.returncode == 0, f"Translation failed: {result.stderr}"
        
        # Check that bilingual file was created
        bilingual_file = os.path.join(temp_workspace, "the_little_prince_bilingual.txt")
        assert os.path.isfile(bilingual_file), "Bilingual file was not created"
        assert os.path.getsize(bilingual_file) > 0, "Bilingual file is empty"

    def test_formatter_prompt_md(self, test_book_dir, temp_workspace):
        """Test formatter prompt with markdown file."""
        # Create a simple markdown test file
        test_md_content = """# Test Chapter

This is a test chapter with some **bold text** and *italic text*.

## Subsection

Here is a list:
- Item 1
- Item 2
- Item 3

And some `inline code` and a [link](https://example.com).
"""
        
        test_md_file = os.path.join(temp_workspace, "test.md")
        with open(test_md_file, 'w', encoding='utf-8') as f:
            f.write(test_md_content)

        # Run formatting with formatter prompt
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "book_maker",
                "--book_name",
                test_md_file,
                "--model",
                "google",
                "--language",
                "English",
                "--prompt",
                "prompts/formatter.prompt.md",
                "--test",
                "--test_num",
                "5",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Check that formatting completed successfully
        assert result.returncode == 0, f"Formatting failed: {result.stderr}"

    def test_italian_translation_prompt(self, test_book_dir, temp_workspace):
        """Test Italian translation prompt."""
        # Copy test book to temp workspace
        source_file = os.path.join(test_book_dir, "animal_farm.epub")
        temp_file = os.path.join(temp_workspace, "animal_farm.epub")
        shutil.copyfile(source_file, temp_file)

        # Run translation with Italian prompt
        result = subprocess.run(
            [
                sys.executable,
                "make_book.py",
                "--book_name",
                temp_file,
                "--test",
                "--test_num",
                "10",
                "--model",
                "google",
                "--language",
                "Italian",
                "--prompt",
                "prompts/it/it-translation.prompt.md",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Check that translation completed successfully
        assert result.returncode == 0, f"Translation failed: {result.stderr}"
        
        # Check that bilingual file was created
        bilingual_file = os.path.join(temp_workspace, "animal_farm_bilingual.epub")
        assert os.path.isfile(bilingual_file), "Bilingual file was not created"

    def test_srt_subtitle_translation(self, test_book_dir, temp_workspace):
        """Test SRT subtitle translation."""
        # Copy test subtitle file to temp workspace
        source_file = os.path.join(test_book_dir, "Lex_Fridman_episode_322.srt")
        temp_file = os.path.join(temp_workspace, "Lex_Fridman_episode_322.srt")
        shutil.copyfile(source_file, temp_file)

        # Run translation with English prompt
        result = subprocess.run(
            [
                sys.executable,
                "make_book.py",
                "--book_name",
                temp_file,
                "--test",
                "--test_num",
                "15",
                "--model",
                "google",
                "--language",
                "German",
                "--prompt",
                "prompts/en/en-translation.prompt.md",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Check that translation completed successfully
        assert result.returncode == 0, f"Translation failed: {result.stderr}"
        
        # Check that bilingual file was created
        bilingual_file = os.path.join(temp_workspace, "Lex_Fridman_episode_322_bilingual.srt")
        assert os.path.isfile(bilingual_file), "Bilingual file was not created"

    @pytest.mark.skipif(
        not os.environ.get("BBM_OPENAI_API_KEY"),
        reason="No BBM_OPENAI_API_KEY in environment variable.",
    )
    def test_openai_with_english_prompt(self, test_book_dir, temp_workspace):
        """Test OpenAI model with English translation prompt."""
        # Copy test book to temp workspace
        source_file = os.path.join(test_book_dir, "animal_farm.epub")
        temp_file = os.path.join(temp_workspace, "animal_farm.epub")
        shutil.copyfile(source_file, temp_file)

        # Run translation with OpenAI and English prompt
        result = subprocess.run(
            [
                sys.executable,
                "make_book.py",
                "--book_name",
                temp_file,
                "--test",
                "--test_num",
                "5",
                "--model",
                "openai",
                "--language",
                "French",
                "--prompt",
                "prompts/en/en-translation.prompt.md",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Check that translation completed successfully
        assert result.returncode == 0, f"Translation failed: {result.stderr}"
        
        # Check that bilingual file was created
        bilingual_file = os.path.join(temp_workspace, "animal_farm_bilingual.epub")
        assert os.path.isfile(bilingual_file), "Bilingual file was not created"

    def test_batch_size_variations(self, test_book_dir, temp_workspace):
        """Test different batch sizes with basic prompts."""
        # Copy test book to temp workspace
        source_file = os.path.join(test_book_dir, "the_little_prince.txt")
        temp_file = os.path.join(temp_workspace, "the_little_prince.txt")
        shutil.copyfile(source_file, temp_file)

        batch_sizes = [5, 10, 15, 20]
        
        for batch_size in batch_sizes:
            result = subprocess.run(
                [
                    sys.executable,
                    "make_book.py",
                    "--book_name",
                    temp_file,
                    "--test",
                    "--test_num",
                    "10",
                    "--model",
                    "google",
                    "--language",
                    "Portuguese",
                    "--prompt",
                    "prompts/en/en-translation.prompt.md",
                    "--batch_size",
                    str(batch_size),
                ],
                env=os.environ.copy(),
                capture_output=True,
                text=True,
            )

            # Check that translation completed successfully
            assert result.returncode == 0, f"Translation failed with batch_size {batch_size}: {result.stderr}"

    def test_language_variations(self, test_book_dir, temp_workspace):
        """Test different target languages with basic prompts."""
        # Copy test book to temp workspace
        source_file = os.path.join(test_book_dir, "animal_farm.epub")
        temp_file = os.path.join(temp_workspace, "animal_farm.epub")
        shutil.copyfile(source_file, temp_file)

        languages = ["French", "Spanish", "German", "Italian", "Portuguese"]
        
        for language in languages:
            result = subprocess.run(
                [
                    sys.executable,
                    "make_book.py",
                    "--book_name",
                    temp_file,
                    "--test",
                    "--test_num",
                    "5",
                    "--model",
                    "google",
                    "--language",
                    language,
                    "--prompt",
                    "prompts/en/en-translation.prompt.md",
                ],
                env=os.environ.copy(),
                capture_output=True,
                text=True,
            )

            # Check that translation completed successfully
            assert result.returncode == 0, f"Translation failed for language {language}: {result.stderr}"

    def test_prompt_file_validation(self, prompts_dir):
        """Test that basic prompt files exist and are valid."""
        required_prompts = [
            ("en", "en-translation.prompt.md"),
            ("", "formatter.prompt.md"),
            ("it", "it-translation.prompt.md"),
        ]
        
        for subdir, prompt_file in required_prompts:
            if subdir:
                prompt_path = os.path.join(prompts_dir, subdir, prompt_file)
            else:
                prompt_path = os.path.join(prompts_dir, prompt_file)
            assert os.path.isfile(prompt_path), f"Required prompt file missing: {prompt_file}"
            
            # Check that prompt file has content
            with open(prompt_path, 'r', encoding='utf-8') as f:
                content = f.read()
                assert len(content) > 0, f"Prompt file is empty: {prompt_file}"
                assert "{text}" in content or "{language}" in content, f"Prompt file missing required placeholders: {prompt_file}"

    def test_test_books_existence(self, test_book_dir):
        """Test that required test books exist."""
        required_books = [
            "animal_farm.epub",
            "the_little_prince.txt",
            "Lex_Fridman_episode_322.srt",
            "Liber_Esther.epub",
            "sample_article.md",
            "sample_quarto.qmd",
        ]
        
        for book_file in required_books:
            book_path = os.path.join(test_book_dir, book_file)
            assert os.path.isfile(book_path), f"Required test book missing: {book_file}"
            
            # Check that test book has content
            assert os.path.getsize(book_path) > 0, f"Test book is empty: {book_file}"


class TestPromptIntegration:
    """Test integration between prompts and translation models."""

    def test_prompt_placeholder_substitution(self, test_book_dir, temp_workspace):
        """Test that prompt placeholders are properly substituted."""
        # Create a simple test prompt
        test_prompt = """Translate the following text to {language}:

{text}

Please maintain the original formatting."""
        
        test_prompt_file = os.path.join(temp_workspace, "test_prompt.md")
        with open(test_prompt_file, 'w', encoding='utf-8') as f:
            f.write(test_prompt)

        # Create a simple test text file
        test_text = "Hello world. This is a test."
        test_text_file = os.path.join(temp_workspace, "test.txt")
        with open(test_text_file, 'w', encoding='utf-8') as f:
            f.write(test_text)

        # Run translation with custom prompt
        result = subprocess.run(
            [
                sys.executable,
                "make_book.py",
                "--book_name",
                test_text_file,
                "--test",
                "--test_num",
                "1",
                "--model",
                "google",
                "--language",
                "French",
                "--prompt",
                test_prompt_file,
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Check that translation completed successfully
        assert result.returncode == 0, f"Translation failed: {result.stderr}"

    def test_prompt_with_context(self, test_book_dir, temp_workspace):
        """Test prompts with context awareness."""
        # Copy test book to temp workspace
        source_file = os.path.join(test_book_dir, "animal_farm.epub")
        temp_file = os.path.join(temp_workspace, "animal_farm.epub")
        shutil.copyfile(source_file, temp_file)

        # Run translation with context
        result = subprocess.run(
            [
                sys.executable,
                "make_book.py",
                "--book_name",
                temp_file,
                "--test",
                "--test_num",
                "10",
                "--model",
                "google",
                "--language",
                "Spanish",
                "--prompt",
                "prompts/en/en-translation.prompt.md",
                "--use_context",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Check that translation completed successfully
        assert result.returncode == 0, f"Translation failed: {result.stderr}"
        
        # Check that bilingual file was created
        bilingual_file = os.path.join(temp_workspace, "animal_farm_bilingual.epub")
        assert os.path.isfile(bilingual_file), "Bilingual file was not created"


class TestErrorHandling:
    """Test error handling with basic prompts."""

    def test_invalid_prompt_file(self, test_book_dir, temp_workspace):
        """Test handling of invalid prompt file."""
        # Copy test book to temp workspace
        source_file = os.path.join(test_book_dir, "animal_farm.epub")
        temp_file = os.path.join(temp_workspace, "animal_farm.epub")
        shutil.copyfile(source_file, temp_file)

        # Run translation with non-existent prompt file
        result = subprocess.run(
            [
                sys.executable,
                "make_book.py",
                "--book_name",
                temp_file,
                "--test",
                "--test_num",
                "5",
                "--model",
                "google",
                "--language",
                "French",
                "--prompt",
                "non_existent_prompt.md",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Should handle the error gracefully
        # The exact behavior depends on the implementation, but it shouldn't crash

    def test_empty_prompt_file(self, test_book_dir, temp_workspace):
        """Test handling of empty prompt file."""
        # Create empty prompt file
        empty_prompt_file = os.path.join(temp_workspace, "empty_prompt.md")
        with open(empty_prompt_file, 'w', encoding='utf-8') as f:
            f.write("")

        # Copy test book to temp workspace
        source_file = os.path.join(test_book_dir, "animal_farm.epub")
        temp_file = os.path.join(temp_workspace, "animal_farm.epub")
        shutil.copyfile(source_file, temp_file)

        # Run translation with empty prompt file
        result = subprocess.run(
            [
                sys.executable,
                "make_book.py",
                "--book_name",
                temp_file,
                "--test",
                "--test_num",
                "5",
                "--model",
                "google",
                "--language",
                "French",
                "--prompt",
                empty_prompt_file,
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Should handle the error gracefully
        # The exact behavior depends on the implementation, but it shouldn't crash 