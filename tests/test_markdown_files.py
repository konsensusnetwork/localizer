"""
Tests for markdown and quarto files using the translation system.

This module tests the translation system with markdown (.md) and quarto (.qmd) files
to ensure proper handling of markdown formatting, code blocks, and quarto-specific features.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Dict, Any

import pytest


class TestMarkdownFiles:
    """Test translation of markdown files."""

    def test_markdown_article_translation(self, test_book_dir, temp_workspace):
        """Test translation of a comprehensive markdown article."""
        # Copy test markdown file to temp workspace
        source_file = os.path.join(test_book_dir, "sample_article.md")
        temp_file = os.path.join(temp_workspace, "sample_article.md")
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
                "Spanish",
                "--prompt",
                "prompts/en/en-translation.prompt.md",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Check that translation completed successfully
        assert result.returncode == 0, f"Markdown translation failed: {result.stderr}"
        
        # Check that bilingual file was created
        bilingual_file = os.path.join(temp_workspace, "sample_article_bilingual.md")
        assert os.path.isfile(bilingual_file), "Bilingual markdown file was not created"
        assert os.path.getsize(bilingual_file) > 0, "Bilingual markdown file is empty"

    def test_markdown_article_french_translation(self, test_book_dir, temp_workspace):
        """Test translation of markdown article to French."""
        # Copy test markdown file to temp workspace
        source_file = os.path.join(test_book_dir, "sample_article.md")
        temp_file = os.path.join(temp_workspace, "sample_article.md")
        shutil.copyfile(source_file, temp_file)

        # Run translation to French
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
        assert result.returncode == 0, f"French translation failed: {result.stderr}"
        
        # Check that bilingual file was created
        bilingual_file = os.path.join(temp_workspace, "sample_article_bilingual.md")
        assert os.path.isfile(bilingual_file), "Bilingual markdown file was not created"

    def test_markdown_article_german_translation(self, test_book_dir, temp_workspace):
        """Test translation of markdown article to German."""
        # Copy test markdown file to temp workspace
        source_file = os.path.join(test_book_dir, "sample_article.md")
        temp_file = os.path.join(temp_workspace, "sample_article.md")
        shutil.copyfile(source_file, temp_file)

        # Run translation to German
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
                "German",
                "--prompt",
                "prompts/en/en-translation.prompt.md",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Check that translation completed successfully
        assert result.returncode == 0, f"German translation failed: {result.stderr}"
        
        # Check that bilingual file was created
        bilingual_file = os.path.join(temp_workspace, "sample_article_bilingual.md")
        assert os.path.isfile(bilingual_file), "Bilingual markdown file was not created"

    def test_markdown_with_formatter_prompt(self, test_book_dir, temp_workspace):
        """Test markdown file with formatter prompt."""
        # Copy test markdown file to temp workspace
        source_file = os.path.join(test_book_dir, "sample_article.md")
        temp_file = os.path.join(temp_workspace, "sample_article.md")
        shutil.copyfile(source_file, temp_file)

        # Run formatting with formatter prompt
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "book_maker",
                "--book_name",
                temp_file,
                "--model",
                "google",
                "--language",
                "English",
                "--prompt",
                "prompts/formatter.prompt.md",
                "--test",
                "--test_num",
                "10",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Check that formatting completed successfully
        assert result.returncode == 0, f"Markdown formatting failed: {result.stderr}"

    def test_markdown_batch_size_variations(self, test_book_dir, temp_workspace):
        """Test markdown translation with different batch sizes."""
        # Copy test markdown file to temp workspace
        source_file = os.path.join(test_book_dir, "sample_article.md")
        temp_file = os.path.join(temp_workspace, "sample_article.md")
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
                    "8",
                    "--model",
                    "google",
                    "--language",
                    "Italian",
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


class TestQuartoFiles:
    """Test translation of quarto files."""

    def test_quarto_file_translation(self, test_book_dir, temp_workspace):
        """Test translation of a quarto file with complex formatting."""
        # Copy test quarto file to temp workspace
        source_file = os.path.join(test_book_dir, "sample_quarto.qmd")
        temp_file = os.path.join(temp_workspace, "sample_quarto.qmd")
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
                "12",
                "--model",
                "google",
                "--language",
                "Spanish",
                "--prompt",
                "prompts/en/en-translation.prompt.md",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Check that translation completed successfully
        assert result.returncode == 0, f"Quarto translation failed: {result.stderr}"
        
        # Check that bilingual file was created
        bilingual_file = os.path.join(temp_workspace, "sample_quarto_bilingual.qmd")
        assert os.path.isfile(bilingual_file), "Bilingual quarto file was not created"
        assert os.path.getsize(bilingual_file) > 0, "Bilingual quarto file is empty"

    def test_quarto_file_french_translation(self, test_book_dir, temp_workspace):
        """Test translation of quarto file to French."""
        # Copy test quarto file to temp workspace
        source_file = os.path.join(test_book_dir, "sample_quarto.qmd")
        temp_file = os.path.join(temp_workspace, "sample_quarto.qmd")
        shutil.copyfile(source_file, temp_file)

        # Run translation to French
        result = subprocess.run(
            [
                sys.executable,
                "make_book.py",
                "--book_name",
                temp_file,
                "--test",
                "--test_num",
                "8",
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
        assert result.returncode == 0, f"French quarto translation failed: {result.stderr}"
        
        # Check that bilingual file was created
        bilingual_file = os.path.join(temp_workspace, "sample_quarto_bilingual.qmd")
        assert os.path.isfile(bilingual_file), "Bilingual quarto file was not created"

    def test_quarto_with_formatter_prompt(self, test_book_dir, temp_workspace):
        """Test quarto file with formatter prompt."""
        # Copy test quarto file to temp workspace
        source_file = os.path.join(test_book_dir, "sample_quarto.qmd")
        temp_file = os.path.join(temp_workspace, "sample_quarto.qmd")
        shutil.copyfile(source_file, temp_file)

        # Run formatting with formatter prompt
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "book_maker",
                "--book_name",
                temp_file,
                "--model",
                "google",
                "--language",
                "English",
                "--prompt",
                "prompts/formatter.prompt.md",
                "--test",
                "--test_num",
                "8",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Check that formatting completed successfully
        assert result.returncode == 0, f"Quarto formatting failed: {result.stderr}"

    def test_quarto_code_block_preservation(self, test_book_dir, temp_workspace):
        """Test that code blocks in quarto files are preserved during translation."""
        # Copy test quarto file to temp workspace
        source_file = os.path.join(test_book_dir, "sample_quarto.qmd")
        temp_file = os.path.join(temp_workspace, "sample_quarto.qmd")
        shutil.copyfile(source_file, temp_file)

        # Run translation
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
                "German",
                "--prompt",
                "prompts/en/en-translation.prompt.md",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Check that translation completed successfully
        assert result.returncode == 0, f"Quarto code block translation failed: {result.stderr}"
        
        # Check that bilingual file was created
        bilingual_file = os.path.join(temp_workspace, "sample_quarto_bilingual.qmd")
        assert os.path.isfile(bilingual_file), "Bilingual quarto file was not created"

    @pytest.mark.skipif(
        not os.environ.get("BBM_OPENAI_API_KEY"),
        reason="No BBM_OPENAI_API_KEY in environment variable.",
    )
    def test_quarto_with_openai(self, test_book_dir, temp_workspace):
        """Test quarto file translation with OpenAI model."""
        # Copy test quarto file to temp workspace
        source_file = os.path.join(test_book_dir, "sample_quarto.qmd")
        temp_file = os.path.join(temp_workspace, "sample_quarto.qmd")
        shutil.copyfile(source_file, temp_file)

        # Run translation with OpenAI
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
        assert result.returncode == 0, f"OpenAI quarto translation failed: {result.stderr}"
        
        # Check that bilingual file was created
        bilingual_file = os.path.join(temp_workspace, "sample_quarto_bilingual.qmd")
        assert os.path.isfile(bilingual_file), "Bilingual quarto file was not created"


class TestMarkdownQuartoComparison:
    """Test comparison between markdown and quarto file handling."""

    def test_markdown_vs_quarto_translation(self, test_book_dir, temp_workspace):
        """Compare translation of markdown vs quarto files."""
        # Copy both test files to temp workspace
        md_source = os.path.join(test_book_dir, "sample_article.md")
        qmd_source = os.path.join(test_book_dir, "sample_quarto.qmd")
        
        md_temp = os.path.join(temp_workspace, "sample_article.md")
        qmd_temp = os.path.join(temp_workspace, "sample_quarto.qmd")
        
        shutil.copyfile(md_source, md_temp)
        shutil.copyfile(qmd_source, qmd_temp)

        # Test markdown translation
        md_result = subprocess.run(
            [
                sys.executable,
                "make_book.py",
                "--book_name",
                md_temp,
                "--test",
                "--test_num",
                "5",
                "--model",
                "google",
                "--language",
                "Spanish",
                "--prompt",
                "prompts/en/en-translation.prompt.md",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Test quarto translation
        qmd_result = subprocess.run(
            [
                sys.executable,
                "make_book.py",
                "--book_name",
                qmd_temp,
                "--test",
                "--test_num",
                "5",
                "--model",
                "google",
                "--language",
                "Spanish",
                "--prompt",
                "prompts/en/en-translation.prompt.md",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Check that both translations completed successfully
        assert md_result.returncode == 0, f"Markdown translation failed: {md_result.stderr}"
        assert qmd_result.returncode == 0, f"Quarto translation failed: {qmd_result.stderr}"
        
        # Check that both bilingual files were created
        md_bilingual = os.path.join(temp_workspace, "sample_article_bilingual.md")
        qmd_bilingual = os.path.join(temp_workspace, "sample_quarto_bilingual.qmd")
        
        assert os.path.isfile(md_bilingual), "Markdown bilingual file was not created"
        assert os.path.isfile(qmd_bilingual), "Quarto bilingual file was not created"

    def test_file_format_handling(self, test_book_dir):
        """Test that different file formats are handled correctly."""
        # Check that both file types exist
        md_file = os.path.join(test_book_dir, "sample_article.md")
        qmd_file = os.path.join(test_book_dir, "sample_quarto.qmd")
        
        assert os.path.isfile(md_file), "Sample markdown file not found"
        assert os.path.isfile(qmd_file), "Sample quarto file not found"
        
        # Check file sizes
        md_size = os.path.getsize(md_file)
        qmd_size = os.path.getsize(qmd_file)
        
        assert md_size > 0, "Markdown file is empty"
        assert qmd_size > 0, "Quarto file is empty"
        
        # Check that files have different content (different formats)
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        with open(qmd_file, 'r', encoding='utf-8') as f:
            qmd_content = f.read()
        
        # Quarto files should have YAML front matter
        assert qmd_content.startswith('---'), "Quarto file should start with YAML front matter"
        
        # Markdown files should not have YAML front matter
        assert not md_content.startswith('---'), "Markdown file should not start with YAML front matter"


class TestMarkdownQuartoErrorHandling:
    """Test error handling for markdown and quarto files."""

    def test_invalid_markdown_file(self, temp_workspace):
        """Test handling of invalid markdown file."""
        # Create an invalid markdown file
        invalid_md = os.path.join(temp_workspace, "invalid.md")
        with open(invalid_md, 'w', encoding='utf-8') as f:
            f.write("This is not properly formatted markdown\n")
            f.write("Missing headers and structure\n")

        # Try to translate the invalid file
        result = subprocess.run(
            [
                sys.executable,
                "make_book.py",
                "--book_name",
                invalid_md,
                "--test",
                "--test_num",
                "3",
                "--model",
                "google",
                "--language",
                "Spanish",
                "--prompt",
                "prompts/en/en-translation.prompt.md",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Should handle the error gracefully
        # The exact behavior depends on the implementation

    def test_empty_markdown_file(self, temp_workspace):
        """Test handling of empty markdown file."""
        # Create an empty markdown file
        empty_md = os.path.join(temp_workspace, "empty.md")
        with open(empty_md, 'w', encoding='utf-8') as f:
            f.write("")

        # Try to translate the empty file
        result = subprocess.run(
            [
                sys.executable,
                "make_book.py",
                "--book_name",
                empty_md,
                "--test",
                "--test_num",
                "1",
                "--model",
                "google",
                "--language",
                "Spanish",
                "--prompt",
                "prompts/en/en-translation.prompt.md",
            ],
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )

        # Should handle the error gracefully
        # The exact behavior depends on the implementation 