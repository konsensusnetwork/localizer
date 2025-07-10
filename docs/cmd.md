# Command Reference

Complete documentation of all command-line options and parameters for the Bilingual Book Maker.

## Basic Command Structure

```bash
python3 make_book.py [OPTIONS] --book_name FILE --model PROVIDER
```

## Required Arguments

### `--book_name` (Required)
Path to the book file to translate.

```bash
--book_name test_books/animal_farm.epub
--book_name /path/to/your/document.txt
--book_name /path/to/markdown/directory
```

**Supported formats:**
- `.epub` - E-book files
- `.txt` - Plain text files
- `.srt` - Subtitle files
- `.md`, `.qmd` - Markdown files
- Directory path - Process all markdown files in directory

## Model Selection

### Simple Model Selection
Choose a provider with default model:

```bash
--model openai      # Uses gpt-3.5-turbo
--model gemini      # Uses gemini-1.5-flash
```

### Specific Model Selection
Choose exact model(s):

```bash
--model_list gpt-4
--model_list gpt-3.5-turbo
--model_list gemini-1.5-pro
--model_list o1-mini,o3-mini  # Multiple models for load balancing
```

## API Keys

### OpenAI API Key
```bash
--openai_key "sk-your-api-key-here"
```

**Environment variable:** `BBM_OPENAI_API_KEY`

### Google Gemini API Key
```bash
--gemini_key "your-gemini-key-here"
```

**Environment variable:** `BBM_GOOGLE_GEMINI_KEY`

## Language Options

### Target Language
```bash
--language "Simplified Chinese"    # Full name
--language zh-hans                 # Language code
--language ja                      # Japanese
--language fr                      # French
```

**Default:** `zh-hans` (Simplified Chinese)

### Supported Languages
The tool supports 100+ languages. Common options:

| Language | Code | Full Name |
|----------|------|-----------|
| Chinese (Simplified) | `zh-hans` | `simplified chinese` |
| Chinese (Traditional) | `zh-hant` | `traditional chinese` |
| Japanese | `ja` | `japanese` |
| Korean | `ko` | `korean` |
| French | `fr` | `français` |
| German | `de` | `german` |
| Spanish | `es` | `spanish` |
| Italian | `it` | `italian` |
| Portuguese | `pt` | `portuguese` |
| Russian | `ru` | `russian` |
| Arabic | `ar` | `arabic` |

## Testing and Debugging

### Test Mode
Translate only the first few paragraphs for testing:

```bash
--test                    # Test first 10 paragraphs
--test --test_num 5      # Test first 5 paragraphs
```

### Debug Mode
Enable detailed logging:

```bash
--debug
```

## Translation Options

### Context-Aware Translation
Improve consistency with story context:

```bash
--use_context
--use_context --context_paragraph_limit 3
```

### Single Translation Mode
Generate only translated version (no bilingual):

```bash
--single_translate
```

### Block Size (for single translation)
Merge multiple paragraphs into one block:

```bash
--block_size 5 --single_translate
```

### Batch Size (for text files)
Number of lines to translate together:

```bash
--batch_size 20
```

### Accumulated Tokens
Wait for token accumulation before translation:

```bash
--accumulated_num 1600
```

### Temperature
Control randomness in translation:

```bash
--temperature 0.7
```

**Range:** 0.0 to 2.0 (default: 1.0)

### Reasoning Effort (O1/O3 models)
Set reasoning effort level:

```bash
--reasoning_effort low
--reasoning_effort medium
--reasoning_effort high
--reasoning_effort auto
```

## EPUB-Specific Options

### Translate Tags
Specify HTML tags to translate:

```bash
--translate-tags p,blockquote,h1,h2
```

**Default:** `p`

### Exclude Tags
Specify HTML tags to skip:

```bash
--exclude_translate-tags table,sup,code
```

**Default:** `sup`

### Allow Navigable Strings
Translate untagged text:

```bash
--allow_navigable_strings
```

### File Filtering
Include/exclude specific files:

```bash
--only_filelist "chapter1.xhtml,chapter2.xhtml"
--exclude_filelist "nav.xhtml,cover.xhtml"
```

## Custom Prompts

### Simple Template
```bash
--prompt "Translate {text} to {language} in a formal style"
```

### JSON Configuration
```bash
--prompt '{"system": "You are a professional translator", "user": "Translate {text} to {language}"}'
```

### File-Based Prompts
```bash
--prompt prompt_template.txt
--prompt prompt_config.json
--prompt custom_prompt.md
```

## Resume and Recovery

### Resume Interrupted Translation
```bash
--resume
```

### Retranslate Specific Sections
```bash
--retranslate "book_bilingual.epub" "chapter.xhtml" "start text" "end text"
```

## API Configuration

### Custom API Base URL
```bash
--api_base "https://your-endpoint.openai.azure.com/"
```

### Azure Deployment ID
```bash
--deployment_id "your-deployment-name"
```

### Ollama Support
```bash
--ollama_model "llama2"
--api_base "http://localhost:11434/v1"
```

## Proxy and Network

### Proxy Configuration
```bash
--proxy "http://127.0.0.1:7890"
```

### Request Interval (Gemini)
```bash
--interval 0.1
```

## E-Reader Support

### Kobo Device
```bash
--book_from kobo --device_path /path/to/kobo/device
```

## Output Styling

### Translation Style
```bash
--translation_style "color: #808080; font-style: italic;"
```

## Complete Examples

### Basic Translation
```bash
python3 make_book.py \
  --book_name test_books/animal_farm.epub \
  --model openai \
  --openai_key YOUR_API_KEY \
  --language zh-hans
```

### Advanced Translation
```bash
python3 make_book.py \
  --book_name your_book.epub \
  --model_list gpt-4 \
  --openai_key YOUR_API_KEY \
  --language fr \
  --use_context \
  --temperature 0.7 \
  --single_translate \
  --translation_style "color: #808080; font-style: italic;"
```

### Test Translation
```bash
python3 make_book.py \
  --book_name test_books/animal_farm.epub \
  --model openai \
  --openai_key YOUR_API_KEY \
  --test \
  --test_num 5 \
  --language ja
```

### Directory Processing
```bash
python3 make_book.py \
  --book_name /path/to/markdown/directory \
  --model openai \
  --openai_key YOUR_API_KEY \
  --language es \
  --batch_size 10
```

### Azure OpenAI
```bash
python3 make_book.py \
  --book_name your_book.epub \
  --model_list gpt-4 \
  --openai_key YOUR_AZURE_KEY \
  --api_base "https://your-endpoint.openai.azure.com/" \
  --deployment_id "your-deployment-name" \
  --language de
```

### Gemini Translation
```bash
python3 make_book.py \
  --book_name your_book.epub \
  --model_list gemini-1.5-pro \
  --gemini_key YOUR_GEMINI_KEY \
  --language it \
  --interval 0.05
```

## Environment Variables

You can set these environment variables instead of command-line arguments:

```bash
export BBM_OPENAI_API_KEY="sk-your-key"
export BBM_GOOGLE_GEMINI_KEY="your-gemini-key"
export BBM_OPENAI_API_BASE="https://your-endpoint.openai.azure.com/"
export BBM_OPENAI_DEPLOYMENT_ID="your-deployment-name"
```

## Help and Information

### Show Help
```bash
python3 make_book.py --help
```

### Show Version
```bash
python3 make_book.py --version
```

## Error Handling

### Common Error Messages

1. **"API key not provided"**
   - Set environment variable or use `--openai_key`/`--gemini_key`

2. **"Book file not found"**
   - Check file path and permissions

3. **"Unsupported model"**
   - Use `--model_list` with supported model names

4. **"Translation failed"**
   - Check API key validity and network connection
   - Try with `--test` first

### Debugging Tips

1. **Use `--debug`** for detailed logging
2. **Start with `--test`** to verify setup
3. **Check API quotas** and billing status
4. **Verify file format** is supported
5. **Use `--resume`** if translation is interrupted

## Performance Optimization

### For Large Books
```bash
# Use faster model
--model_list gpt-3.5-turbo

# Increase batch size
--batch_size 50

# Use multiple models
--model_list gpt-4,gpt-3.5-turbo,gpt-4o
```

### For Quality Translation
```bash
# Use advanced model
--model_list gpt-4

# Enable context
--use_context

# Lower temperature
--temperature 0.3
```

## Next Steps

- **[Examples](./commands_examples.md)** - Real-world usage scenarios
- **[Implementation Details](./implementation.md)** - Technical architecture
- **[Troubleshooting](./troubleshooting.md)** - Common issues and solutions 