#!/usr/bin/env python3
"""
Test runner for Bilingual Book Maker.

This script provides a convenient way to run the comprehensive test suite
with different configurations and options.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def run_tests(test_type: str = "all", verbose: bool = False, coverage: bool = False):
    """Run tests with specified configuration."""
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    
    # Change to project root
    os.chdir(project_root)
    
    # Build pytest command
    cmd = [sys.executable, "-m", "pytest"]
    
    # Add test type filters
    if test_type == "unit":
        cmd.extend(["-m", "unit"])
    elif test_type == "integration":
        cmd.extend(["-m", "integration"])
    elif test_type == "api":
        cmd.extend(["-m", "api"])
    elif test_type == "basic":
        cmd.extend(["tests/test_basic_prompts.py"])
    elif test_type == "cli":
        cmd.extend(["tests/test_cli_commands.py"])
    elif test_type == "integration_old":
        cmd.extend(["tests/test_integration.py"])
    elif test_type == "markdown":
        cmd.extend(["tests/test_markdown_files.py"])
    elif test_type != "all":
        print(f"Unknown test type: {test_type}")
        return False
    
    # Add verbosity
    if verbose:
        cmd.append("-v")
    
    # Add coverage
    if coverage:
        cmd.extend(["--cov=book_maker", "--cov-report=html", "--cov-report=term"])
    
    # Add test directory
    cmd.append("tests/")
    
    print(f"Running tests with command: {' '.join(cmd)}")
    
    # Run tests
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Tests failed with return code: {e.returncode}")
        return False


def check_environment():
    """Check if the test environment is properly set up."""
    print("Checking test environment...")
    
    # Check required directories
    required_dirs = ["test_books", "prompts", "tests"]
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            print(f"❌ Missing required directory: {dir_name}")
            return False
        else:
            print(f"✅ Found directory: {dir_name}")
    
    # Check required test books
    required_books = [
        "test_books/animal_farm.epub",
        "test_books/the_little_prince.txt",
        "test_books/Lex_Fridman_episode_322.srt",
        "test_books/Liber_Esther.epub",
    ]
    
    for book_path in required_books:
        if not os.path.exists(book_path):
            print(f"❌ Missing required test book: {book_path}")
            return False
        else:
            print(f"✅ Found test book: {book_path}")
    
    # Check required prompts
    required_prompts = [
        "prompts/en/en-translation.prompt.md",
        "prompts/formatter.prompt.md",
        "prompts/it/it-translation.prompt.md",
    ]
    
    for prompt_path in required_prompts:
        if not os.path.exists(prompt_path):
            print(f"❌ Missing required prompt: {prompt_path}")
            return False
        else:
            print(f"✅ Found prompt: {prompt_path}")
    
    # Check test files
    required_tests = [
        "tests/test_basic_prompts.py",
        "tests/test_cli_commands.py",
        "tests/test_integration.py",
        "tests/test_markdown_files.py",
        "tests/conftest.py",
    ]
    
    for test_path in required_tests:
        if not os.path.exists(test_path):
            print(f"❌ Missing required test file: {test_path}")
            return False
        else:
            print(f"✅ Found test file: {test_path}")
    
    print("✅ Test environment is properly set up!")
    return True


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Run Bilingual Book Maker tests")
    parser.add_argument(
        "--type",
        choices=["all", "unit", "integration", "api", "basic", "cli", "integration_old", "markdown"],
        default="all",
        help="Type of tests to run"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--coverage", "-c",
        action="store_true",
        help="Generate coverage report"
    )
    parser.add_argument(
        "--check-env",
        action="store_true",
        help="Check test environment setup"
    )
    
    args = parser.parse_args()
    
    if args.check_env:
        success = check_environment()
        sys.exit(0 if success else 1)
    
    print(f"Running {args.type} tests...")
    success = run_tests(args.type, args.verbose, args.coverage)
    
    if success:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main() 