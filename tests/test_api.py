#!/usr/bin/env python3
"""
Pytest-compatible API Tests for Book Translation Service
"""

import json
import os
import time
import pytest
import requests
from pathlib import Path
from typing import Dict, Any, Optional

# Configuration
API_BASE_URL = "http://localhost:8000"
TEST_BOOK_PATH = "test_books/the_little_prince.txt"
TEST_PROMPT_PATH = "prompts/it/it-translation.prompt.md"
TEST_MODEL = "o3-mini"
TEST_LANGUAGE = "it"

@pytest.fixture(scope="session")
def api_session():
    """Create a session for API tests"""
    session = requests.Session()
    return session

@pytest.fixture(scope="session")
def service_running():
    """Check if service is running before running tests"""
    try:
        response = requests.get(API_BASE_URL, timeout=5)
        if response.status_code == 200:
            return True
        else:
            pytest.skip("Service not responding properly")
    except requests.exceptions.RequestException:
        pytest.skip("Service not running at http://localhost:8000")

class TestAPIEndpoints:
    """Test API endpoints"""
    
    @pytest.mark.api
    def test_service_info(self, api_session, service_running):
        """Test service information endpoint"""
        response = api_session.get(f"{API_BASE_URL}/")
        assert response.status_code == 200
        
        data = response.json()
        expected_keys = ["service", "version", "docs", "redoc"]
        for key in expected_keys:
            assert key in data, f"Missing key: {key}"
    
    @pytest.mark.api
    def test_models_endpoint(self, api_session, service_running):
        """Test models endpoint"""
        response = api_session.get(f"{API_BASE_URL}/models")
        assert response.status_code == 200
        
        models = response.json()
        assert isinstance(models, list)
        assert len(models) > 0
    
    @pytest.mark.api
    def test_auth_status(self, api_session, service_running):
        """Test authentication status endpoint"""
        response = api_session.get(f"{API_BASE_URL}/auth/status")
        assert response.status_code == 200
        
        data = response.json()
        assert "mock_mode" in data
    
    @pytest.mark.api
    def test_user_info(self, api_session, service_running):
        """Test user info endpoint"""
        response = api_session.get(f"{API_BASE_URL}/auth/user-info")
        assert response.status_code == 200
        
        data = response.json()
        assert "id" in data
        assert "email" in data
    
    @pytest.mark.api
    def test_translate_models(self, api_session, service_running):
        """Test translation models endpoint"""
        response = api_session.get(f"{API_BASE_URL}/translate/models")
        assert response.status_code == 200
        
        models = response.json()
        assert isinstance(models, list)
        assert len(models) > 0
    
    @pytest.mark.api
    def test_languages(self, api_session, service_running):
        """Test languages endpoint"""
        response = api_session.get(f"{API_BASE_URL}/translate/languages")
        assert response.status_code == 200
        
        languages = response.json()
        assert isinstance(languages, list)
        assert len(languages) > 0
    
    @pytest.mark.api
    def test_validate_parameters(self, api_session, service_running):
        """Test parameter validation endpoint"""
        params = {"model": TEST_MODEL, "language": TEST_LANGUAGE}
        response = api_session.get(f"{API_BASE_URL}/translate/validate", params=params)
        assert response.status_code == 200
        
        data = response.json()
        assert "valid" in data

class TestTranslationWorkflow:
    """Test the complete translation workflow"""
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_complete_translation_workflow(self, api_session, service_running):
        """Test the complete translation workflow from start to finish"""
        # Prepare test data
        book_path = os.path.abspath(TEST_BOOK_PATH)
        prompt_file = os.path.abspath(TEST_PROMPT_PATH)
        
        # Verify test files exist
        assert os.path.exists(book_path), f"Test book not found: {book_path}"
        assert os.path.exists(prompt_file), f"Test prompt file not found: {prompt_file}"
        
        # Start translation job
        payload = {
            "book_path": book_path,
            "model": TEST_MODEL,
            "language": TEST_LANGUAGE,
            "model_list": TEST_MODEL,
            "batch_size": 5,
            "single_translate": True,
            "test_mode": True,
            "test_num": 3,
            "prompt_file": prompt_file
        }
        
        response = api_session.post(
            f"{API_BASE_URL}/translate/start",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "job_id" in data
        assert "status" in data
        
        job_id = data["job_id"]
        
        # Monitor job status
        max_wait = 60  # 60 seconds timeout
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            response = api_session.get(f"{API_BASE_URL}/translate/jobs")
            assert response.status_code == 200
            
            jobs = response.json().get("jobs", [])
            
            # Find our job
            job = None
            for j in jobs:
                if j.get("job_id") == job_id:
                    job = j
                    break
            
            assert job is not None, f"Job {job_id} not found in jobs list"
            
            status = job.get("status")
            progress = job.get("progress", 0)
            
            if status == "completed":
                result = job.get("result", {})
                assert result.get("success"), f"Translation failed: {result.get('message', 'Unknown error')}"
                
                # Verify output file
                output_file = result.get("output_file", "")
                assert output_file, "No output file specified in result"
                assert os.path.exists(output_file), f"Output file not found: {output_file}"
                
                # Check file content
                with open(output_file, 'r', encoding='utf-8') as f:
                    content = f.read(500)
                    assert len(content) > 0, "Output file is empty"
                    # Check for Italian content
                    assert any(word in content.lower() for word in ["principe", "piccolo", "italiano"]), \
                        "Output file doesn't contain expected Italian content"
                
                return  # Test passed
                
            elif status == "failed":
                error = job.get("error", "Unknown error")
                pytest.fail(f"Job failed: {error}")
            
            time.sleep(2)  # Wait 2 seconds before checking again
        
        pytest.fail(f"Job did not complete within {max_wait} seconds")

class TestErrorHandling:
    """Test error handling scenarios"""
    
    @pytest.mark.api
    def test_invalid_model(self, api_session, service_running):
        """Test validation with invalid model"""
        params = {"model": "invalid-model", "language": TEST_LANGUAGE}
        response = api_session.get(f"{API_BASE_URL}/translate/validate", params=params)
        assert response.status_code == 200
        
        data = response.json()
        assert "valid" in data
        # Should be invalid for invalid model
        assert not data.get("valid", True)
    
    @pytest.mark.api
    def test_missing_parameters(self, api_session, service_running):
        """Test validation with missing parameters"""
        response = api_session.get(f"{API_BASE_URL}/translate/validate")
        # Should handle missing parameters gracefully
        assert response.status_code in [200, 400, 422]
    
    @pytest.mark.api
    def test_nonexistent_job(self, api_session, service_running):
        """Test getting a non-existent job"""
        response = api_session.get(f"{API_BASE_URL}/translate/jobs/nonexistent-job-id")
        assert response.status_code == 404

def run_standalone_tests(verbose=False):
    """Run tests in standalone mode (without pytest)"""
    print("=" * 60)
    print("API TEST SUITE - Book Translation Service")
    print("=" * 60)
    print()
    
    # Import the original test logic
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    
    # Import and run the original test logic
    from test_api_original import APITester
    
    tester = APITester()
    results = tester.run_all_tests()
    
    # Exit with appropriate code
    if results["failed"] > 0:
        sys.exit(1)
    else:
        print("🎉 All tests passed!")
        sys.exit(0)

if __name__ == "__main__":
    # Allow running as standalone script
    pytest.main([__file__, "-v"]) 