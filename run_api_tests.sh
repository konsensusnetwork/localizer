#!/bin/bash

# API Test Runner Script
# This script runs comprehensive tests for the Book Translation Service API

set -e  # Exit on any error

echo "=========================================="
echo "Book Translation Service - API Test Suite"
echo "=========================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if requests module is available
if ! python3 -c "import requests" &> /dev/null; then
    echo "❌ Python requests module is not installed"
    echo "Please install it with: pip install requests"
    exit 1
fi

# Check if service is running
echo "🔍 Checking if service is running..."
if ! curl -s http://localhost:8000/ > /dev/null; then
    echo "❌ Service is not running at http://localhost:8000"
    echo "Please start the service with: python run_service.py"
    exit 1
fi

echo "✅ Service is running"
echo ""

# Run the Python test suite
echo "🧪 Running API tests..."
pytest tests/test_api.py -v

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 All tests passed successfully!"
    exit 0
else
    echo ""
    echo "❌ Some tests failed. Check the output above for details."
    exit 1
fi 