"""
Pytest configuration and shared fixtures for Bilingual Book Maker tests.

This module provides common fixtures and configuration for all test modules.
"""

import os
import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture(scope="session")
def test_book_dir() -> str:
    """Return test book directory path."""
    return str(Path(__file__).parent.parent / "test_books")


@pytest.fixture(scope="session")
def prompts_dir() -> str:
    """Return prompts directory path."""
    return str(Path(__file__).parent.parent / "prompts")


@pytest.fixture(scope="session")
def book_maker_dir() -> str:
    """Return book_maker module directory path."""
    return str(Path(__file__).parent.parent / "book_maker")


@pytest.fixture
def temp_workspace() -> Generator[str, None, None]:
    """Create a temporary workspace for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture(scope="session")
def required_test_books() -> list:
    """Return list of required test books."""
    return [
        "animal_farm.epub",
        "the_little_prince.txt",
        "Lex_Fridman_episode_322.srt",
        "Liber_Esther.epub",
        "sample_article.md",
        "sample_quarto.qmd",
    ]


@pytest.fixture(scope="session")
def required_prompts() -> list:
    """Return list of required basic prompts."""
    return [
        "en-translation.prompt.md",
        "formatter.prompt.md",
        "it-translation.prompt.md",
    ]


@pytest.fixture(scope="session")
def supported_models() -> list:
    """Return list of supported translation models."""
    return [
        "google",
        "openai",
        "gemini",
        "deepl",
        "deeplfree",
        "claude",
        "caiyun",
        "tencentransmart",
        "xai",
        "groq",
    ]


@pytest.fixture(scope="session")
def supported_languages() -> list:
    """Return list of supported target languages."""
    return [
        "French",
        "Spanish",
        "German",
        "Italian",
        "Portuguese",
        "Dutch",
        "Simplified Chinese",
        "Traditional Chinese",
        "Japanese",
        "Korean",
    ]


@pytest.fixture(scope="session")
def supported_formats() -> list:
    """Return list of supported file formats."""
    return [
        ".epub",
        ".txt",
        ".srt",
        ".md",
        ".qmd",
    ]


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow running"
    )
    config.addinivalue_line(
        "markers", "api: marks tests that require API keys"
    )


def pytest_collection_modifyitems(config, items):
    """Add markers to tests based on their names."""
    for item in items:
        # Mark integration tests
        if "integration" in item.name or "test_basic_prompts" in item.name:
            item.add_marker(pytest.mark.integration)
        
        # Mark API tests
        if "openai" in item.name or "api" in item.name:
            item.add_marker(pytest.mark.api)
        
        # Mark slow tests
        if "slow" in item.name or "large" in item.name:
            item.add_marker(pytest.mark.slow)
        
        # Mark unit tests
        if "unit" in item.name or "validation" in item.name:
            item.add_marker(pytest.mark.unit)
        
        # Mark markdown tests
        if "markdown" in item.name:
            item.add_marker(pytest.mark.markdown) 