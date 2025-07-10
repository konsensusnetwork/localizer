# Bilingual Book Maker Documentation

Welcome to the comprehensive documentation for the **Bilingual Book Maker** - an AI-powered translation tool that creates multi-language versions of books and documents.

## What is Bilingual Book Maker?

The Bilingual Book Maker is a sophisticated AI translation tool that uses advanced language models (OpenAI GPT, Google Gemini, and others) to assist users in creating bilingual versions of various document formats. It's designed specifically for translating public domain books and documents, ensuring compliance with copyright laws.

## Key Features

- **Multi-format Support**: EPUB, TXT, SRT, Markdown (.md, .qmd)
- **Multiple AI Models**: OpenAI GPT-4, GPT-3.5, O1 models, Google Gemini
- **Bilingual Output**: Creates side-by-side original and translated text
- **Batch Processing**: Handle entire directories of markdown files
- **Resume Capability**: Continue interrupted translations
- **Custom Prompts**: Tailored translation instructions per language
- **API Service**: RESTful API for integration
- **Docker Support**: Containerized deployment

## Quick Navigation

### Getting Started
- **[Installation Guide](./installation.md)** - Set up the environment and dependencies
- **[Quick Start](./quickstart.md)** - Basic usage examples and first steps

### Usage
- **[Command Reference](./cmd.md)** - Complete CLI documentation and options
- **[Examples](./commands_examples.md)** - Real-world usage scenarios
- **[API Documentation](./api.md)** - REST API endpoints and usage

### Advanced Topics
- **[Implementation Details](./implementation.md)** - Technical architecture and design
- **[Prompt Customization](./prompts.md)** - Creating custom translation prompts
- **[Troubleshooting](./troubleshooting.md)** - Common issues and solutions

## Supported Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| EPUB | `.epub` | E-book format with HTML content |
| Text | `.txt` | Plain text files |
| Subtitles | `.srt` | SubRip subtitle format |
| Markdown | `.md`, `.qmd` | Markdown and Quarto documents |

## Supported Models

### OpenAI Models
- `gpt-4`, `gpt-4-turbo`, `gpt-4-32k`
- `gpt-3.5-turbo`, `gpt-3.5-turbo-16k`
- `gpt-4o`, `gpt-4o-mini`
- `o1-preview`, `o1-mini`, `o3-mini`

### Google Gemini Models
- `gemini-1.5-flash`, `gemini-1.5-flash-002`
- `gemini-1.5-pro`, `gemini-1.5-pro-002`
- `gemini-1.0-pro`

## Supported Languages

The tool supports 100+ languages including:
- **Chinese**: Simplified (zh-hans), Traditional (zh-hant)
- **European**: English, French, German, Spanish, Italian, Dutch
- **Asian**: Japanese, Korean, Vietnamese, Thai
- **Others**: Arabic, Russian, Portuguese, and many more

## Architecture Overview

The project follows a modular architecture:

```
bilingual_book_maker/
├── book_maker/           # Core translation engine
│   ├── cli.py           # Command-line interface
│   ├── loader/          # File format handlers
│   ├── translator/      # AI model integrations
│   └── utils.py         # Utilities and helpers
├── my_app/              # API service
│   ├── main.py          # FastAPI application
│   ├── routers/         # API endpoints
│   └── workers/         # Background tasks
├── prompts/             # Translation prompts
└── test_books/          # Sample files
```

## Quick Example

```bash
# Basic translation
python3 make_book.py --book_name test_books/animal_farm.epub \
                     --model openai \
                     --openai_key YOUR_API_KEY \
                     --language zh-hans

# Test mode (first 10 paragraphs)
python3 make_book.py --book_name test_books/animal_farm.epub \
                     --model openai \
                     --openai_key YOUR_API_KEY \
                     --test \
                     --language zh-hans
```

## Legal Notice

⚠️ **Important**: This tool is designed exclusively for translating books that have entered the public domain. It is not intended for copyrighted works. Please ensure you have the right to translate any content before using this tool.

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](../CONTRIBUTING.md) for details on how to submit issues, feature requests, or pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.

---

**Ready to get started?** Check out the [Installation Guide](./installation.md) to set up your environment, or jump to [Quick Start](./quickstart.md) for immediate usage examples. 