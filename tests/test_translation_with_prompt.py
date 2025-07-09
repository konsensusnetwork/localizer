#!/usr/bin/env python3
"""
Test script to trigger a translation request with a PromptDown file
"""
import requests
import json
import time
import os

def test_translation_with_promptdown():
    """Test the translation endpoint with a PromptDown file"""
    base_url = "http://localhost:8000"
    
    # Test data with a PromptDown file
    test_data = {
        "book_path": "books/bm-it/ch01.md",
        "model": "o3mini",
        "language": "en",
        "batch_size": 1,
        "single_translate": False,
        "test": True,
        "test_num": 1,
        "prompt": "prompts/fr/fr-translate.prompt.md"  # Use a PromptDown file
    }
    
    print("Testing translation endpoint with PromptDown file...")
    print(f"Request data: {json.dumps(test_data, indent=2)}")
    
    try:
        # Make the request
        response = requests.post(
            f"{base_url}/translate/start",
            data=test_data,
            timeout=60
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response body: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            job_data = response.json()
            job_id = job_data.get("job_id")
            
            if job_id:
                print(f"\nJob started with ID: {job_id}")
                print("Waiting for job to complete...")
                
                # Wait for job completion
                max_wait = 120  # 2 minutes
                wait_time = 0
                while wait_time < max_wait:
                    time.sleep(5)
                    wait_time += 5
                    
                    # Check job status
                    status_response = requests.get(f"{base_url}/translate/jobs")
                    if status_response.status_code == 200:
                        jobs = status_response.json().get("jobs", [])
                        for job in jobs:
                            if job.get("job_id") == job_id:
                                status = job.get("status")
                                print(f"Job status: {status}")
                                
                                if status == "completed":
                                    output_file = job.get("output_file")
                                    print(f"Translation completed! Output file: {output_file}")
                                    
                                    # Check if output file exists
                                    if output_file and os.path.exists(output_file):
                                        print(f"Output file exists: {output_file}")
                                        with open(output_file, 'r', encoding='utf-8') as f:
                                            content = f.read()
                                        print(f"Output file content:\n{content}")
                                    else:
                                        print(f"Output file not found: {output_file}")
                                    return
                                elif status == "failed":
                                    error = job.get("error")
                                    print(f"Translation failed: {error}")
                                    return
                                break
                
                print("Job did not complete within timeout")
            else:
                print("No job ID received")
        else:
            print(f"Request failed with status {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_translation_with_promptdown() 