# Supabase Integration for Translation API

This document explains how to set up and use the Supabase integration for storing translation runs and output files.

## Overview

The Supabase integration provides:
- **Database Storage**: Translation job metadata, status, and logs
- **File Storage**: Translated output files and processing logs
- **User-based Access Control**: Each user can only access their own translations
- **Download URLs**: Secure signed URLs for downloading translation results

## Setup

### 1. Environment Variables

Add the following environment variables to your `.env` file:

```bash
# Supabase Configuration
SUPABASE_URL=your-supabase-project-url
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_KEY=your-supabase-service-role-key
```

### 2. Database Schema

Run the SQL commands in `supabase_schema.sql` in your Supabase dashboard to create:
- `translation_runs` table with proper indexes
- Storage buckets for files and logs
- Row Level Security (RLS) policies
- Automatic timestamp triggers

### 3. Install Dependencies

The Supabase client is already included in the project dependencies:

```bash
pip install supabase
```

### 4. Initialize Buckets

Call the setup endpoint to ensure storage buckets are created:

```bash
POST /translate/setup/supabase
```

## API Endpoints

### Translation Management

#### Start Translation Job
```bash
POST /translate/start
```
- Creates translation job with Supabase logging
- Returns job ID and Supabase status
- Automatically stores job metadata in database

#### Get Job Status
```bash
GET /translate/jobs/{job_id}?user_id={user_id}
```
- Retrieves job status from Supabase database
- Includes download URL if translation is completed
- User authorization required

#### Get User Translation History
```bash
GET /translate/user/{user_id}/translations?limit=50
```
- Fetches user's translation history from database
- Supports pagination with limit parameter
- Returns detailed job information

#### Download Translation Output
```bash
GET /translate/download/{job_id}?user_id={user_id}
```
- Creates secure signed URL for file download
- URL expires in 1 hour
- User authorization required

#### Delete Translation Job
```bash
DELETE /translate/jobs/{job_id}?user_id={user_id}
```
- Removes job from database
- Deletes associated files from storage
- User authorization required

### System Management

#### Check Supabase Health
```bash
GET /translate/health/supabase
```
- Verifies Supabase connection and configuration
- Returns status of environment variables
- Shows bucket names

#### Setup Supabase
```bash
POST /translate/setup/supabase
```
- Creates required storage buckets
- Verifies connection
- Returns setup status

## Data Flow

### Translation Process

1. **Job Creation**: POST to `/translate/start`
   - Creates `TranslationJob` object
   - Logs initial job to Supabase database
   - Starts background translation task

2. **Translation Execution**: Background process
   - Updates job status to "running"
   - Performs translation using book_maker
   - Tracks progress and errors

3. **Completion Processing**: `process_translation_completion()`
   - Uploads output file to Supabase Storage
   - Creates processing log and uploads to Storage
   - Updates final job status in database

4. **File Access**: Client requests
   - Creates signed URLs for secure downloads
   - Enforces user authorization
   - Provides temporary access (1 hour)

### Storage Structure

```
Supabase Storage:
├── translation-files/
│   └── {user_id}/
│       └── {job_id}/
│           └── {output_filename}
└── translation-logs/
    └── {user_id}/
        └── {job_id}/
            └── translation_log_{job_id}.json
```

### Database Schema

```sql
translation_runs:
├── id (BIGSERIAL)
├── user_id (VARCHAR)
├── job_id (VARCHAR, UNIQUE)
├── book_path (TEXT)
├── model (VARCHAR)
├── language (VARCHAR)
├── status (VARCHAR)
├── output_file (TEXT)
├── error (TEXT)
├── token_usage (JSONB)
├── config (JSONB)
├── created_at (TIMESTAMP)
├── started_at (TIMESTAMP)
├── completed_at (TIMESTAMP)
└── updated_at (TIMESTAMP)
```

## Security

### Row Level Security (RLS)
- Users can only access their own translation records
- Storage files are organized by user ID
- All operations require user authentication

### File Access
- Files are stored in private buckets
- Access via signed URLs with expiration
- User authorization checked before URL generation

### API Authorization
- All endpoints require `user_id` parameter
- Jobs are filtered by user ownership
- Cross-user access is prevented

## Error Handling

### Supabase Unavailable
- API gracefully degrades when Supabase is unavailable
- Translation jobs still run but without persistence
- Status endpoints return 503 Service Unavailable

### File Upload Failures
- Translation continues even if file upload fails
- Errors are logged and returned in API responses
- Database logging continues independently

### Configuration Issues
- Health endpoint reports missing environment variables
- Setup endpoint validates configuration
- Clear error messages for troubleshooting

## Usage Examples

### Python Client Example

```python
import requests

# Start translation
response = requests.post('http://localhost:8000/translate/start', json={
    'book_path': '/path/to/book.txt',
    'model': 'gpt-4',
    'language': 'Chinese',
    'user_id': 'user123'
})
job_id = response.json()['job_id']

# Check status
status = requests.get(f'http://localhost:8000/translate/jobs/{job_id}?user_id=user123')
print(status.json())

# Download result when completed
if status.json()['status'] == 'completed':
    download = requests.get(f'http://localhost:8000/translate/download/{job_id}?user_id=user123')
    download_url = download.json()['download_url']
    
    # Download the file
    file_response = requests.get(download_url)
    with open('translated_book.txt', 'wb') as f:
        f.write(file_response.content)
```

### JavaScript/Fetch Example

```javascript
// Start translation
const response = await fetch('/translate/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        book_path: '/path/to/book.txt',
        model: 'gpt-4',
        language: 'Chinese',
        user_id: 'user123'
    })
});
const { job_id } = await response.json();

// Poll for completion
const checkStatus = async () => {
    const status = await fetch(`/translate/jobs/${job_id}?user_id=user123`);
    const data = await status.json();
    
    if (data.status === 'completed') {
        // Download file
        const download = await fetch(`/translate/download/${job_id}?user_id=user123`);
        const { download_url } = await download.json();
        window.open(download_url);
    } else if (data.status === 'running') {
        setTimeout(checkStatus, 5000); // Check again in 5 seconds
    }
};
checkStatus();
```

## Monitoring and Maintenance

### Health Checks
- Use `/translate/health/supabase` to monitor service health
- Check environment variable configuration
- Verify bucket availability

### File Cleanup
- Implement periodic cleanup of old files
- Use job deletion endpoint for manual cleanup
- Monitor storage usage in Supabase dashboard

### Database Maintenance
- Index performance monitoring
- Query optimization for large datasets
- Archive old translation records

## Troubleshooting

### Common Issues

1. **"Supabase not available"**
   - Check environment variables
   - Verify Supabase project is active
   - Test connection with health endpoint

2. **"Failed to create signed URL"**
   - Verify file exists in storage
   - Check user has access to the job
   - Ensure storage bucket policies are correct

3. **"Job not found"**
   - Verify job_id is correct
   - Check user_id matches job owner
   - Ensure job was created successfully

4. **File upload failures**
   - Check Supabase storage quotas
   - Verify bucket permissions
   - Monitor file size limits

For additional support, check the Supabase documentation and API logs.