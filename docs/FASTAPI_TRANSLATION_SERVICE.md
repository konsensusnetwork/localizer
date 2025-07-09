# FastAPI + Supabase Translation Service

This is a comprehensive implementation of a translation service built with FastAPI and Supabase, as outlined in the integration guide. The service provides asynchronous translation capabilities with user authentication, file storage, and a modern web dashboard.

## Architecture Overview

The implementation follows the architecture described in the integration guide:

1. **FastAPI Backend** - Async-capable web framework for the API
2. **Supabase Integration** - Authentication, file storage, and database logging
3. **Asynchronous Processing** - Both BackgroundTasks and Celery options
4. **Web Dashboard** - Modern HTML/JavaScript front-end
5. **Translation Engine** - Built on top of the existing book-maker translation system

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

frontend/
└── index.html             # Web dashboard

Config Files:
├── .env.example           # Environment variables template
├── fastapi_requirements.txt # Additional dependencies
└── FASTAPI_TRANSLATION_SERVICE.md # This documentation
```

## Features

### Authentication & Authorization
- ✅ Supabase-based JWT authentication
- ✅ Mock authentication for development
- ✅ User-based job isolation
- ✅ Protected API endpoints

### Translation Processing
- ✅ Asynchronous translation with FastAPI BackgroundTasks
- ✅ Celery integration for robust background processing
- ✅ Support for multiple file formats (EPUB, TXT, SRT, QMD, MD)
- ✅ File upload and processing
- ✅ Model and language validation
- ✅ Custom prompt support
- ✅ Test mode for development

### Job Management
- ✅ Real-time job status tracking
- ✅ Job cancellation
- ✅ Progress monitoring
- ✅ Error handling and reporting
- ✅ Job history

### File Storage & Logging
- ✅ Supabase Storage integration
- ✅ Automatic file upload after translation
- ✅ Structured logging to database
- ✅ Download links for completed translations
- ✅ File cleanup and management

### Web Dashboard
- ✅ Modern, responsive UI
- ✅ Drag-and-drop file upload
- ✅ Real-time job monitoring
- ✅ Translation history
- ✅ Configuration validation
- ✅ Error handling and user feedback

## Installation & Setup

### 1. Install Dependencies

```bash
# Install existing dependencies
pip install -r requirements.txt

# Install additional FastAPI dependencies
pip install -r fastapi_requirements.txt
```

### 2. Environment Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your credentials
nano .env
```

Required environment variables:
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_ANON_KEY`: Supabase anonymous key
- `SUPABASE_SERVICE_KEY`: Supabase service key (for server-side operations)
- `REDIS_URL`: Redis connection URL (for Celery)
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

### 4. Redis Setup (Optional - for Celery)

```bash
# Install Redis
sudo apt-get install redis-server

# Or using Docker
docker run -d -p 6379:6379 redis:alpine
```

## Running the Service

### Development Mode

```bash
# Start the FastAPI server
uvicorn my_app.main:app --reload --host 0.0.0.0 --port 8000

# For Celery (in a separate terminal)
celery -A my_app.workers.tasks worker --loglevel=info
```

### Production Mode

```bash
# Start with multiple workers
uvicorn my_app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Start Celery worker
celery -A my_app.workers.tasks worker --loglevel=info --concurrency=4
```

### Using Docker

```bash
# Build the image
docker build -t translation-service .

# Run with Docker Compose
docker-compose up -d
```

## API Endpoints

### Authentication
- `GET /auth/status` - Check authentication system status
- `GET /auth/user-info` - Get current user information
- `POST /auth/test-auth` - Test authentication

### Translation
- `GET /translate/models` - Get supported models and languages
- `POST /translate/start` - Start translation with file path
- `POST /translate/upload-and-translate` - Upload file and start translation
- `GET /translate/status/{job_id}` - Get job status
- `GET /translate/jobs` - Get user's active jobs
- `DELETE /translate/jobs/{job_id}` - Cancel a job
- `GET /translate/download/{job_id}` - Get download link
- `POST /translate/validate` - Validate translation configuration

### Core Endpoints
- `GET /` - API information
- `GET /health` - Health check

## Usage Examples

### Starting a Translation (File Upload)

```bash
curl -X POST "http://localhost:8000/translate/upload-and-translate" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/book.epub" \
  -F "model=openai" \
  -F "language=zh-hans" \
  -F "single_translate=true"
```

### Checking Job Status

```bash
curl -X GET "http://localhost:8000/translate/status/job-id" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Getting User Jobs

```bash
curl -X GET "http://localhost:8000/translate/jobs" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Web Dashboard

The web dashboard provides a complete user interface for:

1. **Authentication** - Automatic handling of Supabase authentication
2. **File Upload** - Drag-and-drop or file picker
3. **Translation Configuration** - Model selection, language, prompts
4. **Job Monitoring** - Real-time status updates
5. **Download Management** - Easy access to completed translations
6. **History** - View past translations

To access the dashboard:
1. Open `frontend/index.html` in a web browser
2. Configure the API_BASE_URL in the JavaScript
3. Set up Supabase credentials if using real authentication

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

## Background Processing Options

### FastAPI BackgroundTasks
- **Pros**: Simple, built-in, no external dependencies
- **Cons**: Limited scalability, tasks lost on restart
- **Use Case**: Development, small-scale usage

### Celery with Redis
- **Pros**: Robust, scalable, persistent, retry logic
- **Cons**: Requires Redis, more complex setup
- **Use Case**: Production, high-volume processing

## Monitoring & Logging

### Database Logging
All translation runs are logged to the Supabase database with:
- Job configuration
- Status tracking
- Error information
- Performance metrics
- Token usage

### File Logging
Detailed logs are stored in Supabase Storage:
- Translation progress
- API responses
- Error details
- Processing times

### Job Status Tracking
Real-time status updates:
- `pending` - Job created, waiting to start
- `started` - Translation in progress
- `completed` - Successfully finished
- `failed` - Error occurred
- `cancelled` - User cancelled

## Security Considerations

1. **Authentication**: All endpoints require valid JWT tokens
2. **Authorization**: Users can only access their own jobs
3. **File Upload**: Validation of file types and sizes
4. **API Keys**: Secure storage in environment variables
5. **CORS**: Configurable for production deployment

## Error Handling

The service implements comprehensive error handling:
- Configuration validation
- API key validation
- File format validation
- Network error handling
- Database error handling
- Storage error handling

## Performance Considerations

1. **Async Processing**: Non-blocking translation execution
2. **Database Indexing**: Optimized queries for job lookup
3. **File Management**: Automatic cleanup of temporary files
4. **Connection Pooling**: Efficient database connections
5. **Caching**: Job status caching for performance

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
COPY requirements.txt fastapi_requirements.txt ./
RUN pip install -r requirements.txt -r fastapi_requirements.txt

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

# Rate limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600
```

## Testing

### Unit Tests
```bash
# Run translation tests
python -m pytest tests/test_translation.py

# Run API tests
python -m pytest tests/test_api.py

# Run integration tests
python -m pytest tests/test_integration.py
```

### Manual Testing
1. Test authentication flow
2. Test file upload and processing
3. Test job management
4. Test error scenarios
5. Test dashboard functionality

## Contributing

1. Follow the existing code structure
2. Add comprehensive error handling
3. Include type hints
4. Write tests for new features
5. Update documentation

## Future Enhancements

- [ ] Batch translation processing
- [ ] Translation quality metrics
- [ ] User usage analytics
- [ ] Custom model integration
- [ ] Advanced file preprocessing
- [ ] Multi-tenant support
- [ ] API rate limiting
- [ ] WebSocket status updates
- [ ] Mobile app integration
- [ ] Advanced search and filtering

## Troubleshooting

### Common Issues

1. **Authentication fails**: Check Supabase configuration
2. **Translation fails**: Verify API keys and model availability
3. **File upload fails**: Check file size and format
4. **Jobs stuck**: Restart Celery workers
5. **Database errors**: Check Supabase connection

### Debug Mode
```bash
# Enable debug logging
export DEBUG=True

# Check service status
curl http://localhost:8000/health

# Check authentication
curl http://localhost:8000/auth/status
```

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs for error details
3. Verify environment configuration
4. Test with minimal configuration

This implementation provides a complete, production-ready translation service that combines the power of FastAPI's async capabilities with Supabase's authentication and storage features, exactly as outlined in the integration guide.