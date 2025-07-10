# Implementation Details

This document provides a deep dive into the technical architecture and implementation details of the Bilingual Book Maker.

## Architecture Overview

The Bilingual Book Maker follows a modular, extensible architecture designed for maintainability and scalability.

```
bilingual_book_maker/
├── book_maker/           # Core translation engine
│   ├── cli.py           # Command-line interface & orchestration
│   ├── loader/          # File format handlers
│   │   ├── base_loader.py      # Abstract base class
│   │   ├── epub_loader.py      # EPUB processing
│   │   ├── txt_loader.py       # Text file processing
│   │   ├── srt_loader.py       # Subtitle processing
│   │   ├── md_loader.py        # Markdown processing
│   │   └── helper.py           # EPUB helper functions
│   ├── translator/      # AI model integrations
│   │   ├── base_translator.py  # Abstract base class
│   │   ├── chatgptapi_translator.py  # OpenAI models
│   │   ├── gemini_translator.py      # Google Gemini
│   │   └── [other translators]       # Additional providers
│   ├── utils.py         # Utilities and helpers
│   ├── config.py        # Configuration management
│   └── obok.py          # Kobo device integration
├── my_app/              # API service
│   ├── main.py          # FastAPI application
│   ├── core.py          # Core business logic
│   ├── routers/         # API endpoints
│   │   ├── auth.py      # Authentication
│   │   └── translate.py # Translation endpoints
│   ├── workers/         # Background tasks
│   │   └── tasks.py     # Celery tasks
│   └── supabase_client.py # Database integration
└── prompts/             # Translation prompts by language
```

## Core Components

### 1. Command-Line Interface (`cli.py`)

The CLI module serves as the main entry point and orchestrates the entire translation process.

**Key Responsibilities:**
- Argument parsing and validation
- Environment configuration
- Model and loader selection
- Process orchestration

**Key Functions:**
```python
def main():
    # Parse command-line arguments
    # Validate configuration
    # Select appropriate loader and translator
    # Execute translation process

def parse_prompt_arg(prompt_arg):
    # Parse custom prompts from various formats
    # Support JSON, text, and PromptDown formats
```

### 2. Loader System (`loader/`)

The loader system handles different file formats through a common interface.

#### Base Loader (`base_loader.py`)

```python
class BaseBookLoader(ABC):
    @abstractmethod
    def make_bilingual_book(self):
        pass
    
    @abstractmethod
    def load_state(self):
        pass
    
    @abstractmethod
    def _save_temp_book(self):
        pass
```

#### EPUB Loader (`epub_loader.py`)

**Features:**
- EPUB file parsing and extraction
- HTML content processing
- Tag-based translation filtering
- Progress tracking and resume capability

**Key Methods:**
```python
class EPUBBookLoader(BaseBookLoader):
    def make_bilingual_book(self):
        # Extract EPUB content
        # Process HTML elements
        # Translate selected content
        # Rebuild EPUB with translations
    
    def _process_paragraph(self, p, translate_model):
        # Handle individual paragraph translation
        # Apply styling and formatting
```

#### Text Loader (`txt_loader.py`)

**Features:**
- Line-by-line or batch processing
- Special text filtering
- Progress tracking

#### Markdown Loader (`md_loader.py`)

**Features:**
- Markdown parsing and preservation
- Batch processing for efficiency
- Directory processing support

#### SRT Loader (`srt_loader.py`)

**Features:**
- SubRip subtitle format parsing
- Timestamp preservation
- Block-based translation

### 3. Translator System (`translator/`)

The translator system provides a unified interface for different AI models.

#### Base Translator (`base_translator.py`)

```python
class Base(ABC):
    def __init__(self, key, language):
        self.keys = itertools.cycle(key.split(","))
        self.language = language
        self.api_call_count = 0
    
    @abstractmethod
    def translate(self, text):
        pass
```

#### OpenAI Translator (`chatgptapi_translator.py`)

**Features:**
- Support for all OpenAI models (GPT-3.5, GPT-4, O1, O3)
- Token counting and management
- Rate limiting and retry logic
- Context-aware translation
- Model load balancing

**Key Methods:**
```python
class ChatGPTAPI(Base):
    def translate(self, text):
        # Prepare prompt with context
        # Call OpenAI API
        # Handle rate limits and errors
        # Return translation
    
    def set_model_list(self, model_list):
        # Configure multiple models for load balancing
    
    def set_deployment_id(self, deployment_id):
        # Configure Azure deployment
```

#### Gemini Translator (`gemini_translator.py`)

**Features:**
- Google Gemini model support
- Request interval control
- Error handling and retries

### 4. API Service (`my_app/`)

The API service provides RESTful endpoints for programmatic access.

#### FastAPI Application (`main.py`)

```python
app = FastAPI(title="Book Translation Service")

# Include routers
app.include_router(auth.router, prefix="/auth")
app.include_router(translate.router, prefix="/translate")
```

#### Translation Router (`routers/translate.py`)

**Endpoints:**
- `POST /translate/start` - Start translation job
- `GET /translate/jobs` - List all jobs
- `GET /translate/jobs/{job_id}` - Get job status
- `GET /translate/models` - Get supported models
- `GET /translate/languages` - Get supported languages

#### Background Tasks (`workers/tasks.py`)

**Features:**
- Celery integration for async processing
- Job status tracking
- Error handling and retries

## Translation Process Flow

### 1. Initialization Phase

```python
# 1. Parse command-line arguments
options = parser.parse_args()

# 2. Validate file and model
book_type = options.book_name.split(".")[-1]
book_loader_class = BOOK_LOADER_DICT.get(book_type)
translate_model_class = MODEL_DICT.get(model)

# 3. Initialize components
book_loader = book_loader_class(
    options.book_name,
    translate_model_class,
    API_KEY,
    options.resume,
    language=language,
    # ... other options
)
```

### 2. Translation Execution

```python
# 1. Load and parse source file
book_loader.load_book()

# 2. Extract translatable content
content_blocks = book_loader.extract_content()

# 3. Process each block
for block in content_blocks:
    # Prepare context if enabled
    if use_context:
        context = build_context(previous_blocks)
    
    # Translate block
    translation = translate_model.translate(block, context)
    
    # Apply styling and formatting
    formatted_translation = apply_styling(translation)
    
    # Save progress
    book_loader.save_progress()

# 4. Generate output file
book_loader.generate_output()
```

### 3. Context Management

When `--use_context` is enabled:

```python
def build_context(previous_blocks):
    # Summarize previous content
    summary = summarize_blocks(previous_blocks)
    
    # Limit context size
    if len(summary) > context_limit:
        summary = truncate_context(summary)
    
    return summary
```

## File Format Processing

### EPUB Processing

1. **Extraction**: Extract HTML content from EPUB
2. **Parsing**: Parse HTML with BeautifulSoup
3. **Filtering**: Apply tag-based filtering
4. **Translation**: Translate selected content
5. **Rebuilding**: Rebuild EPUB with translations

### Markdown Processing

1. **Parsing**: Parse markdown structure
2. **Batching**: Group paragraphs for efficiency
3. **Translation**: Translate batches
4. **Reconstruction**: Rebuild markdown with translations

### SRT Processing

1. **Parsing**: Parse subtitle blocks and timestamps
2. **Grouping**: Group blocks for translation
3. **Translation**: Translate text content
4. **Reconstruction**: Rebuild SRT with translations

## Error Handling and Recovery

### 1. API Error Handling

```python
def translate_with_retry(text, max_retries=3):
    for attempt in range(max_retries):
        try:
            return translate_model.translate(text)
        except RateLimitError:
            wait_for_rate_limit()
        except APIError as e:
            if attempt == max_retries - 1:
                raise
            wait_before_retry(attempt)
```

### 2. Progress Tracking

```python
def save_progress(self):
    progress_data = {
        'translated_blocks': self.translated_blocks,
        'current_position': self.current_position,
        'timestamp': datetime.now().isoformat()
    }
    with open(self.progress_file, 'w') as f:
        json.dump(progress_data, f)
```

### 3. Resume Capability

```python
def load_state(self):
    if os.path.exists(self.progress_file):
        with open(self.progress_file, 'r') as f:
            progress_data = json.load(f)
        self.translated_blocks = progress_data['translated_blocks']
        self.current_position = progress_data['current_position']
```

## Performance Optimizations

### 1. Batch Processing

```python
def process_batch(self, blocks):
    # Combine multiple blocks for efficiency
    combined_text = "\n\n".join(blocks)
    translation = self.translate_model.translate(combined_text)
    return split_translation(translation)
```

### 2. Model Load Balancing

```python
def get_next_model(self):
    # Rotate through available models
    model = next(self.model_cycle)
    return model
```

### 3. Token Management

```python
def count_tokens(self, text):
    # Use tiktoken for accurate token counting
    encoding = tiktoken.encoding_for_model(self.model)
    return len(encoding.encode(text))
```

## Configuration Management

### Environment Variables

```python
def get_project_config(key, project_dir=None):
    # Load from project-specific .env file
    if project_dir:
        project_env = Path(project_dir) / '.env'
        if project_env.exists():
            load_dotenv(dotenv_path=project_env, override=True)
    
    # Fallback to global .env
    load_dotenv()
    return os.getenv(key)
```

### Model Configuration

```python
MODEL_DICT = {
    # OpenAI models
    "gpt-4": ChatGPTAPI,
    "gpt-3.5-turbo": ChatGPTAPI,
    "o1-mini": ChatGPTAPI,
    
    # Gemini models
    "gemini-1.5-flash": Gemini,
    "gemini-1.5-pro": Gemini,
}
```

## Security Considerations

### 1. API Key Management

- Environment variables for sensitive data
- Project-specific configuration files
- No hardcoded keys in source code

### 2. Input Validation

```python
def validate_file_path(file_path):
    # Check file exists and is readable
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Validate file extension
    supported_extensions = ['.epub', '.txt', '.srt', '.md', '.qmd']
    if not any(file_path.endswith(ext) for ext in supported_extensions):
        raise ValueError(f"Unsupported file format")
```

### 3. Output Sanitization

```python
def sanitize_output(text):
    # Remove potentially harmful content
    # Validate HTML structure
    # Ensure proper encoding
    return cleaned_text
```

## Testing Strategy

### 1. Unit Tests

- Individual component testing
- Mock API responses
- Error condition testing

### 2. Integration Tests

- End-to-end translation testing
- File format processing
- API service testing

### 3. Performance Tests

- Large file processing
- Memory usage monitoring
- API rate limit testing

## Deployment Considerations

### 1. Docker Support

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["python3", "make_book.py"]
```

### 2. API Service Deployment

```bash
# Start FastAPI service
uvicorn my_app.main:app --host 0.0.0.0 --port 8000

# With multiple workers
uvicorn my_app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 3. Background Task Processing

```bash
# Start Celery worker
celery -A my_app.workers.tasks worker --loglevel=info

# Start Celery beat (for scheduled tasks)
celery -A my_app.workers.tasks beat --loglevel=info
```

## Future Enhancements

### 1. Additional File Formats

- PDF support
- DOCX processing
- HTML file handling

### 2. Advanced Features

- OCR integration for image-based content
- Voice synthesis for audio output
- Real-time collaboration features

### 3. Performance Improvements

- Parallel processing
- Caching mechanisms
- CDN integration for large files

## Contributing to the Codebase

### 1. Adding New Translators

```python
class NewTranslator(Base):
    def __init__(self, key, language):
        super().__init__(key, language)
        # Initialize your translator
    
    def translate(self, text):
        # Implement translation logic
        return translated_text
```

### 2. Adding New Loaders

```python
class NewFormatLoader(BaseBookLoader):
    def make_bilingual_book(self):
        # Implement file processing logic
        pass
    
    def load_state(self):
        # Implement state loading
        pass
```

### 3. Code Style Guidelines

- Follow PEP 8 style guide
- Use type hints
- Write comprehensive docstrings
- Include unit tests for new features

## Next Steps

- **[API Documentation](./api.md)** - REST API details
- **[Troubleshooting](./troubleshooting.md)** - Common issues and solutions
- **[Prompt Customization](./prompts.md)** - Creating custom translation prompts 