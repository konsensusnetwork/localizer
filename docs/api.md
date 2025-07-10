# API Documentation

The Bilingual Book Maker provides a RESTful API service for programmatic access to translation capabilities.

## Overview

The API service is built with FastAPI and provides endpoints for:
- Starting translation jobs
- Monitoring job progress
- Retrieving supported models and languages
- Authentication and user management

## Base URL

```
http://localhost:8000
```

## Authentication

The API supports multiple authentication methods:

### API Key Authentication
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  http://localhost:8000/translate/models
```

### Session Authentication
```bash
# Login first
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "password"}'

# Use session cookie in subsequent requests
curl -H "Cookie: session=YOUR_SESSION_ID" \
  http://localhost:8000/translate/models
```

## Endpoints

### Health Check

#### GET /
Check service status

**Response:**
```json
{
  "service": "Book Translation Service",
  "version": "1.0.0",
  "docs": "/docs",
  "redoc": "/redoc"
}
```

### Translation Jobs

#### POST /translate/start
Start a new translation job

**Request Body:**
```json
{
  "book_path": "test_books/animal_farm.epub",
  "model": "gpt-3.5-turbo",
  "language": "zh-hans",
  "model_list": "gpt-4,gpt-3.5-turbo",
  "batch_size": 10,
  "single_translate": false,
  "test_mode": true,
  "test_num": 5,
  "use_context": true,
  "reasoning_effort": "medium",
  "temperature": 0.7,
  "accumulated_num": 1,
  "block_size": -1,
  "prompt_file": "custom_prompt.md",
  "user_id": "user123"
}
```

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "started",
  "message": "Translation job started"
}
```

#### GET /translate/jobs
List all translation jobs

**Response:**
```json
{
  "jobs": [
    {
      "job_id": "550e8400-e29b-41d4-a716-446655440000",
      "status": "completed",
      "progress": 100,
      "message": "Translation completed successfully",
      "result": {
        "success": true,
        "output_file": "test_books/animal_farm_bilingual.epub",
        "message": "Translation completed successfully"
      },
      "error": null
    }
  ]
}
```

#### GET /translate/jobs/{job_id}
Get status of a specific translation job

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "running",
  "progress": 45,
  "message": "Translating chapter 3...",
  "result": null,
  "error": null
}
```

### Models and Languages

#### GET /translate/models
Get supported translation models

**Response:**
```json
{
  "openai": [
    "gpt-4",
    "gpt-4-turbo",
    "gpt-4-32k",
    "gpt-3.5-turbo",
    "gpt-4o",
    "gpt-4o-mini",
    "o1-preview",
    "o1-mini",
    "o3-mini"
  ],
  "gemini": [
    "gemini-1.5-flash",
    "gemini-1.5-flash-002",
    "gemini-1.5-pro",
    "gemini-1.5-pro-002",
    "gemini-1.0-pro"
  ]
}
```

#### GET /translate/languages
Get supported languages

**Response:**
```json
{
  "languages": {
    "zh-hans": "simplified chinese",
    "zh-hant": "traditional chinese",
    "ja": "japanese",
    "ko": "korean",
    "fr": "français",
    "de": "german",
    "es": "spanish",
    "it": "italian",
    "pt": "portuguese",
    "ru": "russian",
    "ar": "arabic"
  }
}
```

### Validation

#### GET /translate/validate
Validate translation parameters

**Query Parameters:**
- `model`: Translation model name
- `language`: Target language
- `model_list`: Comma-separated model list
- `prompt_file`: Custom prompt file path

**Response:**
```json
{
  "valid": true,
  "message": "Parameters are valid",
  "warnings": []
}
```

## Usage Examples

### 1. Start a Simple Translation

```bash
curl -X POST "http://localhost:8000/translate/start" \
  -H "Content-Type: application/json" \
  -d '{
    "book_path": "test_books/animal_farm.epub",
    "model": "gpt-3.5-turbo",
    "language": "zh-hans",
    "test_mode": true,
    "test_num": 5
  }'
```

### 2. Start a High-Quality Translation

```bash
curl -X POST "http://localhost:8000/translate/start" \
  -H "Content-Type: application/json" \
  -d '{
    "book_path": "books/1984.epub",
    "model": "gpt-4",
    "language": "fr",
    "use_context": true,
    "temperature": 0.3,
    "single_translate": false
  }'
```

### 3. Monitor Job Progress

```bash
# Start job
JOB_ID=$(curl -X POST "http://localhost:8000/translate/start" \
  -H "Content-Type: application/json" \
  -d '{
    "book_path": "test_books/animal_farm.epub",
    "model": "gpt-3.5-turbo",
    "language": "zh-hans",
    "test_mode": true
  }' | jq -r '.job_id')

# Check status
curl "http://localhost:8000/translate/jobs/$JOB_ID"
```

### 4. Batch Process Multiple Files

```bash
curl -X POST "http://localhost:8000/translate/start" \
  -H "Content-Type: application/json" \
  -d '{
    "book_path": "manuscript/chapters/",
    "model": "gpt-3.5-turbo",
    "language": "es",
    "batch_size": 15
  }'
```

## Error Handling

### Common Error Responses

#### 400 Bad Request
```json
{
  "detail": "Invalid parameters: book_path is required"
}
```

#### 404 Not Found
```json
{
  "detail": "Job not found"
}
```

#### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "model"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Translation failed: API key not provided"
}
```

## Data Models

### TranslationRequest

```python
class TranslationRequest(BaseModel):
    book_path: str
    model: str
    language: str
    model_list: Optional[str] = None
    batch_size: Optional[int] = None
    single_translate: bool = False
    test_mode: bool = False
    test_num: int = 10
    use_context: bool = False
    reasoning_effort: str = "medium"
    temperature: float = 1.0
    accumulated_num: int = 1
    block_size: int = -1
    prompt_file: Optional[str] = None
    user_id: str = "mock_user"
```

### TranslationResponse

```python
class TranslationResponse(BaseModel):
    job_id: str
    status: str
    message: str
```

### Job Status

```python
class JobStatus(BaseModel):
    job_id: str
    status: str  # "running", "completed", "failed"
    progress: int  # 0-100
    message: str
    result: Optional[Dict] = None
    error: Optional[str] = None
```

## Rate Limiting

The API implements rate limiting to prevent abuse:

- **Requests per minute**: 60
- **Requests per hour**: 1000
- **Concurrent jobs**: 10 per user

### Rate Limit Headers

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1640995200
```

## WebSocket Support

For real-time job monitoring, WebSocket endpoints are available:

### WebSocket Connection

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/jobs/{job_id}');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Job update:', data);
};
```

### WebSocket Messages

```json
{
  "type": "progress",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "progress": 45,
  "message": "Translating chapter 3..."
}
```

## Background Processing

The API uses Celery for background job processing:

### Celery Configuration

```python
CELERY_CONFIG = {
    'broker_url': os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    'result_backend': os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    'task_serializer': 'json',
    'accept_content': ['json'],
    'result_serializer': 'json',
    'timezone': 'UTC',
    'enable_utc': True,
}
```

### Job States

- `PENDING`: Job queued, waiting to start
- `STARTED`: Job is running
- `SUCCESS`: Job completed successfully
- `FAILURE`: Job failed with error
- `RETRY`: Job failed, will retry

## Security

### API Key Management

- API keys are stored securely
- Keys are rotated automatically
- Failed authentication attempts are logged

### Input Validation

- File path validation
- Model name validation
- Language code validation
- File size limits

### Output Sanitization

- HTML content sanitization
- Path traversal prevention
- XSS protection

## Monitoring and Logging

### Health Checks

```bash
# Service health
curl http://localhost:8000/health

# Detailed health check
curl http://localhost:8000/health/detailed
```

### Metrics

The API exposes Prometheus metrics:

```bash
curl http://localhost:8000/metrics
```

### Logging

Logs are written to:
- Console output
- `translation_debug.log`
- Structured JSON logs

## Deployment

### Docker Deployment

```bash
# Build image
docker build -t bilingual-book-maker-api .

# Run container
docker run -p 8000:8000 \
  -e BBM_OPENAI_API_KEY=your-key \
  bilingual-book-maker-api
```

### Production Deployment

```bash
# Start with multiple workers
uvicorn my_app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --proxy-headers \
  --forwarded-allow-ips="*"
```

### Environment Variables

```bash
# Required
BBM_OPENAI_API_KEY=sk-your-key

# Optional
BBM_GOOGLE_GEMINI_KEY=your-gemini-key
REDIS_URL=redis://localhost:6379/0
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-supabase-key
```

## SDK Examples

### Python SDK

```python
import requests

class BilingualBookMakerAPI:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def start_translation(self, book_path, model, language, **kwargs):
        response = requests.post(
            f"{self.base_url}/translate/start",
            json={
                "book_path": book_path,
                "model": model,
                "language": language,
                **kwargs
            }
        )
        return response.json()
    
    def get_job_status(self, job_id):
        response = requests.get(
            f"{self.base_url}/translate/jobs/{job_id}"
        )
        return response.json()

# Usage
api = BilingualBookMakerAPI()
job = api.start_translation(
    "test_books/animal_farm.epub",
    "gpt-3.5-turbo",
    "zh-hans",
    test_mode=True
)
```

### JavaScript SDK

```javascript
class BilingualBookMakerAPI {
    constructor(baseUrl = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
    }
    
    async startTranslation(bookPath, model, language, options = {}) {
        const response = await fetch(`${this.baseUrl}/translate/start`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                book_path: bookPath,
                model: model,
                language: language,
                ...options
            })
        });
        return response.json();
    }
    
    async getJobStatus(jobId) {
        const response = await fetch(`${this.baseUrl}/translate/jobs/${jobId}`);
        return response.json();
    }
}

// Usage
const api = new BilingualBookMakerAPI();
const job = await api.startTranslation(
    'test_books/animal_farm.epub',
    'gpt-3.5-turbo',
    'zh-hans',
    { test_mode: true }
);
```

## Next Steps

- **[Implementation Details](./implementation.md)** - Technical architecture
- **[Troubleshooting](./troubleshooting.md)** - Common issues and solutions
- **[Examples](./commands_examples.md)** - Real-world usage scenarios 