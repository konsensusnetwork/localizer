# API Testing Guide

This guide explains how to test the Book Translation Service API using curl commands.

## Overview

The Book Translation Service is a backend-only API built with FastAPI. It provides endpoints for:
- Authentication (with mock mode for development)
- Translation job management
- Model and language validation
- Real-time job status tracking

## Prerequisites

1. **Start the API Server**
   ```bash
   uvicorn my_app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Required Tools**
   - `curl` (for API testing)
   - `jq` (optional, for JSON formatting)

## Test Scripts

### 1. Comprehensive Test Suite (`api_curl_tests.sh`)

A complete test suite that covers all API endpoints:

```bash
./api_curl_tests.sh
```

**Features:**
- Tests all API endpoints
- Includes error handling tests
- Performance testing
- Color-coded output
- Detailed logging

### 2. Quick Tests (`api_quick_tests.sh`)

A simplified test script for quick validation:

```bash
./api_quick_tests.sh
```

**Features:**
- Essential endpoint tests
- Shows both commands and responses
- Quick validation of API functionality

## Manual Testing

### Basic Endpoints

#### 1. Service Information
```bash
curl http://localhost:8000/
```

Expected response:
```json
{
  "service": "Book Translation Service",
  "version": "1.0.0",
  "docs": "/docs",
  "redoc": "/redoc"
}
```

#### 2. Get Supported Models
```bash
curl http://localhost:8000/models
```

#### 3. Authentication Status
```bash
curl http://localhost:8000/auth/status
```

Expected response:
```json
{
  "supabase_available": false,
  "supabase_configured": false,
  "mock_mode": true
}
```

### Authentication Endpoints

#### 1. Get User Info (Mock Mode)
```bash
curl http://localhost:8000/auth/user-info
```

#### 2. Test Authentication
```bash
curl -X POST http://localhost:8000/auth/test-auth
```

#### 3. With Authentication Token
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/auth/user-info
```

### Translation Endpoints

#### 1. Validate Translation Parameters
```bash
curl "http://localhost:8000/translate/validate?model=openai&language=zh-hans"
```

#### 2. Start Translation Job
```bash
curl -X POST http://localhost:8000/translate/start \
  -H "Content-Type: application/json" \
  -d '{
    "book_path": "/path/to/book.epub",
    "model": "openai",
    "language": "zh-hans",
    "test_mode": true,
    "test_num": 5
  }'
```

#### 3. Get All Translation Jobs
```bash
curl http://localhost:8000/translate/jobs
```

#### 4. Get Specific Job Status
```bash
curl http://localhost:8000/translate/jobs/JOB_ID
```

## API Request Examples

### Minimal Translation Request
```bash
curl -X POST http://localhost:8000/translate/start \
  -H "Content-Type: application/json" \
  -d '{
    "book_path": "/workspace/books/test_book.epub",
    "model": "openai",
    "language": "zh-hans"
  }'
```

### Full Translation Request
```bash
curl -X POST http://localhost:8000/translate/start \
  -H "Content-Type: application/json" \
  -d '{
    "book_path": "/workspace/books/test_book.epub",
    "model": "openai",
    "language": "zh-hans",
    "model_list": "openai,claude",
    "batch_size": 10,
    "single_translate": false,
    "test_mode": true,
    "test_num": 3,
    "use_context": true,
    "reasoning_effort": "high",
    "temperature": 0.7,
    "accumulated_num": 2,
    "block_size": 100,
    "prompt_file": "/workspace/prompts/custom_prompt.txt",
    "user_id": "test_user"
  }'
```

## Response Formats

### Translation Job Response
```json
{
  "job_id": "uuid-job-id",
  "status": "started",
  "message": "Translation job started"
}
```

### Job Status Response
```json
{
  "job_id": "uuid-job-id",
  "status": "running",
  "progress": 45,
  "message": "Translation in progress",
  "result": null,
  "error": null
}
```

### Error Response
```json
{
  "detail": "Error message description"
}
```

## Configuration

### Test Configuration
Edit the configuration variables in the test scripts:

```bash
# Configuration in test scripts
API_BASE_URL="http://localhost:8000"
TEST_BOOK_PATH="/workspace/books/test_book.epub"
TEST_MODEL="openai"
TEST_LANGUAGE="zh-hans"
AUTH_TOKEN=""  # Add your token here if testing with authentication
```

### Supported Models
- `openai` - OpenAI GPT models
- `claude` - Anthropic Claude
- `gemini` - Google Gemini
- `groq` - Groq API
- `caiyun` - Caiyun Translation
- `deepl` - DeepL Translation

### Supported Languages
- `zh-hans` - Chinese (Simplified)
- `zh-hant` - Chinese (Traditional)
- `ja` - Japanese
- `ko` - Korean
- `fr` - French
- `es` - Spanish
- `de` - German
- `it` - Italian
- `pt` - Portuguese
- `ru` - Russian

## Interactive Documentation

### Swagger UI
Open in your browser: `http://localhost:8000/docs`

Features:
- Interactive API testing
- Request/response examples
- Authentication testing
- Schema documentation

### ReDoc
Open in your browser: `http://localhost:8000/redoc`

Features:
- Clean documentation format
- Code examples
- Detailed schemas

## Authentication Modes

### Mock Mode (Development)
- No authentication required
- Uses mock user credentials
- Automatically enabled when Supabase is not configured

### Supabase Mode (Production)
- Requires valid JWT tokens
- Bearer token authentication
- User isolation and security

## Error Handling

### Common HTTP Status Codes
- `200` - Success
- `400` - Bad Request (validation errors)
- `401` - Unauthorized (authentication required)
- `404` - Not Found (resource not found)
- `500` - Internal Server Error

### Testing Error Scenarios

#### 1. Invalid Model
```bash
curl "http://localhost:8000/translate/validate?model=invalid_model&language=zh-hans"
```

#### 2. Missing Required Fields
```bash
curl -X POST http://localhost:8000/translate/start \
  -H "Content-Type: application/json" \
  -d '{"model": "openai"}'
```

#### 3. Invalid Job ID
```bash
curl http://localhost:8000/translate/jobs/invalid-job-id
```

## Troubleshooting

### Common Issues

1. **Server Not Running**
   ```bash
   curl: (7) Failed to connect to localhost port 8000: Connection refused
   ```
   **Solution:** Start the server with `uvicorn my_app.main:app --reload`

2. **JSON Parsing Error**
   ```bash
   curl: (3) URL using bad/illegal format or missing URL
   ```
   **Solution:** Check JSON syntax and proper quoting

3. **Authentication Fails**
   ```json
   {"detail": "No token provided"}
   ```
   **Solution:** In mock mode, no token is required. In production, provide valid JWT token.

4. **File Not Found**
   ```json
   {"detail": "File not found: /path/to/book.epub"}
   ```
   **Solution:** Check file path and permissions

### Debug Tips

1. **Add Verbose Output**
   ```bash
   curl -v http://localhost:8000/
   ```

2. **Check Response Headers**
   ```bash
   curl -I http://localhost:8000/
   ```

3. **Pretty Print JSON**
   ```bash
   curl http://localhost:8000/ | jq '.'
   ```

4. **Save Response to File**
   ```bash
   curl http://localhost:8000/ > response.json
   ```

## Test Automation

### Running All Tests
```bash
# Run comprehensive test suite
./api_curl_tests.sh

# Run quick tests
./api_quick_tests.sh

# Run specific test
curl http://localhost:8000/auth/status
```

### Integration with CI/CD
```bash
# Example test pipeline
#!/bin/bash
set -e

# Start server
uvicorn my_app.main:app --host 0.0.0.0 --port 8000 &
SERVER_PID=$!

# Wait for server to start
sleep 5

# Run tests
./api_curl_tests.sh

# Stop server
kill $SERVER_PID
```

## Performance Testing

### Concurrent Requests
```bash
# Test concurrent requests
for i in {1..10}; do
  curl -s http://localhost:8000/ &
done
wait
```

### Load Testing with curl
```bash
# Simple load test
time for i in {1..100}; do
  curl -s http://localhost:8000/ > /dev/null
done
```

## Best Practices

1. **Use Test Mode**: Always set `test_mode: true` for development
2. **Check Status**: Monitor job status regularly
3. **Handle Errors**: Always check HTTP status codes
4. **Validate Input**: Use validation endpoints before starting jobs
5. **Use Appropriate Timeouts**: Set reasonable timeout values

## Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review server logs for detailed error information
3. Verify environment configuration
4. Test with minimal configuration first

## File Structure

```
/workspace/
├── api_curl_tests.sh          # Comprehensive test suite
├── api_quick_tests.sh         # Quick test script
├── API_TESTING_README.md      # This file
├── docs/
│   └── FASTAPI_TRANSLATION_SERVICE.md  # API documentation
└── my_app/                    # FastAPI application
    ├── main.py
    ├── routers/
    │   ├── auth.py
    │   └── translate.py
    └── core.py
```

This testing guide provides comprehensive coverage for validating the Book Translation Service API functionality.