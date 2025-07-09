# Bilingual Book Maker Documentation

Welcome to the Bilingual Book Maker documentation. This tool is an AI translation service that uses various language models to create multi-language versions of epub/txt/srt files and books.

## ⚠️ Important Disclaimer

This tool is exclusively designed for translating epub books that have entered the public domain and is not intended for copyrighted works. Please review the project's **[disclaimer](disclaimer.md)** before use.

## 📚 Documentation Sections

### Getting Started
- **[Installation](installation.md)** - How to install and set up the tool
- **[Quick Start](quickstart.md)** - Basic usage examples
- **[Environment Settings](env_settings.md)** - Configuration and API keys

### Usage Guides
- **[Command Reference](cmd.md)** - Complete command-line interface documentation
- **[Book Sources](book_source.md)** - Supported input formats and sources
- **[Model Languages](model_lang.md)** - Available translation models and languages
- **[Prompts](prompt.md)** - Customizing translation prompts

### Advanced Features
- **[Translation UI Updates](ui_updates.md)** - Web interface documentation
- **[Implementation Summary](implementation.md)** - Technical architecture overview

### Examples
- **[Commands Examples](commands_examples.md)** - Real-world usage examples from the project

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Test with sample book
python3 make_book.py --book_name test_books/animal_farm.epub --openai_key ${openai_key} --test
```

## 🔧 Supported Models

- **OpenAI**: GPT-3.5-turbo, GPT-4, GPT-4-turbo
- **Google**: Gemini Pro, Gemini Flash
- **DeepL**: Professional and free versions
- **Claude**: Anthropic's Claude models
- **Google Translate**: Free translation service
- **Caiyun**: Chinese translation service
- **Tencent TranSmart**: Professional translation
- **xAI**: xAI models
- **Ollama**: Self-hosted models
- **Groq**: High-performance inference

## 📖 Supported Formats

- **EPUB**: E-book format with HTML content
- **TXT**: Plain text files
- **SRT**: Subtitle files
- **Markdown**: Documentation files

## 🌍 Target Languages

The tool supports translation to multiple languages including:
- Simplified Chinese (default)
- Traditional Chinese
- English
- French
- German
- Spanish
- Japanese
- Korean
- And many more...

For a complete list, run: `python make_book.py --help`