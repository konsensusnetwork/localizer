# Bilingual Book Maker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/bbook-maker.svg)](https://badge.fury.io/py/bbook-maker)

An AI-powered translation tool that creates bilingual versions of books and documents using advanced language models. Perfect for translating public domain works into multiple languages.

![Bilingual Book Maker Demo](https://user-images.githubusercontent.com/15976103/222317531-a05317c5-4eee-49de-95cd-04063d9539d9.png)

## ✨ Features

- **Multi-format Support**: EPUB, TXT, SRT, Markdown (.md, .qmd)
- **Multiple AI Models**: OpenAI GPT-4/3.5, Google Gemini, O1 models
- **Bilingual Output**: Side-by-side original and translated text
- **Batch Processing**: Handle entire directories of markdown files
- **Resume Capability**: Continue interrupted translations
- **Custom Prompts**: Tailored translation instructions per language
- **REST API**: Programmatic access via HTTP endpoints
- **Docker Support**: Containerized deployment
- **100+ Languages**: Comprehensive language support

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI (recommended)
pip install bbook-maker

# Or install from source
git clone https://github.com/yihong0618/bilingual_book_maker.git
cd bilingual_book_maker
pip install -r requirements.txt
```

### Basic Usage

```bash
# Test with sample book (first 10 paragraphs)
python3 make_book.py \
  --book_name test_books/animal_farm.epub \
  --model openai \
  --openai_key YOUR_API_KEY \
  --test \
  --language zh-hans

# Full translation
python3 make_book.py \
  --book_name your_book.epub \
  --model openai \
  --openai_key YOUR_API_KEY \
  --language fr
```

### Using the CLI Tool

```bash
# After pip installation
bbook_maker --book_name your_book.epub --model openai --openai_key YOUR_KEY
```

## 📚 Supported Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| EPUB | `.epub` | E-book format with HTML content |
| Text | `.txt` | Plain text files |
| Subtitles | `.srt` | SubRip subtitle format |
| Markdown | `.md`, `.qmd` | Markdown and Quarto documents |

## 🤖 Supported AI Models

### OpenAI Models
- `gpt-4`, `gpt-4-turbo`, `gpt-4-32k`
- `gpt-3.5-turbo`, `gpt-3.5-turbo-16k`
- `gpt-4o`, `gpt-4o-mini`
- `o1-preview`, `o1-mini`, `o3-mini`

### Google Gemini Models
- `gemini-1.5-flash`, `gemini-1.5-flash-002`
- `gemini-1.5-pro`, `gemini-1.5-pro-002`
- `gemini-1.0-pro`

### Model Selection

```bash
# Simple defaults
--model openai    # Uses gpt-3.5-turbo
--model gemini    # Uses gemini-1.5-flash

# Specific models
--model_list gpt-4
--model_list gemini-1.5-pro

# Multiple models for load balancing
--model_list gpt-4,gpt-3.5-turbo,gpt-4o
```

## 🌍 Language Support

The tool supports 100+ languages including:

- **Chinese**: Simplified (zh-hans), Traditional (zh-hant)
- **European**: English, French, German, Spanish, Italian, Dutch
- **Asian**: Japanese, Korean, Vietnamese, Thai
- **Others**: Arabic, Russian, Portuguese, and many more

Run `python3 make_book.py --help` to see the complete language list.

## 📖 Common Use Cases

### EPUB Translation
```bash
python3 make_book.py \
  --book_name your_book.epub \
  --model openai \
  --openai_key YOUR_API_KEY \
  --language fr
```

### Text File Translation
```bash
python3 make_book.py \
  --book_name your_document.txt \
  --model openai \
  --openai_key YOUR_API_KEY \
  --language ja \
  --batch_size 20
```

### Subtitle Translation
```bash
python3 make_book.py \
  --book_name your_subtitles.srt \
  --model openai \
  --openai_key YOUR_API_KEY \
  --language ko
```

### Markdown Directory Processing
```bash
python3 make_book.py \
  --book_name path/to/markdown/directory \
  --model openai \
  --openai_key YOUR_API_KEY \
  --language es
```

## 🔧 Advanced Features

### Context-Aware Translation
Improve translation consistency with context:

```bash
python3 make_book.py \
  --book_name your_book.epub \
  --model openai \
  --openai_key YOUR_API_KEY \
  --language fr \
  --use_context
```

### Custom Prompts
```bash
# Simple prompt
python3 make_book.py \
  --book_name your_book.epub \
  --model openai \
  --prompt "Translate {text} to {language}"

# JSON prompt file
python3 make_book.py \
  --book_name your_book.epub \
  --model openai \
  --prompt prompt_template_sample.json
```

### Resume Interrupted Translations
```bash
python3 make_book.py \
  --book_name your_book.epub \
  --model openai \
  --resume
```

## 🐳 Docker Support

```bash
# Build image
docker build --tag bilingual_book_maker .

# Run container
docker run --rm \
  --mount type=bind,source=/path/to/your/books,target=/app/test_books \
  bilingual_book_maker \
  --book_name /app/test_books/your_book.epub \
  --openai_key YOUR_API_KEY \
  --language zh-hans
```

## 🔌 API Service

Start the REST API service:

```bash
# Install API dependencies
pip install fastapi uvicorn python-multipart

# Start service
python run_service.py
```

Access the API at:
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/

## 🧪 Testing

```bash
# Run all tests
pdm run test-all

# Run API tests
pdm run test-api
pdm run test-api-verbose

# Run comprehensive example tests
pdm run test-examples

# Run specific test categories
pdm run test-examples-basic      # Basic translation tests
pdm run test-examples-models     # Model selection tests
pdm run test-examples-advanced   # Advanced features tests
pdm run test-examples-languages  # Language support tests
pdm run test-examples-prompts    # Prompt examples tests
pdm run test-examples-cli        # CLI command tests
pdm run test-examples-errors     # Error handling tests

# Run with pytest directly
pytest tests/test_examples.py -m basic -v
pytest tests/test_examples.py::TestBasicTranslation::test_epub_translation_openai -v
```

## 📚 Documentation

For comprehensive documentation, visit the **[docs folder](./docs/)**:

- **[Getting Started](./docs/index.md)** - Complete documentation overview
- **[Installation Guide](./docs/installation.md)** - Setup instructions
- **[Quick Start](./docs/quickstart.md)** - Basic usage examples
- **[Command Reference](./docs/cmd.md)** - Complete CLI documentation
- **[Examples](./docs/commands_examples.md)** - Real-world usage examples
- **[API Documentation](./docs/api.md)** - REST API endpoints
- **[Implementation Details](./docs/implementation.md)** - Technical architecture
- **[Prompt Customization](./docs/prompts.md)** - Creating custom prompts
- **[Troubleshooting](./docs/troubleshooting.md)** - Common issues and solutions

## ⚠️ Important Notice

**This tool is designed exclusively for translating books that have entered the public domain.** It is not intended for copyrighted works. Please ensure you have the right to translate any content before using this tool.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](./CONTRIBUTING.md) for details on how to submit issues, feature requests, or pull requests.

### Development Setup

```bash
# Clone and setup
git clone https://github.com/yihong0618/bilingual_book_maker.git
cd bilingual_book_maker

# Install with PDM
pdm install

# Run tests
pdm run pytest

# Format code
black make_book.py
```

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## 🙏 Acknowledgments

- [@yetone](https://github.com/yetone) for the original inspiration
- All contributors and users of this project

---

**Ready to get started?** Check out the [Installation Guide](./docs/installation.md) to set up your environment, or jump to [Quick Start](./docs/quickstart.md) for immediate usage examples.
