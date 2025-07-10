# Examples and Use Cases

This page provides comprehensive examples of how to use the Bilingual Book Maker for various real-world scenarios.

## Basic Examples

### 1. Simple EPUB Translation

Translate an EPUB book to Chinese:

```bash
python3 make_book.py \
  --book_name "books/1984.epub" \
  --model openai \
  --openai_key "sk-your-api-key" \
  --language zh-hans
```

**Output:** `books/1984_bilingual.epub`

### 2. Test Translation First

Always test with a small sample:

```bash
python3 make_book.py \
  --book_name "books/1984.epub" \
  --model openai \
  --openai_key "sk-your-api-key" \
  --test \
  --test_num 5 \
  --language zh-hans
```

### 3. High-Quality Translation

Use GPT-4 for better quality:

```bash
python3 make_book.py \
  --book_name "books/1984.epub" \
  --model_list gpt-4 \
  --openai_key "sk-your-api-key" \
  --language fr \
  --use_context \
  --temperature 0.3
```

## Advanced Examples

### 4. Batch Processing Markdown Files

Process an entire directory of markdown files:

```bash
python3 make_book.py \
  --book_name "manuscript/chapters/" \
  --model openai \
  --openai_key "sk-your-api-key" \
  --language es \
  --batch_size 15
```

### 5. Subtitle Translation

Translate movie subtitles:

```bash
python3 make_book.py \
  --book_name "movies/movie_eng.srt" \
  --model openai \
  --openai_key "sk-your-api-key" \
  --language ja
```

### 6. Single Translation Mode

Generate only the translated version:

```bash
python3 make_book.py \
  --book_name "books/1984.epub" \
  --model openai \
  --openai_key "sk-your-api-key" \
  --language de \
  --single_translate
```

### 7. Custom Translation Style

Apply custom styling to translations:

```bash
python3 make_book.py \
  --book_name "books/1984.epub" \
  --model openai \
  --openai_key "sk-your-api-key" \
  --language it \
  --translation_style "color: #666666; font-style: italic; font-size: 0.9em;"
```

## Model-Specific Examples

### 8. Using Gemini Models

```bash
python3 make_book.py \
  --book_name "books/1984.epub" \
  --model_list gemini-1.5-pro \
  --gemini_key "your-gemini-key" \
  --language ko \
  --interval 0.1
```

### 9. Multiple Models for Load Balancing

```bash
python3 make_book.py \
  --book_name "books/1984.epub" \
  --model_list "gpt-4,gpt-3.5-turbo,gpt-4o" \
  --openai_key "sk-your-api-key" \
  --language pt
```

### 10. O1/O3 Models for Complex Content

```bash
python3 make_book.py \
  --book_name "books/technical_manual.epub" \
  --model_list o1-mini \
  --openai_key "sk-your-api-key" \
  --language zh-hans \
  --reasoning_effort high
```

## Custom Prompts Examples

### 11. Academic Translation

```bash
python3 make_book.py \
  --book_name "papers/research_paper.md" \
  --model openai \
  --openai_key "sk-your-api-key" \
  --language fr \
  --prompt "Translate this academic text to French, maintaining formal academic style and preserving all technical terminology: {text}"
```

### 12. Creative Writing Translation

```bash
python3 make_book.py \
  --book_name "stories/creative_story.md" \
  --model openai \
  --openai_key "sk-your-api-key" \
  --language ja \
  --prompt "Translate this creative story to Japanese, preserving the poetic and emotional tone while adapting cultural references appropriately: {text}"
```

### 13. Technical Documentation

```bash
python3 make_book.py \
  --book_name "docs/technical_guide.md" \
  --model openai \
  --openai_key "sk-your-api-key" \
  --language de \
  --prompt "Translate this technical documentation to German, maintaining precise technical terminology and clear instructional style: {text}"
```

## EPUB-Specific Examples

### 14. Selective Tag Translation

```bash
python3 make_book.py \
  --book_name "books/1984.epub" \
  --model openai \
  --openai_key "sk-your-api-key" \
  --language es \
  --translate-tags "p,h1,h2,h3,blockquote" \
  --exclude_translate-tags "code,pre,table"
```

### 15. Navigable Strings Translation

```bash
python3 make_book.py \
  --book_name "books/1984.epub" \
  --model openai \
  --openai_key "sk-your-api-key" \
  --language it \
  --allow_navigable_strings
```

### 16. File-Specific Translation

```bash
python3 make_book.py \
  --book_name "books/1984.epub" \
  --model openai \
  --openai_key "sk-your-api-key" \
  --language ru \
  --only_filelist "chapter1.xhtml,chapter2.xhtml,chapter3.xhtml"
```

## Performance Optimization Examples

### 17. Fast Translation (Speed over Quality)

```bash
python3 make_book.py \
  --book_name "books/1984.epub" \
  --model_list gpt-3.5-turbo \
  --openai_key "sk-your-api-key" \
  --language zh-hans \
  --batch_size 50 \
  --temperature 1.0
```

### 18. High-Quality Translation (Quality over Speed)

```bash
python3 make_book.py \
  --book_name "books/1984.epub" \
  --model_list gpt-4 \
  --openai_key "sk-your-api-key" \
  --language fr \
  --use_context \
  --temperature 0.3 \
  --accumulated_num 2000
```

### 19. Balanced Approach

```bash
python3 make_book.py \
  --book_name "books/1984.epub" \
  --model_list "gpt-4,gpt-3.5-turbo" \
  --openai_key "sk-your-api-key" \
  --language de \
  --use_context \
  --temperature 0.7
```

## Resume and Recovery Examples

### 20. Resume Interrupted Translation

```bash
python3 make_book.py \
  --book_name "books/1984.epub" \
  --model openai \
  --openai_key "sk-your-api-key" \
  --language ja \
  --resume
```

### 21. Retranslate Specific Section

```bash
python3 make_book.py \
  --book_name "books/1984.epub" \
  --retranslate "books/1984_bilingual.epub" \
  "chapter3.xhtml" \
  "It was a bright cold day in April" \
  "The clocks were striking thirteen"
```

## API and Cloud Examples

### 22. Azure OpenAI

```bash
python3 make_book.py \
  --book_name "books/1984.epub" \
  --model_list gpt-4 \
  --openai_key "your-azure-key" \
  --api_base "https://your-resource.openai.azure.com/" \
  --deployment_id "gpt-4-deployment" \
  --language es
```

### 23. Ollama Local Models

```bash
python3 make_book.py \
  --book_name "books/1984.epub" \
  --model_list gpt-3.5-turbo \
  --ollama_model "llama2" \
  --api_base "http://localhost:11434/v1" \
  --language fr
```

### 24. Custom API Endpoint

```bash
python3 make_book.py \
  --book_name "books/1984.epub" \
  --model_list gpt-4 \
  --openai_key "your-key" \
  --api_base "https://your-custom-endpoint.com/v1" \
  --language de
```

## Language-Specific Examples

### 25. Chinese Translation

```bash
# Simplified Chinese
python3 make_book.py \
  --book_name "books/1984.epub" \
  --model openai \
  --openai_key "sk-your-api-key" \
  --language zh-hans

# Traditional Chinese
python3 make_book.py \
  --book_name "books/1984.epub" \
  --model openai \
  --openai_key "sk-your-api-key" \
  --language zh-hant
```

### 26. Japanese Translation

```bash
python3 make_book.py \
  --book_name "books/1984.epub" \
  --model openai \
  --openai_key "sk-your-api-key" \
  --language ja \
  --use_context
```

### 27. Arabic Translation

```bash
python3 make_book.py \
  --book_name "books/1984.epub" \
  --model openai \
  --openai_key "sk-your-api-key" \
  --language ar \
  --prompt "Translate to Arabic, maintaining right-to-left text formatting: {text}"
```

## Specialized Use Cases

### 28. Academic Paper Translation

```bash
python3 make_book.py \
  --book_name "papers/academic_paper.md" \
  --model_list gpt-4 \
  --openai_key "sk-your-api-key" \
  --language fr \
  --prompt "Translate this academic paper to French, preserving all citations, references, and technical terminology: {text}" \
  --use_context \
  --temperature 0.2
```

### 29. Poetry Translation

```bash
python3 make_book.py \
  --book_name "poetry/poems.md" \
  --model_list gpt-4 \
  --openai_key "sk-your-api-key" \
  --language it \
  --prompt "Translate this poetry to Italian, preserving meter, rhythm, and emotional resonance while adapting cultural references: {text}" \
  --temperature 0.8
```

### 30. Technical Manual Translation

```bash
python3 make_book.py \
  --book_name "manuals/technical_manual.md" \
  --model_list o1-mini \
  --openai_key "sk-your-api-key" \
  --language de \
  --prompt "Translate this technical manual to German, maintaining precise technical terminology and clear step-by-step instructions: {text}" \
  --reasoning_effort high
```

## Environment Variable Examples

### 31. Using Environment Variables

```bash
# Set environment variables
export BBM_OPENAI_API_KEY="sk-your-api-key"
export BBM_GOOGLE_GEMINI_KEY="your-gemini-key"

# Run without command-line keys
python3 make_book.py \
  --book_name "books/1984.epub" \
  --model openai \
  --language zh-hans
```

### 32. Project-Specific Configuration

```bash
# Create .env file in project directory
echo "BBM_OPENAI_API_KEY=sk-your-api-key" > .env
echo "BBM_OPENAI_API_BASE=https://your-endpoint.openai.azure.com/" >> .env
echo "BBM_OPENAI_DEPLOYMENT_ID=your-deployment" >> .env

# Run with project configuration
python3 make_book.py \
  --book_name "books/1984.epub" \
  --model_list gpt-4 \
  --language es
```

## Docker Examples

### 33. Basic Docker Usage

```bash
# Build image
docker build --tag bilingual_book_maker .

# Run translation
docker run --rm \
  --mount type=bind,source=/path/to/books,target=/app/test_books \
  bilingual_book_maker \
  --book_name /app/test_books/1984.epub \
  --openai_key "sk-your-api-key" \
  --language fr
```

### 34. Docker with Environment File

```bash
# Create .env file
echo "BBM_OPENAI_API_KEY=sk-your-api-key" > .env

# Run with environment file
docker run --rm \
  --mount type=bind,source=/path/to/books,target=/app/test_books \
  --env-file .env \
  bilingual_book_maker \
  --book_name /app/test_books/1984.epub \
  --language zh-hans
```

## Troubleshooting Examples

### 35. Debug Mode

```bash
python3 make_book.py \
  --book_name "books/1984.epub" \
  --model openai \
  --openai_key "sk-your-api-key" \
  --language zh-hans \
  --debug
```

### 36. Test with Small Sample

```bash
python3 make_book.py \
  --book_name "books/1984.epub" \
  --model openai \
  --openai_key "sk-your-api-key" \
  --test \
  --test_num 3 \
  --language zh-hans \
  --debug
```

## Best Practices

1. **Always test first** with `--test` and small `--test_num`
2. **Use appropriate models** - GPT-4 for quality, GPT-3.5 for speed
3. **Enable context** with `--use_context` for better consistency
4. **Set reasonable temperature** - 0.3 for technical, 0.7 for creative
5. **Use custom prompts** for specialized content
6. **Monitor API usage** and costs
7. **Backup original files** before translation
8. **Use resume capability** for large books

## Next Steps

- **[Command Reference](./cmd.md)** - Complete CLI documentation
- **[Implementation Details](./implementation.md)** - Technical architecture
- **[API Documentation](./api.md)** - REST API usage 