#!/usr/bin/env python3
"""
Test script to verify form submission handles all parameters correctly
"""

import requests
import json
import time

def test_form_submission():
    """Test that form submission properly handles all parameters"""
    
    base_url = "http://localhost:8000"
    
    print("Testing Form Submission Parameters...")
    
    # Test 1: Test with model_list parameter (o3-mini)
    print("\n1. Testing model_list parameter (o3-mini)...")
    try:
        form_data = {
            "book_path": "/tmp/test.txt",
            "model": "openai",
            "language": "en",
            "model_list": "o3-mini",
            "prompt": "Test prompt",
            "batch_size": "5",
            "single_translate": "false",
            "test": "false",
            "use_context": "true",
            "reasoning_effort": "high"
        }
        response = requests.post(f"{base_url}/translate/validate", data=form_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Model list parameter accepted. Validation result: {result}")
        else:
            print(f"❌ Model list parameter failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Model list parameter error: {e}")
    
    # Test 2: Test with prompt_file parameter
    print("\n2. Testing prompt_file parameter...")
    try:
        form_data = {
            "book_path": "/tmp/test.txt",
            "model": "openai",
            "language": "en",
            "prompt_file": "en-translation.prompt.md",
            "batch_size": "5",
            "single_translate": "false",
            "test": "false",
            "use_context": "true",
            "reasoning_effort": "medium"
        }
        response = requests.post(f"{base_url}/translate/validate", data=form_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Prompt file parameter accepted. Validation result: {result}")
        else:
            print(f"❌ Prompt file parameter failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Prompt file parameter error: {e}")
    
    # Test 3: Test with custom prompt
    print("\n3. Testing custom prompt parameter...")
    try:
        form_data = {
            "book_path": "/tmp/test.txt",
            "model": "openai",
            "language": "en",
            "prompt": "Custom translation prompt for testing",
            "batch_size": "5",
            "single_translate": "false",
            "test": "false",
            "use_context": "false",
            "reasoning_effort": "low"
        }
        response = requests.post(f"{base_url}/translate/validate", data=form_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Custom prompt parameter accepted. Validation result: {result}")
        else:
            print(f"❌ Custom prompt parameter failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Custom prompt parameter error: {e}")
    
    # Test 4: Test with different reasoning_effort values
    print("\n4. Testing different reasoning_effort values...")
    reasoning_efforts = ["low", "medium", "high", "auto"]
    for effort in reasoning_efforts:
        try:
            form_data = {
                "book_path": "/tmp/test.txt",
                "model": "openai",
                "language": "en",
                "prompt": "Test prompt",
                "batch_size": "5",
                "single_translate": "false",
                "test": "false",
                "use_context": "true",
                "reasoning_effort": effort
            }
            response = requests.post(f"{base_url}/translate/validate", data=form_data)
            if response.status_code == 200:
                print(f"✅ Reasoning effort '{effort}' accepted")
            else:
                print(f"❌ Reasoning effort '{effort}' failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Reasoning effort '{effort}' error: {e}")
    
    # Test 5: Test with use_context parameter
    print("\n5. Testing use_context parameter...")
    for use_context in ["true", "false"]:
        try:
            form_data = {
                "book_path": "/tmp/test.txt",
                "model": "openai",
                "language": "en",
                "prompt": "Test prompt",
                "batch_size": "5",
                "single_translate": "false",
                "test": "false",
                "use_context": use_context,
                "reasoning_effort": "medium"
            }
            response = requests.post(f"{base_url}/translate/validate", data=form_data)
            if response.status_code == 200:
                print(f"✅ Use context '{use_context}' accepted")
            else:
                print(f"❌ Use context '{use_context}' failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Use context '{use_context}' error: {e}")
    
    print("\n✅ Form submission parameter tests completed!")
    return True

if __name__ == "__main__":
    test_form_submission() 