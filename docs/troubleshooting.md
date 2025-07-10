# Troubleshooting Guide

This guide helps you resolve common issues when using the Bilingual Book Maker.

## Common Issues

### 1. API Key Problems

#### Issue: "API key not provided"
**Symptoms:**
```
Exception: OpenAI API key not provided, please google how to obtain it
```

**Solutions:**
```bash
# Option 1: Set environment variable
export BBM_OPENAI_API_KEY="sk-your-api-key-here"

# Option 2: Use command line argument
--openai_key "sk-your-api-key-here"

# Option 3: Create .env file
echo "BBM_OPENAI_API_KEY=sk-your-api-key-here" > .env
```

#### Issue: "Invalid API key"
**Symptoms:**
```
openai.AuthenticationError: Invalid API key
```

**Solutions:**
1. Check your API key format (should start with `sk-`)
2. Verify the key is active in your OpenAI account
3. Check your billing status
4. Ensure you have sufficient credits

#### Issue: "Rate limit exceeded"
**Symptoms:**
```
openai.RateLimitError: Rate limit exceeded
```

**Solutions:**
```bash
# Use multiple API keys
--openai_key "sk-key1,sk-key2,sk-key3"

# Or set multiple environment variables
export BBM_OPENAI_API_KEY="sk-key1,sk-key2,sk-key3"
```

### 2. File Path Issues

#### Issue: "Book file not found"
**Symptoms:**
```
Error: the book your_book.epub does not exist.
```

**Solutions:**
```bash
# Check file exists
ls -la your_book.epub

# Use absolute path
--book_name /full/path/to/your_book.epub

# Check file permissions
chmod 644 your_book.epub
```

#### Issue: "Unsupported file format"
**Symptoms:**
```
Exception: now only support files of these formats: epub,txt,srt,md,qmd
```

**Solutions:**
1. Convert your file to a supported format
2. Check file extension is correct
3. For directories, ensure they contain markdown files

### 3. Model Selection Issues

#### Issue: "Unsupported model"
**Symptoms:**
```
Exception: Unsupported model: 'invalid-model'
```

**Solutions:**
```bash
# Use simple model selection
--model openai    # Uses gpt-3.5-turbo
--model gemini    # Uses gemini-1.5-flash

# Or use specific supported models
--model_list gpt-4
--model_list gpt-3.5-turbo
--model_list gemini-1.5-pro
```

#### Issue: "Cannot use both --model and --model_list"
**Symptoms:**
```
Exception: Cannot use both --model and --model_list. Choose one.
```

**Solutions:**
```bash
# Choose one approach:
--model openai
# OR
--model_list gpt-4
```

### 4. Translation Quality Issues

#### Issue: Poor translation quality
**Symptoms:**
- Inaccurate translations
- Missing context
- Inconsistent terminology

**Solutions:**
```bash
# Use better model
--model_list gpt-4

# Enable context
--use_context

# Lower temperature for consistency
--temperature 0.3

# Use custom prompt
--prompt "Translate to {language} with high accuracy and consistency: {text}"
```

#### Issue: Inconsistent translations
**Symptoms:**
- Same terms translated differently
- Inconsistent tone

**Solutions:**
```bash
# Enable context awareness
--use_context

# Use reasoning models
--model_list o1-mini --reasoning_effort high

# Increase accumulated tokens
--accumulated_num 2000
```

### 5. Performance Issues

#### Issue: Slow translation
**Symptoms:**
- Translation takes too long
- API rate limits

**Solutions:**
```bash
# Use faster model
--model_list gpt-3.5-turbo

# Increase batch size
--batch_size 50

# Use multiple models
--model_list "gpt-4,gpt-3.5-turbo,gpt-4o"

# Disable context for speed
# (remove --use_context)
```

#### Issue: Memory issues
**Symptoms:**
- Out of memory errors
- Process crashes

**Solutions:**
```bash
# Reduce batch size
--batch_size 5

# Use smaller accumulated tokens
--accumulated_num 800

# Process smaller files first
--test --test_num 3
```

### 6. Network Issues

#### Issue: Connection timeouts
**Symptoms:**
```
requests.exceptions.ConnectTimeout
```

**Solutions:**
```bash
# Set proxy
--proxy "http://127.0.0.1:7890"

# Or use environment variables
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890

# Increase timeout
# (modify in code if needed)
```

#### Issue: SSL certificate errors
**Symptoms:**
```
ssl.SSLCertVerificationError
```

**Solutions:**
```bash
# Update certificates
pip install --upgrade certifi

# Or disable verification (not recommended)
# export PYTHONHTTPSVERIFY=0
```

### 7. EPUB-Specific Issues

#### Issue: "Cannot parse EPUB"
**Symptoms:**
```
Exception: can not load file
```

**Solutions:**
1. Check EPUB file integrity
2. Try a different EPUB file
3. Re-download the EPUB file
4. Use a different EPUB reader to verify

#### Issue: Missing translations in EPUB
**Symptoms:**
- Some paragraphs not translated
- Inconsistent translation coverage

**Solutions:**
```bash
# Include more tags
--translate-tags "p,h1,h2,h3,blockquote,div"

# Allow navigable strings
--allow_navigable_strings

# Check excluded tags
--exclude_translate-tags "sup,code"
```

### 8. Resume Issues

#### Issue: Resume not working
**Symptoms:**
- Translation starts from beginning
- Progress not saved

**Solutions:**
```bash
# Ensure resume flag is set
--resume

# Check temp files exist
ls -la *_bilingual_temp.epub

# Check progress file
ls -la *_progress.json
```

#### Issue: Corrupted progress file
**Symptoms:**
- Resume fails with error
- Progress file is invalid JSON

**Solutions:**
```bash
# Remove corrupted progress file
rm *_progress.json

# Start fresh without resume
# (remove --resume flag)
```

### 9. Docker Issues

#### Issue: "Permission denied" in Docker
**Symptoms:**
```
docker: Error response from daemon: permission denied
```

**Solutions:**
```bash
# Fix directory permissions
chmod 755 /path/to/your/books

# Use correct user
docker run --user $(id -u):$(id -g) ...

# Or run as root (not recommended)
docker run --user root ...
```

#### Issue: "File not found" in Docker
**Symptoms:**
```
Error: the book /app/test_books/book.epub does not exist
```

**Solutions:**
```bash
# Check volume mounting
docker run --mount type=bind,source=/host/path,target=/app/test_books ...

# Verify file exists in host
ls -la /host/path/book.epub

# Use absolute paths
docker run --mount type=bind,source=$(pwd),target=/app/test_books ...
```

### 10. API Service Issues

#### Issue: "Cannot connect to API"
**Symptoms:**
```
Connection refused
```

**Solutions:**
```bash
# Check if service is running
curl http://localhost:8000/

# Start the service
python run_service.py

# Check logs
tail -f translation_debug.log
```

#### Issue: "Job not found"
**Symptoms:**
```
HTTP 404: Job not found
```

**Solutions:**
1. Check job ID is correct
2. Verify job exists in memory
3. Restart API service if needed
4. Check job status with `GET /translate/jobs`

## Debug Mode

Enable debug logging for detailed troubleshooting:

```bash
python3 make_book.py \
  --book_name your_book.epub \
  --model openai \
  --openai_key YOUR_KEY \
  --language zh-hans \
  --debug
```

Debug output includes:
- API request/response details
- Token usage information
- File processing steps
- Error stack traces

## Testing Your Setup

### 1. Basic Test
```bash
python3 make_book.py \
  --book_name test_books/animal_farm.epub \
  --model openai \
  --openai_key YOUR_KEY \
  --test \
  --test_num 3 \
  --language zh-hans
```

### 2. API Test
```bash
# Test API health
curl http://localhost:8000/

# Test models endpoint
curl http://localhost:8000/translate/models

# Test translation start
curl -X POST "http://localhost:8000/translate/start" \
  -H "Content-Type: application/json" \
  -d '{
    "book_path": "test_books/animal_farm.epub",
    "model": "gpt-3.5-turbo",
    "language": "zh-hans",
    "test_mode": true
  }'
```

### 3. Environment Test
```bash
# Check Python version
python3 --version

# Check dependencies
pip list | grep -E "(openai|google-generativeai|ebooklib)"

# Check environment variables
echo $BBM_OPENAI_API_KEY
```

## Performance Optimization

### For Large Books
```bash
# Use faster model
--model_list gpt-3.5-turbo

# Increase batch size
--batch_size 50

# Use multiple models
--model_list "gpt-4,gpt-3.5-turbo,gpt-4o"

# Disable context for speed
# (remove --use_context)
```

### For Quality Translation
```bash
# Use advanced model
--model_list gpt-4

# Enable context
--use_context

# Lower temperature
--temperature 0.3

# Increase accumulated tokens
--accumulated_num 2000
```

## Getting Help

### 1. Check Logs
```bash
# Application logs
tail -f translation_debug.log

# API logs
tail -f api_debug.log

# System logs
journalctl -u bilingual-book-maker
```

### 2. Enable Verbose Output
```bash
# CLI verbose mode
--debug

# API verbose mode
uvicorn my_app.main:app --log-level debug
```

### 3. Community Support
- **GitHub Issues**: Report bugs and feature requests
- **Discussions**: Ask questions and share solutions
- **Documentation**: Check the full documentation

### 4. Common Commands for Debugging

```bash
# Check file integrity
file your_book.epub

# Check file size
ls -lh your_book.epub

# Check API key format
echo $BBM_OPENAI_API_KEY | head -c 10

# Test API connectivity
curl -H "Authorization: Bearer $BBM_OPENAI_API_KEY" \
  https://api.openai.com/v1/models

# Check Python environment
python3 -c "import openai; print(openai.__version__)"
```

## Prevention Tips

1. **Always test first** with `--test` and small `--test_num`
2. **Use environment variables** for API keys
3. **Check file formats** before processing
4. **Monitor API usage** and costs
5. **Backup original files** before translation
6. **Use resume capability** for large books
7. **Enable debug mode** when troubleshooting
8. **Keep dependencies updated**

## Next Steps

- **[Installation Guide](./installation.md)** - Setup instructions
- **[Quick Start](./quickstart.md)** - Basic usage examples
- **[Command Reference](./cmd.md)** - Complete CLI documentation
- **[Examples](./commands_examples.md)** - Real-world usage scenarios 