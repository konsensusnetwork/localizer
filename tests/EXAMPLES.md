# Test Examples for Bilingual Book Maker

This directory contains comprehensive test examples that demonstrate all the features and use cases from the README and documentation.

## 📁 Test Files

- **`test_examples.py`** - Comprehensive test suite covering all features
- **`test_api.py`** - API service tests

## 🚀 Quick Start

### 1. Check Environment Setup

First, check if your environment is properly configured:

```bash
python tests/setup_env.py
```

This will show you:
- API key status
- Test books availability
- Test prompts availability

### 2. Set Up API Keys (if needed)

If no API keys are found, create a `.env` file:

```bash
python tests/setup_env.py --create-env
```

Then edit the `.env` file with your actual API keys:
- Get OpenAI API key from: https://platform.openai.com/account/api-keys
- Get Gemini API key from: https://makersuite.google.com/app/apikey

### 3. Run Tests

```bash
# Run all comprehensive examples
pdm run test-examples

# Run specific test categories
pdm run test-examples-basic      # Basic translation tests
pdm run test-examples-models     # Model selection tests
pdm run test-examples-advanced   # Advanced features tests
pdm run test-examples-languages  # Language support tests
pdm run test-examples-prompts    # Prompt examples tests
pdm run test-examples-cli        # CLI command tests
pdm run test-examples-errors     # Error handling tests

# Run all tests (API + Examples)
pdm run test-all
```

### Using Pytest Directly

```bash
# Run all example tests
pytest tests/test_examples.py

# Run specific test categories
pytest tests/test_examples.py -m basic
pytest tests/test_examples.py -m models
pytest tests/test_examples.py -m advanced
pytest tests/test_examples.py -m languages
pytest tests/test_examples.py -m prompts
pytest tests/test_examples.py -m cli
pytest tests/test_examples.py -m errors

# Run specific test methods
pytest tests/test_examples.py::TestBasicTranslation::test_epub_translation_openai -v
pytest tests/test_examples.py::TestLanguageSupport::test_chinese_simplified -v
```

## 🧪 Test Categories

### Basic Translation Tests (`-m basic`)
- EPUB translation with OpenAI
- TXT translation with Gemini
- SRT subtitle translation

### Model Selection Tests (`-m models`)
- Specific OpenAI models (gpt-3.5-turbo, gpt-4o-mini)
- Specific Gemini models (gemini-1.5-flash)
- Multiple models for load balancing

### Advanced Features Tests (`-m advanced`)
- Context-aware translation
- Custom prompts (simple text and files)
- Batch size for TXT files
- Single translation mode

### Language Support Tests (`-m languages`)
- Chinese (Simplified/Traditional)
- Japanese, Korean
- European languages (French, German, Spanish, Italian, Portuguese)
- Russian, Arabic

### Prompt Examples Tests (`-m prompts`)
- English translation prompt
- French translation prompt
- Italian translation prompt

### CLI Command Tests (`-m cli`)
- bbook_maker command usage

### Error Handling Tests (`-m errors`)
- Missing book files
- Invalid languages

## 🔧 Environment Setup

### API Keys

Set your API keys as environment variables:

```bash
# OpenAI API key
export BBM_OPENAI_API_KEY="sk-your-openai-key"

# Gemini API key
export BBM_GOOGLE_GEMINI_KEY="your-gemini-key"
```

Or create a `.env` file:

```bash
echo "BBM_OPENAI_API_KEY=sk-your-openai-key" > .env
echo "BBM_GOOGLE_GEMINI_KEY=your-gemini-key" >> .env
```

### Test Books

The tests use these sample books:
- `test_books/animal_farm.epub` - EPUB format
- `test_books/the_little_prince.txt` - TXT format
- `test_books/Lex_Fridman_episode_322.srt` - SRT format

### Test Prompts

The tests use these prompt files:
- `prompts/en/en-translation.prompt.md` - English translation prompt
- `prompts/fr/fr-translation-1.prompt.md` - French translation prompt
- `prompts/it/it-translation.prompt.md` - Italian translation prompt

## 📊 Test Results

Tests will create temporary output files in a temporary directory. The tests verify:

1. **Command Execution**: Commands run successfully
2. **Output Files**: Bilingual/translated files are created
3. **Error Handling**: Proper error handling for invalid inputs

## 🐛 Troubleshooting

### Common Issues

1. **No API Keys**: Tests will be skipped if no API keys are available
2. **Missing Test Books**: Check that test books exist in `test_books/` directory
3. **Missing Prompts**: Check that prompt files exist in `prompts/` directory
4. **Network Issues**: Ensure internet connectivity for API calls

### Debug Mode

Run tests with verbose output to see detailed information:

```bash
pytest tests/test_examples.py -m basic -v
```

## 📝 Adding New Tests

To add new test examples:

1. Add test methods to the appropriate test class in `test_examples.py`
2. Use the `@pytest.mark.category` decorator for proper categorization
3. Follow the existing pattern for command execution and assertions
4. Update this documentation with new test examples

## 🔗 Related Documentation

- [Main README](../README.md) - Project overview and quick start
- [Installation Guide](../docs/installation.md) - Setup instructions
- [Command Reference](../docs/cmd.md) - Complete CLI documentation
- [Examples](../docs/commands_examples.md) - Real-world usage examples 