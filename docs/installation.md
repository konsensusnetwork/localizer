# Installation Guide

This guide covers all the different ways to install and set up the Bilingual Book Maker.

## Prerequisites

- **Python 3.10+** (required for all installation methods)
- **Internet connection** (for downloading dependencies and API access)
- **API keys** for your chosen translation service

## Installation Methods

### Method 1: Using pip (Recommended)

The easiest way to install the tool is using pip:

```bash
# Install from PyPI
pip install bbook-maker

# Or install the latest development version
pip install git+https://github.com/yihong0618/bilingual_book_maker.git
```

After installation, you can use the `bbook_maker` command directly:

```bash
bbook_maker --book_name your_book.epub --model openai --openai_key YOUR_KEY
```

### Method 2: From Source

For development or if you need the latest features:

```bash
# Clone the repository
git clone https://github.com/yihong0618/bilingual_book_maker.git
cd bilingual_book_maker

# Install dependencies
pip install -r requirements.txt

# Run directly
python3 make_book.py --book_name your_book.epub --model openai --openai_key YOUR_KEY
```

### Method 3: Using PDM (Development)

For contributors and developers:

```bash
# Install PDM if you haven't already
pip install pdm

# Clone and setup
git clone https://github.com/yihong0618/bilingual_book_maker.git
cd bilingual_book_maker

# Install with PDM
pdm install

# Run with PDM
pdm run python make_book.py --book_name your_book.epub --model openai --openai_key YOUR_KEY
```

### Method 4: Docker

For containerized deployment:

```bash
# Build the Docker image
docker build --tag bilingual_book_maker .

# Run with volume mounting
docker run --rm \
  --mount type=bind,source=/path/to/your/books,target=/app/test_books \
  bilingual_book_maker \
  --book_name /app/test_books/your_book.epub \
  --openai_key YOUR_API_KEY \
  --language zh-hans
```

## API Key Setup

### OpenAI API Key

1. **Get your API key**:
   - Visit [OpenAI Platform](https://platform.openai.com/account/api-keys)
   - Create a new API key
   - Copy the key (starts with `sk-`)

2. **Set the key**:
   ```bash
   # Option 1: Environment variable
   export BBM_OPENAI_API_KEY="sk-your-api-key-here"
   
   # Option 2: .env file
   echo "BBM_OPENAI_API_KEY=sk-your-api-key-here" > .env
   
   # Option 3: Command line (less secure)
   --openai_key "sk-your-api-key-here"
   ```

### Google Gemini API Key

1. **Get your API key**:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the key

2. **Set the key**:
   ```bash
   # Option 1: Environment variable
   export BBM_GOOGLE_GEMINI_KEY="your-gemini-key-here"
   
   # Option 2: .env file
   echo "BBM_GOOGLE_GEMINI_KEY=your-gemini-key-here" >> .env
   
   # Option 3: Command line
   --gemini_key "your-gemini-key-here"
   ```

## Environment Variables

Create a `.env` file in your project directory for persistent configuration:

```bash
# Translation API Keys
BBM_OPENAI_API_KEY=sk-your-openai-key
BBM_GOOGLE_GEMINI_KEY=your-gemini-key

# Optional: Custom API base URL (for Azure, etc.)
BBM_OPENAI_API_BASE=https://your-endpoint.openai.azure.com/

# Optional: Deployment ID (for Azure)
BBM_OPENAI_DEPLOYMENT_ID=your-deployment-name

# Optional: Proxy settings
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
```

## Verification

Test your installation with the sample book:

```bash
# Test with OpenAI
python3 make_book.py \
  --book_name test_books/animal_farm.epub \
  --model openai \
  --openai_key YOUR_API_KEY \
  --test \
  --language zh-hans

# Test with Gemini
python3 make_book.py \
  --book_name test_books/animal_farm.epub \
  --model gemini \
  --gemini_key YOUR_API_KEY \
  --test \
  --language zh-hans
```

## API Service Setup

To run the REST API service:

```bash
# Install additional dependencies
pip install fastapi uvicorn python-multipart

# Start the API service
python run_service.py

# Or use the provided script
pdm run start-service
```

The API will be available at:
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/

## Development Setup

For contributors and developers:

```bash
# Clone the repository
git clone https://github.com/yihong0618/bilingual_book_maker.git
cd bilingual_book_maker

# Install development dependencies
pdm install

# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run tests
pdm run test-api

# Run with coverage
pdm run test-api --coverage
```

## Troubleshooting

### Common Issues

1. **"No module named 'book_maker'"**
   ```bash
   # Make sure you're in the project directory
   cd bilingual_book_maker
   pip install -e .
   ```

2. **API Key not found**
   ```bash
   # Check if environment variable is set
   echo $BBM_OPENAI_API_KEY
   
   # Or use command line argument
   --openai_key "your-key-here"
   ```

3. **Permission denied (Docker)**
   ```bash
   # Make sure the directory is readable
   chmod 755 /path/to/your/books
   ```

4. **Proxy issues**
   ```bash
   # Set proxy environment variables
   export http_proxy=http://127.0.0.1:7890
   export https_proxy=http://127.0.0.1:7890
   ```

### System Requirements

- **Memory**: Minimum 2GB RAM, 4GB+ recommended
- **Storage**: 1GB free space for installation
- **Network**: Stable internet connection for API calls
- **OS**: Linux, macOS, or Windows (with WSL recommended)

### Dependencies

The tool requires these main dependencies:
- `openai>=1.68.2` - OpenAI API client
- `google-generativeai` - Google Gemini API
- `ebooklib>=0.19` - EPUB file handling
- `beautifulsoup4` - HTML parsing
- `tiktoken` - Token counting
- `rich` - Terminal output formatting

## Next Steps

After installation, check out:
- **[Quick Start](./quickstart.md)** - Basic usage examples
- **[Command Reference](./cmd.md)** - Complete CLI documentation
- **[Examples](./commands_examples.md)** - Real-world usage scenarios 