#!/usr/bin/env python3
"""
Test script to trigger a translation request and monitor logs
"""
import requests
import json
import time
import os

def test_translation_request():
    """Test the translation endpoint"""
    base_url = "http://localhost:8000"
    
    # Test data
    test_data = {
        "book_path": "books/bm-it/ch01.md",
        "model": "o3mini",
        "language": "en",
        "batch_size": 1,
        "single_translate": False,
        "test": True,
        "test_num": 1
    }
    
    print("Testing translation endpoint...")
    print(f"Request data: {json.dumps(test_data, indent=2)}")
    
    try:
        # Make the request
        response = requests.post(
            f"{base_url}/translate/start",
            data=test_data,
            timeout=30
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response body: {json.dumps(result, indent=2)}")
        else:
            print(f"Error response: {response.text}")
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_translation_request() 