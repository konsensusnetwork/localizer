# Book Translation Service API

This is a backend-only translation service built with FastAPI and Supabase. The service provides asynchronous translation capabilities with user authentication and file processing.

## Architecture Overview

The implementation consists of:

1. **FastAPI Backend** - Async-capable web framework for the API
2. **Supabase Integration** - Authentication and database logging
3. **Asynchronous Processing** - BackgroundTasks for translation jobs
4. **Translation Engine** - Built on top of the existing book-maker translation system

## Project Structure

```
my_app/
├── __init__.py
├── main.py                 # FastAPI application entry point
├── core.py                 # Core translation logic and job management
├── supabase_client.py      # Supabase integration for storage and logging
├── routers/
│   ├── __init__.py
│   ├── auth.py            # Authentication endpoints
│   └── translate.py       # Translation endpoints
└── workers/
    ├── __init__.py
    └── tasks.py           # Celery tasks for background processing

Config Files:
├── .env                   # Environment variables
├── requirements.txt       # Dependencies
└── docs/                  # API documentation
```

## Features

### Authentication & Authorization
- ✅ Supabase-based JWT authentication
- ✅ Mock authentication for development
- ✅ User-based job isolation
- ✅ Protected API endpoints

### Translation Processing
- ✅ Asynchronous translation with FastAPI BackgroundTasks
- ✅ Support for multiple file formats (EPUB, TXT, SRT, QMD, MD)
- ✅ File path-based processing
- ✅ Model and language validation
- ✅ Custom prompt support
- ✅ Test mode for development

### Job Management
- ✅ Real-time job status tracking
- ✅ Progress monitoring
- ✅ Error handling and reporting
- ✅ Job history

### File Storage & Logging
- ✅ Supabase Storage integration
- ✅ Structured logging to database
- ✅ File cleanup and management

## Installation & Setup

### 1. Install Dependencies

```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
# Create .env file with your credentials
cp .env.example .env
```

Required environment variables:
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_ANON_KEY`: Supabase anonymous key
- `SUPABASE_SERVICE_KEY`: Supabase service key (for server-side operations)
- API keys for your chosen translation models

### 3. Supabase Setup

1. Create a new Supabase project
2. Create the required storage buckets:
   - `translation-files` (for output files)
   - `translation-logs` (for log files)
3. Create the database table:

```sql
CREATE TABLE translation_runs (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    job_id VARCHAR(255) NOT NULL UNIQUE,
    book_path TEXT NOT NULL,
    model VARCHAR(100) NOT NULL,
    language VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    output_file TEXT,
    error TEXT,
    token_usage JSONB,
    config JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Add indexes for performance
CREATE INDEX idx_translation_runs_user_id ON translation_runs(user_id);
CREATE INDEX idx_translation_runs_job_id ON translation_runs(job_id);
CREATE INDEX idx_translation_runs_status ON translation_runs(status);
```

## Running the Service

### Development Mode

```bash
# Start the FastAPI server
uvicorn my_app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
# Start with multiple workers
uvicorn my_app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Docker

```bash
# Build the image
docker build -t translation-service .

# Run the container
docker run -d -p 8000:8000 translation-service
```

## API Endpoints

### Root Endpoints
- `GET /` - Service information
- `GET /models` - Get supported models and languages
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

### Authentication
- `GET /auth/status` - Check authentication system status
- `GET /auth/user-info` - Get current user information
- `POST /auth/test-auth` - Test authentication

### Translation
- `POST /translate/start` - Start translation with file path
- `GET /translate/jobs` - Get user's active jobs
- `GET /translate/jobs/{job_id}` - Get specific job status
- `GET /translate/validate` - Validate translation configuration

## API Usage Examples

### 1. Get Service Information

```bash
curl -X GET "http://localhost:8000/" \
  -H "Content-Type: application/json"
```

Response:
```json
{
  "service": "Book Translation Service",
  "version": "1.0.0",
  "docs": "/docs",
  "redoc": "/redoc"
}
```

### 2. Get Supported Models

```bash
curl -X GET "http://localhost:8000/models" \
  -H "Content-Type: application/json"
```

### 3. Check Authentication Status

```bash
curl -X GET "http://localhost:8000/auth/status" \
  -H "Content-Type: application/json"
```

### 4. Start Translation Job

```bash
curl -X POST "http://localhost:8000/translate/start" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "book_path": "/path/to/book.epub",
    "model": "openai",
    "language": "zh-hans",
    "single_translate": true,
    "test_mode": true,
    "test_num": 10
  }'
```

Response:
```json
{
  "job_id": "uuid-job-id",
  "status": "started",
  "message": "Translation job started"
}
```

### 5. Check Job Status

```bash
curl -X GET "http://localhost:8000/translate/jobs/uuid-job-id" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Response:
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

### 6. Get All User Jobs

```bash
curl -X GET "http://localhost:8000/translate/jobs" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 7. Validate Translation Parameters

```bash
curl -X GET "http://localhost:8000/translate/validate?model=openai&language=zh-hans" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Request/Response Models

### TranslationRequest
```json
{
  "book_path": "string",
  "model": "string",
  "language": "string",
  "model_list": "string (optional)",
  "batch_size": "integer (optional)",
  "single_translate": "boolean (default: false)",
  "test_mode": "boolean (default: false)",
  "test_num": "integer (default: 10)",
  "use_context": "boolean (default: false)",
  "reasoning_effort": "string (default: 'medium')",
  "temperature": "float (default: 1.0)",
  "accumulated_num": "integer (default: 1)",
  "block_size": "integer (default: -1)",
  "prompt_file": "string (optional)",
  "user_id": "string (default: 'mock_user')"
}
```

### TranslationResponse
```json
{
  "job_id": "string",
  "status": "string",
  "message": "string"
}
```

### Job Status Response
```json
{
  "job_id": "string",
  "status": "string",
  "progress": "integer",
  "message": "string",
  "result": "object (optional)",
  "error": "string (optional)"
}
```

## Configuration Options

### Translation Models
- OpenAI (GPT-3.5, GPT-4)
- Claude (Anthropic)
- Gemini (Google)
- Groq
- xAI
- Caiyun
- DeepL
- Custom API

### Supported Languages
- Chinese (Simplified/Traditional)
- Japanese
- Korean
- French
- Spanish
- German
- Italian
- Portuguese
- Russian
- And many more...

### File Formats
- EPUB (eBooks)
- TXT (Plain text)
- SRT (Subtitles)
- QMD (Quarto Markdown)
- MD (Markdown)

## Authentication

The service supports two authentication modes:

1. **Mock Mode** (Development):
   - No Supabase required
   - Uses mock user credentials
   - Automatically enabled when Supabase is not configured

2. **Supabase Mode** (Production):
   - Requires valid JWT tokens
   - Bearer token in Authorization header
   - User isolation and security

## Error Handling

The API returns standard HTTP status codes:
- `200` - Success
- `400` - Bad Request (validation errors)
- `401` - Unauthorized (authentication required)
- `404` - Not Found (resource not found)
- `500` - Internal Server Error

Error responses include:
```json
{
  "detail": "Error message description"
}
```

## Job Status Values

- `running` - Translation in progress
- `completed` - Successfully finished
- `failed` - Error occurred

## Testing the API

### Interactive Documentation
Visit `http://localhost:8000/docs` for Swagger UI interface where you can:
- Explore all endpoints
- Test API calls directly
- View request/response schemas
- Generate code examples

### Alternative Documentation
Visit `http://localhost:8000/redoc` for ReDoc interface with:
- Clean, readable documentation
- Code examples
- Schema definitions

## Security Considerations

1. **Authentication**: Endpoints require valid JWT tokens (except in mock mode)
2. **Authorization**: Users can only access their own jobs
3. **File Validation**: Path validation for file access
4. **API Keys**: Secure storage in environment variables
5. **CORS**: Configurable for production deployment

## Performance Considerations

1. **Async Processing**: Non-blocking translation execution
2. **Background Tasks**: Efficient job processing
3. **Database Indexing**: Optimized queries for job lookup
4. **Connection Pooling**: Efficient database connections

## Development Tips

1. **Mock Mode**: Service works without Supabase for development
2. **Test Mode**: Translate only first 10 paragraphs for testing
3. **Logging**: Comprehensive logging for debugging
4. **Validation**: Input validation before processing
5. **Error Messages**: Clear, actionable error messages

## Deployment

### Docker Deployment
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "my_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables for Production
```bash
# Production settings
ENVIRONMENT=production
DEBUG=False
API_WORKERS=4

# Database connection pooling
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20
```

## Troubleshooting

### Common Issues

1. **Authentication fails**: Check Supabase configuration
2. **Translation fails**: Verify API keys and model availability
3. **File path errors**: Check file permissions and paths
4. **Database errors**: Check Supabase connection

### Debug Mode
```bash
# Enable debug logging
export DEBUG=True

# Check service status
curl http://localhost:8000/

# Check authentication
curl http://localhost:8000/auth/status
```

## Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review the logs for error details
3. Verify environment configuration
4. Test with minimal configuration

This implementation provides a complete, production-ready translation service API that combines the power of FastAPI's async capabilities with Supabase's authentication features.