"""
Tests for CLI commands using examples from commands.md.

This module tests the command-line interface using real-world examples
from the project's commands documentation.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Dict, Any

import pytest


class TestCLICommands:
    """Test CLI commands using examples from commands.md."""

    def test_bbook_maker_formatter_command(self, test_book_dir, temp_workspace):
        """Test bbook_maker formatter command from commands.md."""
        # Create a test markdown file
        test_md_content = """# Test Document

This is a test document for formatting.

## Section 1

Some content here.

## Section 2

More content with **bold** and *italic* text.
"""
        
        test_md_file = os.path.join(temp_workspace, "21F2_EN_test.md")
        with open(test_md_file, 'w', encoding='utf-8') as f:
            f.write(test_md_content)

        # Test the formatter command from commands.md
        result = subprocess.run(
            [
                "pdm", "run", "bbook_maker",
                "--book_name", test_md_file,
                "--model", "openai",
                "--model_list", "o3-mini",
                "--reasoning_effort=high",
                "--prompt", "prompts/formatter.prompt.md",
                "--batch_size", "12",
                "--single_translate",
                "--language", "en",
                "--test",
                "--test_num", "5",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Check that command completed successfully
        assert result.returncode == 0, f"Formatter command failed: {result.stderr}"

    def test_bbook_maker_italian_command(self, test_book_dir, temp_workspace):
        """Test bbook_maker Italian translation command from commands.md."""
        # Create a test qmd file
        test_qmd_content = """# Chapter 1

This is the first chapter of the book.

## Introduction

Welcome to this book.
"""
        
        test_qmd_file = os.path.join(temp_workspace, "ch01.qmd")
        with open(test_qmd_file, 'w', encoding='utf-8') as f:
            f.write(test_qmd_content)

        # Test the Italian translation command from commands.md
        result = subprocess.run(
            [
                "pdm", "run", "bbook_maker",
                "--book_name", test_qmd_file,
                "--model", "openai",
                "--model_list", "o3-mini",
                "--prompt", "prompts/it/it-translation.prompt.md",
                "--batch_size", "5",
                "--single_translate",
                "--language", "it",
                "--test",
                "--test_num", "3",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Check that command completed successfully
        assert result.returncode == 0, f"Italian translation command failed: {result.stderr}"

    def test_bbook_maker_dutch_command(self, test_book_dir, temp_workspace):
        """Test bbook_maker Dutch translation command from commands.md."""
        # Create a test qmd file
        test_qmd_content = """# Chapter 9

This is chapter nine of the book.

## Content

Some content here.
"""
        
        test_qmd_file = os.path.join(temp_workspace, "ch09.qmd")
        with open(test_qmd_file, 'w', encoding='utf-8') as f:
            f.write(test_qmd_content)

        # Test the Dutch translation command from commands.md
        result = subprocess.run(
            [
                "pdm", "run", "bbook_maker",
                "--book_name", test_qmd_file,
                "--model", "openai",
                "--model_list", "o3-mini",
                "--prompt", "prompts/nl/nl-edit-o3.prompt.md",
                "--batch_size", "5",
                "--single_translate",
                "--language", "nl",
                "--use_context",
                "--reasoning_effort=high",
                "--test",
                "--test_num", "3",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Check that command completed successfully
        assert result.returncode == 0, f"Dutch translation command failed: {result.stderr}"

    def test_dir_process_french_command(self, test_book_dir, temp_workspace):
        """Test dir_process French translation command from commands.md."""
        # Create a test directory structure
        test_dir = os.path.join(temp_workspace, "fr")
        os.makedirs(test_dir, exist_ok=True)
        
        # Create test files in the directory
        for i in range(3):
            test_file = os.path.join(test_dir, f"ch{i:02d}.md")
            test_content = f"""# Chapter {i}

This is chapter {i} content.

## Section {i}

Some content for chapter {i}.
"""
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(test_content)

        # Test the French directory processing command from commands.md
        result = subprocess.run(
            [
                "pdm", "run", "dir_process",
                test_dir,
                "--model", "openai",
                "--model_list", "o3-mini",
                "--reasoning_effort=high",
                "--prompt", "prompts/fr-translation-2.prompt.md",
                "--batch_size", "5",
                "--single_translate",
                "--language", "fr",
                "--test",
                "--test_num", "2",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Check that command completed successfully
        assert result.returncode == 0, f"French directory processing command failed: {result.stderr}"

    def test_dir_process_spanish_command(self, test_book_dir, temp_workspace):
        """Test dir_process Spanish translation command from commands.md."""
        # Create a test directory structure
        test_dir = os.path.join(temp_workspace, "es")
        os.makedirs(test_dir, exist_ok=True)
        
        # Create test files in the directory
        for i in range(3):
            test_file = os.path.join(test_dir, f"ch{i:02d}.md")
            test_content = f"""# Chapter {i}

This is chapter {i} content.

## Section {i}

Some content for chapter {i}.
"""
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(test_content)

        # Test the Spanish directory processing command from commands.md
        result = subprocess.run(
            [
                "pdm", "run", "dir_process",
                test_dir,
                "--model", "openai",
                "--model_list", "o3-mini",
                "--reasoning_effort=high",
                "--prompt", "prompts/es-translation-prompt.md",
                "--batch_size", "5",
                "--single_translate",
                "--language", "es",
                "--test",
                "--test_num", "2",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Check that command completed successfully
        assert result.returncode == 0, f"Spanish directory processing command failed: {result.stderr}"

    def test_make_book_gemini_command(self, test_book_dir, temp_workspace):
        """Test make_book.py Gemini command from commands.md."""
        # Copy test book to temp workspace
        source_file = os.path.join(test_book_dir, "animal_farm.epub")
        temp_file = os.path.join(temp_workspace, "animal_farm.epub")
        shutil.copyfile(source_file, temp_file)

        # Test the basic Gemini translation command from commands.md
        result = subprocess.run(
            [
                sys.executable, "make_book.py",
                "--book_name", temp_file,
                "--model", "gemini",
                "--language", "nl",
                "--test",
                "--test_num", "5",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Check that command completed successfully
        assert result.returncode == 0, f"Gemini translation command failed: {result.stderr}"

    @pytest.mark.skipif(
        not os.environ.get("BBM_GEMINI_API_KEY"),
        reason="No BBM_GEMINI_API_KEY in environment variable.",
    )
    def test_bbook_maker_gemini_dutch_command(self, test_book_dir, temp_workspace):
        """Test bbook_maker Gemini Dutch command from commands.md."""
        # Create a test qmd file
        test_qmd_content = """# Chapter 2

This is chapter two content.

## Introduction

Welcome to chapter two.
"""
        
        test_qmd_file = os.path.join(temp_workspace, "ch02.qmd")
        with open(test_qmd_file, 'w', encoding='utf-8') as f:
            f.write(test_qmd_content)

        # Test the Gemini Dutch translation command from commands.md
        result = subprocess.run(
            [
                "pdm", "run", "bbook_maker",
                "--book_name", test_qmd_file,
                "--model", "gemini",
                "--prompt", "prompts/nl/nl-translation-tsi.prompt.md",
                "--batch_size", "5",
                "--single_translate",
                "--language", "nl",
                "--gemini_key", os.environ.get("BBM_GEMINI_API_KEY", ""),
                "--model_list", "gemini-2.5-pro-preview-06-05",
                "--test",
                "--test_num", "3",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Check that command completed successfully
        assert result.returncode == 0, f"Gemini Dutch translation command failed: {result.stderr}"

    @pytest.mark.skipif(
        not os.environ.get("BBM_GEMINI_API_KEY"),
        reason="No BBM_GEMINI_API_KEY in environment variable.",
    )
    def test_bbook_maker_gemini_albanian_command(self, test_book_dir, temp_workspace):
        """Test bbook_maker Gemini Albanian command from commands.md."""
        # Create a test md file
        test_md_content = """# Chapter 0

This is chapter zero content.

## Introduction

Welcome to chapter zero.
"""
        
        test_md_file = os.path.join(temp_workspace, "ch00.md")
        with open(test_md_file, 'w', encoding='utf-8') as f:
            f.write(test_md_content)

        # Test the Gemini Albanian translation command from commands.md
        result = subprocess.run(
            [
                "pdm", "run", "bbook_maker",
                "--book_name", test_md_file,
                "--model", "gemini",
                "--prompt", "prompts/al-translation.prompt.md",
                "--batch_size", "5",
                "--single_translate",
                "--language", "Albanian",
                "--gemini_key", os.environ.get("BBM_GEMINI_API_KEY", ""),
                "--model_list", "gemini-2.5-pro-preview-06-05",
                "--test",
                "--test_num", "3",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Check that command completed successfully
        assert result.returncode == 0, f"Gemini Albanian translation command failed: {result.stderr}"

    @pytest.mark.skipif(
        not os.environ.get("BBM_GEMINI_API_KEY"),
        reason="No BBM_GEMINI_API_KEY in environment variable.",
    )
    def test_dir_process_gemini_italian_command(self, test_book_dir, temp_workspace):
        """Test dir_process Gemini Italian command from commands.md."""
        # Create a test directory structure
        test_dir = os.path.join(temp_workspace, "todo")
        os.makedirs(test_dir, exist_ok=True)
        
        # Create test files in the directory
        for i in range(3):
            test_file = os.path.join(test_dir, f"ch{i:02d}.md")
            test_content = f"""# Chapter {i}

This is chapter {i} content.

## Section {i}

Some content for chapter {i}.
"""
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(test_content)

        # Test the Gemini Italian directory processing command from commands.md
        result = subprocess.run(
            [
                "pdm", "run", "dir_process",
                test_dir,
                "--model", "gemini",
                "--prompt", "prompts/it-translation-2.prompt.md",
                "--batch_size", "5",
                "--single_translate",
                "--language", "it",
                "--gemini_key", os.environ.get("BBM_GEMINI_API_KEY", ""),
                "--model_list", "gemini-2.5-pro-preview-06-05",
                "--test",
                "--test_num", "2",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Check that command completed successfully
        assert result.returncode == 0, f"Gemini Italian directory processing command failed: {result.stderr}"


class TestCLIErrorHandling:
    """Test CLI error handling scenarios."""

    def test_invalid_model(self, temp_workspace):
        """Test CLI with invalid model."""
        # Create a test file
        test_file = os.path.join(temp_workspace, "test.txt")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Test content")

        # Test with invalid model
        result = subprocess.run(
            [
                sys.executable, "make_book.py",
                "--book_name", test_file,
                "--model", "invalid_model",
                "--language", "French",
                "--test",
                "--test_num", "1",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Should handle the error gracefully
        # The exact behavior depends on the implementation

    def test_missing_file(self, temp_workspace):
        """Test CLI with missing file."""
        # Test with non-existent file
        result = subprocess.run(
            [
                sys.executable, "make_book.py",
                "--book_name", "non_existent_file.txt",
                "--model", "google",
                "--language", "French",
                "--test",
                "--test_num", "1",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Should handle the error gracefully
        # The exact behavior depends on the implementation

    def test_invalid_language(self, temp_workspace):
        """Test CLI with invalid language."""
        # Create a test file
        test_file = os.path.join(temp_workspace, "test.txt")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Test content")

        # Test with invalid language
        result = subprocess.run(
            [
                sys.executable, "make_book.py",
                "--book_name", test_file,
                "--model", "google",
                "--language", "InvalidLanguage",
                "--test",
                "--test_num", "1",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Should handle the error gracefully
        # The exact behavior depends on the implementation


class TestCLIParameters:
    """Test CLI parameter variations."""

    def test_batch_size_variations(self, test_book_dir, temp_workspace):
        """Test different batch sizes."""
        # Copy test book to temp workspace
        source_file = os.path.join(test_book_dir, "the_little_prince.txt")
        temp_file = os.path.join(temp_workspace, "the_little_prince.txt")
        shutil.copyfile(source_file, temp_file)

        batch_sizes = [5, 10, 15, 20]
        
        for batch_size in batch_sizes:
            result = subprocess.run(
                [
                    sys.executable, "make_book.py",
                    "--book_name", temp_file,
                    "--model", "google",
                    "--language", "French",
                    "--batch_size", str(batch_size),
                    "--test",
                    "--test_num", "5",
                ],
                env=os.environ.copy(),
                capture_output=True,
                text=True,
            )

            # Check that command completed successfully
            assert result.returncode == 0, f"Command failed with batch_size {batch_size}: {result.stderr}"

    def test_language_variations(self, test_book_dir, temp_workspace):
        """Test different target languages."""
        # Copy test book to temp workspace
        source_file = os.path.join(test_book_dir, "animal_farm.epub")
        temp_file = os.path.join(temp_workspace, "animal_farm.epub")
        shutil.copyfile(source_file, temp_file)

        languages = ["French", "Spanish", "German", "Italian", "Portuguese"]
        
        for language in languages:
            result = subprocess.run(
                [
                    sys.executable, "make_book.py",
                    "--book_name", temp_file,
                    "--model", "google",
                    "--language", language,
                    "--test",
                    "--test_num", "3",
                ],
                env=os.environ.copy(),
                capture_output=True,
                text=True,
            )

            # Check that command completed successfully
            assert result.returncode == 0, f"Command failed for language {language}: {result.stderr}"

    def test_model_variations(self, test_book_dir, temp_workspace):
        """Test different translation models."""
        # Copy test book to temp workspace
        source_file = os.path.join(test_book_dir, "animal_farm.epub")
        temp_file = os.path.join(temp_workspace, "animal_farm.epub")
        shutil.copyfile(source_file, temp_file)

        models = ["google", "deeplfree"]
        
        for model in models:
            result = subprocess.run(
                [
                    sys.executable, "make_book.py",
                    "--book_name", temp_file,
                    "--model", model,
                    "--language", "French",
                    "--test",
                    "--test_num", "3",
                ],
                env=os.environ.copy(),
                capture_output=True,
                text=True,
            )

            # Check that command completed successfully
            assert result.returncode == 0, f"Command failed for model {model}: {result.stderr}" 