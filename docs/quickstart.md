# Quick Start Guide

Get up and running with Bilingual Book Maker in minutes. This guide covers the most common use cases and basic commands.

## Prerequisites

Before starting, make sure you have:
- ✅ Python 3.10+ installed
- ✅ API key for your chosen translation service
- ✅ A book file to translate (EPUB, TXT, SRT, or Markdown)

## Basic Translation

### Step 1: Test Your Setup

Start with a simple test using the included sample book:

```bash
# Test with OpenAI (first 10 paragraphs only)
python3 make_book.py \
  --book_name test_books/animal_farm.epub \
  --model openai \
  --openai_key YOUR_API_KEY \
  --test \
  --language zh-hans
```

This will:
- Translate the first 10 paragraphs of Animal Farm
- Create a bilingual version with Chinese translation
- Save the result as `animal_farm_bilingual.epub`

### Step 2: Full Translation

Once the test works, translate the entire book:

```bash
# Full translation with OpenAI
python3 make_book.py \
  --book_name test_books/animal_farm.epub \
  --model openai \
  --openai_key YOUR_API_KEY \
  --language zh-hans
```

## Common Use Cases

### 1. EPUB Translation

```bash
# Basic EPUB translation
python3 make_book.py \
  --book_name your_book.epub \
  --model openai \
  --openai_key YOUR_API_KEY \
  --language fr

# With specific model
python3 make_book.py \
  --book_name your_book.epub \
  --model_list gpt-4 \
  --openai_key YOUR_API_KEY \
  --language es
```

### 2. Text File Translation

```bash
# Plain text translation
python3 make_book.py \
  --book_name your_document.txt \
  --model openai \
  --openai_key YOUR_API_KEY \
  --language ja

# Batch translation (multiple lines at once)
python3 make_book.py \
  --book_name your_document.txt \
  --model openai \
  --openai_key YOUR_API_KEY \
  --language de \
  --batch_size 20
```

### 3. Subtitle Translation

```bash
# SRT subtitle translation
python3 make_book.py \
  --book_name your_subtitles.srt \
  --model openai \
  --openai_key YOUR_API_KEY \
  --language ko
```

### 4. Markdown Translation

```bash
# Single markdown file
python3 make_book.py \
  --book_name your_document.md \
  --model openai \
  --openai_key YOUR_API_KEY \
  --language it

# Directory of markdown files
python3 make_book.py \
  --book_name path/to/markdown/directory \
  --model openai \
  --openai_key YOUR_API_KEY \
  --language pt
```

## Model Selection

### Simple Model Selection

```bash
# Use OpenAI with default model (gpt-3.5-turbo)
--model openai

# Use Gemini with default model (gemini-1.5-flash)
--model gemini
```

### Specific Model Selection

```bash
# Use specific OpenAI models
--model_list gpt-4
--model_list gpt-3.5-turbo
--model_list o1-mini

# Use specific Gemini models
--model_list gemini-1.5-pro
--model_list gemini-1.5-flash-002

# Use multiple models for load balancing
--model_list gpt-4,gpt-3.5-turbo,gpt-4o
```

## Language Options

### Common Languages

```bash
# Chinese (Simplified)
--language zh-hans

# Chinese (Traditional)
--language zh-hant

# Japanese
--language ja

# Korean
--language ko

# French
--language fr

# German
--language de

# Spanish
--language es

# Italian
--language it

# Portuguese
--language pt

# Russian
--language ru

# Arabic
--language ar
```

### Full Language List

The tool supports 100+ languages. Run this to see all options:

```bash
python3 make_book.py --help
```

## Advanced Features

### 1. Context-Aware Translation

Improve translation consistency with context:

```bash
python3 make_book.py \
  --book_name your_book.epub \
  --model openai \
  --openai_key YOUR_API_KEY \
  --language fr \
  --use_context
```

### 2. Single Translation Mode

Generate only the translated version (no bilingual):

```bash
python3 make_book.py \
  --book_name your_book.epub \
  --model openai \
  --openai_key YOUR_API_KEY \
  --language es \
  --single_translate
```

### 3. Custom Prompts

Use your own translation instructions:

```bash
python3 make_book.py \
  --book_name your_book.epub \
  --model openai \
  --openai_key YOUR_API_KEY \
  --language de \
  --prompt "Translate this text to German in a formal academic style: {text}"
```

### 4. Resume Interrupted Translation

Continue where you left off:

```bash
python3 make_book.py \
  --book_name your_book.epub \
  --model openai \
  --openai_key YOUR_API_KEY \
  --language it \
  --resume
```

## Output Files

### Bilingual Output (Default)

The tool creates bilingual files with both original and translated text:

- `your_book_bilingual.epub` - Original + translation
- `your_book_bilingual.txt` - Original + translation
- `your_book_bilingual.srt` - Original + translation

### Single Translation Output

With `--single_translate`, you get only the translated version:

- `your_book_translated.epub` - Translation only
- `your_book_translated.txt` - Translation only

### Temporary Files

During translation, temporary files are created:

- `your_book_bilingual_temp.epub` - Incomplete translation
- `your_book_progress.json` - Translation progress

## Using the API Service

### Start the API

```bash
# Start the FastAPI service
python run_service.py

# Or with PDM
pdm run start-service
```

### API Usage

```bash
# Start a translation job
curl -X POST "http://localhost:8000/translate/start" \
  -H "Content-Type: application/json" \
  -d '{
    "book_path": "test_books/animal_farm.epub",
    "model": "gpt-3.5-turbo",
    "language": "zh-hans",
    "test_mode": true
  }'

# Check job status
curl "http://localhost:8000/translate/jobs/JOB_ID"

# Get supported models
curl "http://localhost:8000/translate/models"
```

## Troubleshooting

### Common Issues

1. **"API key not provided"**
   ```bash
   # Set environment variable
   export BBM_OPENAI_API_KEY="sk-your-key"
   
   # Or use command line
   --openai_key "sk-your-key"
   ```

2. **"Book file not found"**
   ```bash
   # Check file path
   ls -la your_book.epub
   
   # Use absolute path if needed
   --book_name /full/path/to/your_book.epub
   ```

3. **Translation stops unexpectedly**
   ```bash
   # Resume the translation
   --resume
   ```

4. **Poor translation quality**
   ```bash
   # Try a better model
   --model_list gpt-4
   
   # Use context
   --use_context
   
   # Adjust temperature
   --temperature 0.7
   ```

## Next Steps

Now that you've mastered the basics:

- **[Command Reference](./cmd.md)** - Complete CLI documentation
- **[Examples](./commands_examples.md)** - Advanced usage scenarios
- **[API Documentation](./api.md)** - REST API details
- **[Implementation Details](./implementation.md)** - Technical architecture

## Tips for Best Results

1. **Choose the right model**: GPT-4 for quality, GPT-3.5 for speed
2. **Use context**: Enable `--use_context` for better consistency
3. **Test first**: Always use `--test` to verify settings
4. **Check output**: Review the first few paragraphs before full translation
5. **Resume capability**: Use `--resume` if translation is interrupted 