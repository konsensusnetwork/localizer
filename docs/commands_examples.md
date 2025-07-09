# Command Examples

This document provides real-world examples of how to use the Bilingual Book Maker tool for various translation scenarios.

## Basic Translation Examples

### Formatting Texts to Quarto

```bash
pdm run bbook_maker \
  --book_name books/formatter/21F2_EN_test.md \
  --model openai \
  --model_list o3-mini \
  --reasoning_effort=high \
  --prompt prompts/formatter.prompt.md \
  --batch_size=12 \
  --single_translate \
  --language en
```

### Italian Translation (BM_IT)

```bash
pdm run bbook_maker \
  --book_name books/bm-it/ch01.qmd \
  --model openai \
  --model_list o3-mini \
  --prompt prompts/it-translation.prompt.md \
  --batch_size=5 \
  --single_translate \
  --language it
```

### Dutch Translation (BM_NL)

```bash
pdm run bbook_maker \
  --book_name books/bm-nl/ch09.qmd \
  --model openai \
  --model_list o3-mini \
  --prompt prompts/nl/nl-edit-o3.prompt.md \
  --batch_size=5 \
  --single_translate \
  --language nl \
  --use_context \
  --reasoning_effort=high
```

### TSI Dutch Translation

```bash
pdm run bbook_maker \
  --book_name books/tsi-nl/ch01.qmd \
  --model openai \
  --model_list o3-mini \
  --prompt prompts/nl/nl-edit-o3.prompt.md \
  --batch_size=5 \
  --single_translate \
  --language nl \
  --use_context \
  --reasoning_effort=high
```

## Directory Processing Examples

### French Translation (21FFF_FR) - Run 1

```bash
pdm run dir_process \
  books/21fff/fr \
  --model openai \
  --model_list o3-mini \
  --reasoning_effort=high \
  --prompt prompts/fr-translation-2.prompt.md \
  --batch_size=5 \
  --single_translate \
  --language fr
```

### French Translation (21FFF_FR) - Run 2 (Editing)

```bash
pdm run dir_process \
  books/21fff/fr/to-edit \
  --model openai \
  --model_list o3-mini \
  --reasoning_effort=high \
  --prompt prompts/fr-edit-2.prompt.md \
  --batch_size=5 \
  --single_translate \
  --language fr
```

### Spanish Translation (21FFF_ES)

```bash
pdm run dir_process \
  books/21fff/es \
  --model openai \
  --model_list o3-mini \
  --reasoning_effort=high \
  --prompt prompts/es-translation-prompt.md \
  --batch_size=5 \
  --single_translate \
  --language es
```

### Spanish Translation (21FFF_ES) - Editing

```bash
pdm run dir_process \
  books/21fff/es/to-edit \
  --model openai \
  --model_list o3-mini \
  --reasoning_effort=high \
  --prompt prompts/es/es-edit.prompt.md \
  --batch_size=5 \
  --single_translate \
  --language es
```

## Gemini Model Examples

### Basic Gemini Translation

```bash
python3 make_book.py \
  --book_name test_books/animal_farm.epub \
  --model gemini \
  --language nl
```

### Dutch Translation with Gemini

```bash
pdm run bbook_maker \
  --book_name books/tsi-nl/ch02.qmd \
  --model gemini \
  --prompt prompts/nl/nl-translation-tsi.prompt.md \
  --batch_size=5 \
  --single_translate \
  --language nl \
  --gemini_key AIzaSyA1ZHnMzY6F4vn7JA8QJ6UJXwUvMe2pnfU \
  --model_list gemini-2.5-pro-preview-06-05
```

### Albanian Translation with Gemini

```bash
pdm run bbook_maker \
  --book_name books/bm-al/ch00.md \
  --model gemini \
  --prompt prompts/al-translation.prompt.md \
  --batch_size=5 \
  --single_translate \
  --language Albanian \
  --gemini_key AIzaSyA1ZHnMzY6F4vn7JA8QJ6UJXwUvMe2pnfU \
  --model_list gemini-2.5-pro-preview-06-05
```

### Italian Directory Processing with Gemini

```bash
pdm run dir_process \
  books/bm-it/todo \
  --model gemini \
  --prompt prompts/it-translation-2.prompt.md \
  --batch_size=5 \
  --single_translate \
  --language it \
  --gemini_key AIzaSyA1ZHnMzY6F4vn7JA8QJ6UJXwUvMe2pnfU \
  --model_list gemini-2.5-pro-preview-06-05
```

## Parameter Explanations

### Common Parameters

- `--book_name`: Path to the input file or directory
- `--model`: Translation model to use (openai, gemini, google, deepl, etc.)
- `--model_list`: Specific model variants (comma-separated)
- `--language`: Target language for translation
- `--prompt`: Path to custom prompt file
- `--batch_size`: Number of lines to process in each batch
- `--single_translate`: Process one file at a time
- `--reasoning_effort`: Level of reasoning effort (low, medium, high)
- `--use_context`: Enable context-aware translation

### Model-Specific Parameters

- `--openai_key`: OpenAI API key
- `--gemini_key`: Google Gemini API key
- `--deepl_key`: DeepL API key
- `--claude_key`: Anthropic Claude API key

### Advanced Parameters

- `--resume`: Resume interrupted translation
- `--test`: Test mode with limited processing
- `--test_num`: Number of lines to process in test mode
- `--proxy`: Proxy server for internet access
- `--translate-tags`: HTML tags to translate (for EPUB files)
- `--accumulated_num`: Token accumulation limit before translation 