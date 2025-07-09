**[中文](./README-CN.md) | English**
[![litellm](https://img.shields.io/badge/%20%F0%9F%9A%85%20liteLLM-OpenAI%7CAzure%7CAnthropic%7CPalm%7CCohere%7CReplicate%7CHugging%20Face-blue?color=green)](https://github.com/BerriAI/litellm)

# bilingual_book_maker

The bilingual_book_maker is an AI translation tool that uses ChatGPT to assist users in creating multi-language versions of epub/txt/srt files and books. This tool is exclusively designed for translating epub books that have entered the public domain and is not intended for copyrighted works. Before using this tool, please review the project's **[disclaimer](./docs/disclaimer.md)**.

![image](https://user-images.githubusercontent.com/15976103/222317531-a05317c5-4eee-49de-95cd-04063d9539d9.png)

## 📚 Documentation

For comprehensive documentation, please visit the **[docs folder](./docs/)** which contains:

- **[Getting Started](./docs/index.md)** - Complete documentation overview
- **[Installation Guide](./docs/installation.md)** - Setup instructions
- **[Quick Start](./docs/quickstart.md)** - Basic usage examples
- **[Command Reference](./docs/cmd.md)** - Complete CLI documentation
- **[Examples](./docs/commands_examples.md)** - Real-world usage examples
- **[Implementation Details](./docs/implementation.md)** - Technical architecture

## Supported Models

**OpenAI Models:**
- `gpt-4`, `gpt-4-turbo`, `gpt-4-32k`, `gpt-4-0613`, `gpt-4-32k-0613`
- `gpt-4-1106-preview`, `gpt-4-0125-preview`
- `gpt-3.5-turbo`, `gpt-3.5-turbo-0125`, `gpt-3.5-turbo-1106`, `gpt-3.5-turbo-16k`
- `gpt-4o`, `gpt-4o-mini`
- `o1-preview`, `o1-mini`, `o3-mini`

**Gemini Models:**
- `gemini-1.5-flash`, `gemini-1.5-flash-002`, `gemini-1.5-flash-8b`, `gemini-1.5-flash-8b-exp-0924`
- `gemini-1.5-pro`, `gemini-1.5-pro-002`
- `gemini-1.0-pro`

**Model Selection:** You can use either:
- `--model` with simple defaults: `--model openai` (uses gpt-3.5-turbo) or `--model gemini` (uses gemini-1.5-flash)
- `--model_list` for precise control: specify exact model names like `--model_list gpt-4,gpt-3.5-turbo`

## Preparation

1. ChatGPT or OpenAI token [^token]
2. epub/txt books
3. Environment with internet access or proxy
4. Python 3.8+

## Quick Start

A sample book, `test_books/animal_farm.epub`, is provided for testing purposes.

```shell
pip install -r requirements.txt
# Simple usage with defaults
python3 make_book.py --book_name test_books/animal_farm.epub --model openai --openai_key ${openai_key} --test
# Or specify exact model
python3 make_book.py --book_name test_books/animal_farm.epub --model_list gpt-3.5-turbo --openai_key ${openai_key} --test

OR

pip install -U bbook_maker
# Simple usage with defaults
bbook --book_name test_books/animal_farm.epub --model openai --openai_key ${openai_key} --test
# Or specify exact model
bbook --book_name test_books/animal_farm.epub --model_list gpt-3.5-turbo --openai_key ${openai_key} --test
```

## Testing

The project includes a comprehensive test suite that uses the test books and basic prompts:

```bash
# Run all tests
python tests/run_tests.py

# Run specific test types
python tests/run_tests.py --type basic    # Basic prompt tests
python tests/run_tests.py --type cli      # CLI command tests
python tests/run_tests.py --type integration  # Integration tests
python tests/run_tests.py --type markdown # Markdown and quarto tests

# Check test environment
python tests/run_tests.py --check-env

# Run with coverage
python tests/run_tests.py --coverage
```

## Translate Service

### Basic Usage

- Use `--openai_key` option to specify OpenAI API key. If you have multiple keys, separate them by commas (xxx,xxx,xxx) to reduce errors caused by API call limits.
  Or, just set environment variable `BBM_OPENAI_API_KEY` instead.
- Use `--gemini_key` option to specify Gemini API key, or set environment variable `BBM_GOOGLE_GEMINI_KEY` instead.
- A sample book, `test_books/animal_farm.epub`, is provided for testing purposes.
- **Model Selection:** Choose either:
  - `--model openai` or `--model gemini` for simple usage with sensible defaults
  - `--model_list` to specify exact model names (e.g., `gpt-4`, `gpt-3.5-turbo`, `gemini-1.5-flash-002`)
- You can specify multiple models separated by commas for load balancing: `--model_list gpt-4,gpt-3.5-turbo,gpt-4o`.
- You can add `--use_context` to add a context paragraph to each passage sent to the model for translation (see below).

### OpenAI Models

**Simple Usage (with defaults):**
```shell
# Use OpenAI with default model (gpt-3.5-turbo)
python3 make_book.py --book_name test_books/animal_farm.epub --model openai --openai_key ${openai_key}
```

**Advanced Usage (specific models):**
```shell
# Use GPT-4
python3 make_book.py --book_name test_books/animal_farm.epub --model_list gpt-4 --openai_key ${openai_key}

# Use GPT-3.5-turbo
python3 make_book.py --book_name test_books/animal_farm.epub --model_list gpt-3.5-turbo --openai_key ${openai_key}

# Use multiple models for load balancing
python3 make_book.py --book_name test_books/animal_farm.epub --model_list gpt-4,gpt-3.5-turbo,gpt-4o --openai_key ${openai_key}

# Use O1 models
python3 make_book.py --book_name test_books/animal_farm.epub --model_list o1-mini --openai_key ${openai_key}
```

### Gemini Models

**Simple Usage (with defaults):**
```shell
# Use Gemini with default model (gemini-1.5-flash)
python3 make_book.py --book_name test_books/animal_farm.epub --model gemini --gemini_key ${gemini_key}
```

**Advanced Usage (specific models):**
```shell
# Use Gemini Flash
python3 make_book.py --book_name test_books/animal_farm.epub --model_list gemini-1.5-flash --gemini_key ${gemini_key}

# Use Gemini Pro
python3 make_book.py --book_name test_books/animal_farm.epub --model_list gemini-1.5-pro --gemini_key ${gemini_key}

# Use specific Gemini model version
python3 make_book.py --book_name test_books/animal_farm.epub --model_list gemini-1.5-flash-002 --gemini_key ${gemini_key}

# Use multiple Gemini models
python3 make_book.py --book_name test_books/animal_farm.epub --model_list gemini-1.5-flash,gemini-1.5-pro --gemini_key ${gemini_key}
```

### Ollama Support

For Ollama models, use the OpenAI-compatible endpoint:

```shell
python3 make_book.py --book_name test_books/animal_farm.epub --model_list gpt-3.5-turbo --ollama_model ${ollama_model_name} --api_base http://localhost:11434/v1
```

## Use

- Once the translation is complete, a bilingual book named `${book_name}_bilingual.epub` would be generated.
- If there are any errors or you wish to interrupt the translation by pressing `CTRL+C`. A book named `{book_name}_bilingual_temp.epub` would be generated. You can simply rename it to any desired name.

## Params

- `--test`:

  Use `--test` option to preview the result if you haven't paid for the service. Note that there is a limit and it may take some time.

- `--language`:

  Set the target language like `--language "Simplified Chinese"`. Default target language is `"Simplified Chinese"`.
  Read available languages by helper message: `python make_book.py --help`

- `--proxy`:

  Use `--proxy` option to specify proxy server for internet access. Enter a string such as `http://127.0.0.1:7890`.

- `--resume`:

  Use `--resume` option to manually resume the process after an interruption.

  ```shell
  python3 make_book.py --book_name test_books/animal_farm.epub --model google --resume
  ```

- `--translate-tags`:

  epub is made of html files. By default, we only translate contents in `<p>`.
  Use `--translate-tags` to specify tags need for translation. Use comma to separate multiple tags.
  For example: `--translate-tags h1,h2,h3,p,div`

- `--book_from`:

  Use `--book_from` option to specify e-reader type (Now only `kobo` is available), and use `--device_path` to specify the mounting point.

- `--api_base`:

  If you want to change api_base like using Cloudflare Workers, use `--api_base <URL>` to support it.
  **Note: the api url should be '`https://xxxx/v1`'. Quotation marks are required.**

- `--allow_navigable_strings`:

  If you want to translate strings in an e-book that aren't labeled with any tags, you can use the `--allow_navigable_strings` parameter. This will add the strings to the translation queue. **Note that it's best to look for e-books that are more standardized if possible.**

- `--prompt`:

  To tweak the prompt, use the `--prompt` parameter. Valid placeholders for the `user` role template include `{text}` and `{language}`. It supports a few ways to configure the prompt:

  - If you don't need to set the `system` role content, you can simply set it up like this: `--prompt "Translate {text} to {language}."` or `--prompt prompt_template_sample.txt` (example of a text file can be found at [./prompt_template_sample.txt](./prompt_template_sample.txt)).

  - If you need to set the `system` role content, you can use the following format: `--prompt '{"user":"Translate {text} to {language}", "system": "You are a professional translator."}'` or `--prompt prompt_template_sample.json` (example of a JSON file can be found at [./prompt_template_sample.json](./prompt_template_sample.json)).
  
  - You can now use [PromptDown](https://github.com/btfranklin/promptdown) format (`.md` files) for more structured prompts: `--prompt prompt_md.prompt.md`. PromptDown supports both traditional system messages and developer messages (used by newer AI models). Example:
  
      ```markdown
      # Translation Prompt
      
      ## Developer Message
      You are a professional translator who specializes in accurate translations.
      
      ## Conversation
      
      | Role  | Content                                           |
      |-------|---------------------------------------------------|
      | User  | Please translate the following text into {language}:\n\n{text} |
      ```

  - You can also set the `user` and `system` role prompt by setting environment variables: `BBM_CHATGPTAPI_USER_MSG_TEMPLATE` and `BBM_CHATGPTAPI_SYS_MSG`.

- `--batch_size`:

  Use the `--batch_size` parameter to specify the number of lines for batch translation (default is 10, currently only effective for txt files).

- `--accumulated_num`:

  Wait for how many tokens have been accumulated before starting the translation. gpt3.5 limits the total_token to 4090. For example, if you use `--accumulated_num 1600`, maybe openai will output 2200 tokens and maybe 200 tokens for other messages in the system messages user messages, 1600+2200+200=4000, So you are close to reaching the limit. You have to choose your own
  value, there is no way to know if the limit is reached before sending

- `--use_context`:

  prompts the model to create a three-paragraph summary. If it's the beginning of the translation, it will summarize the entire passage sent (the size depending on `--accumulated_num`).
  For subsequent passages, it will amend the summary to include details from the most recent passage, creating a running one-paragraph context payload of the important details of the entire translated work. This improves consistency of flow and tone throughout the translation. This option is available for all ChatGPT-compatible models and Gemini models.

- `--context_paragraph_limit`:

  Use `--context_paragraph_limit` to set a limit on the number of context paragraphs when using the `--use_context` option.

- `--temperature`:

  Use `--temperature` to set the temperature parameter for `chatgptapi`/`gpt4`/`claude` models.
  For example: `--temperature 0.7`.

- `--block_size`:

  Use `--block_size` to merge multiple paragraphs into one block. This may increase accuracy and speed up the process but can disturb the original format. Must be used with `--single_translate`.
  For example: `--block_size 5 --single_translate`.

- `--single_translate`:

  Use `--single_translate` to output only the translated book without creating a bilingual version.

- `--translation_style`:

  example: `--translation_style "color: #808080; font-style: italic;"`

- `--retranslate "$translated_filepath" "file_name_in_epub" "start_str" "end_str"(optional)`:

  Retranslate from start_str to end_str's tag:

  ```shell
  python3 "make_book.py" --book_name "test_books/animal_farm.epub" --retranslate 'test_books/animal_farm_bilingual.epub' 'index_split_002.html' 'in spite of the present book shortage which' 'This kind of thing is not a good symptom. Obviously'
  ```

  Retranslate start_str's tag:

  ```shell
  python3 "make_book.py" --book_name "test_books/animal_farm.epub" --retranslate 'test_books/animal_farm_bilingual.epub' 'index_split_002.html' 'in spite of the present book shortage which'
  ```

### Examples

**Note if use `pip install bbook_maker` all commands can change to `bbook_maker args`**

```shell
# Test quickly with default OpenAI model (gpt-3.5-turbo)
python3 make_book.py --book_name test_books/animal_farm.epub --model openai --openai_key ${openai_key} --test --language zh-hans

# Test quickly for srt file with default OpenAI model
python3 make_book.py --book_name test_books/Lex_Fridman_episode_322.srt --model openai --openai_key ${openai_key} --test

# Or translate the whole book with default Gemini model
python3 make_book.py --book_name test_books/animal_farm.epub --model gemini --gemini_key ${gemini_key} --language zh-hans

# Or translate the whole book using specific GPT-4 model
python3 make_book.py --book_name test_books/animal_farm.epub --model_list gpt-4 --openai_key ${openai_key} --language zh-hans

# Use a specific list of Gemini model aliases
python3 make_book.py --book_name test_books/animal_farm.epub --model_list gemini-1.5-flash-002,gemini-1.5-flash-8b-exp-0924 --gemini_key ${gemini_key}

# Set env OPENAI_API_KEY to ignore option --openai_key
export OPENAI_API_KEY=${your_api_key}

# Use the GPT-4 model with context to Japanese
python3 make_book.py --book_name test_books/animal_farm.epub --model_list gpt-4 --use_context --language ja

# Use a specific OpenAI model
python3 make_book.py --book_name test_books/animal_farm.epub --model_list gpt-4-1106-preview --openai_key ${openai_key}

# Use multiple OpenAI models for load balancing
python3 make_book.py --book_name test_books/animal_farm.epub --model_list gpt-4-1106-preview,gpt-4-0125-preview,gpt-3.5-turbo-0125 --openai_key ${openai_key}

# Translate contents in <div> and <p> using simple defaults
python3 make_book.py --book_name test_books/animal_farm.epub --model openai --translate-tags div,p

# Tweaking the prompt with simple defaults
python3 make_book.py --book_name test_books/animal_farm.epub --model openai --prompt prompt_template_sample.txt
# or
python3 make_book.py --book_name test_books/animal_farm.epub --model openai --prompt prompt_template_sample.json
# or
python3 make_book.py --book_name test_books/animal_farm.epub --model openai --prompt "Please translate \`{text}\` to {language}"

# Translate books download from Rakuten Kobo on kobo e-reader
python3 make_book.py --book_from kobo --device_path /tmp/kobo --model openai

# translate txt file
python3 make_book.py --book_name test_books/the_little_prince.txt --model openai --test --language zh-hans
# aggregated translation txt file
python3 make_book.py --book_name test_books/the_little_prince.txt --model openai --test --batch_size 20

```

More understandable example

```shell
python3 make_book.py --book_name 'animal_farm.epub' --openai_key sk-XXXXX --api_base 'https://xxxxx/v1'

# Or python3 is not in your PATH
python make_book.py --book_name 'animal_farm.epub' --openai_key sk-XXXXX --api_base 'https://xxxxx/v1'
```

Microsoft Azure Endpoints

```shell
python3 make_book.py --book_name 'animal_farm.epub' --openai_key XXXXX --api_base 'https://example-endpoint.openai.azure.com' --deployment_id 'deployment-name'

# Or python3 is not in your PATH
python make_book.py --book_name 'animal_farm.epub' --openai_key XXXXX --api_base 'https://example-endpoint.openai.azure.com' --deployment_id 'deployment-name'
```

## Docker

You can use [Docker](https://www.docker.com/) if you don't want to deal with setting up the environment.

```shell
# Build image
docker build --tag bilingual_book_maker .

# Run container
# "$folder_path" represents the folder where your book file locates. Also, it is where the processed file will be stored.

# Windows PowerShell
$folder_path=your_folder_path # $folder_path="C:\Users\user\mybook\"
$book_name=your_book_name # $book_name="animal_farm.epub"
$openai_key=your_api_key # $openai_key="sk-xxx"
$language=your_language # see utils.py

docker run --rm --name bilingual_book_maker --mount type=bind,source=$folder_path,target='/app/test_books' bilingual_book_maker --book_name "/app/test_books/$book_name" --openai_key $openai_key --language $language

# Linux
export folder_path=${your_folder_path}
export book_name=${your_book_name}
export openai_key=${your_api_key}
export language=${your_language}

docker run --rm --name bilingual_book_maker --mount type=bind,source=${folder_path},target='/app/test_books' bilingual_book_maker --book_name "/app/test_books/${book_name}" --openai_key ${openai_key} --language "${language}"
```

For example:

```shell
# Linux
docker run --rm --name bilingual_book_maker --mount type=bind,source=/home/user/my_books,target='/app/test_books' bilingual_book_maker --book_name /app/test_books/animal_farm.epub --openai_key sk-XXX --test --test_num 1 --language zh-hant
```

## Notes

1. API token from free trial has limit. If you want to speed up the process, consider paying for the service or use multiple OpenAI tokens
2. PR is welcome

# Thanks

- @[yetone](https://github.com/yetone)

# Contribution

- Any issues or PRs are welcome.
- TODOs in the issue can also be selected.
- Please run `black make_book.py`[^black] before submitting the code.

# Others better

- 书译 iOS -> [AI 全书翻译工具](https://apps.apple.com/cn/app/%E4%B9%A6%E8%AF%91-ai-%E5%85%A8%E4%B9%A6%E7%BF%BB%E8%AF%91%E5%B7%A5%E5%85%B7/id6447665417)

## Appreciation

Thank you, that's enough.

![image](https://user-images.githubusercontent.com/15976103/222407199-1ed8930c-13a8-402b-9993-aaac8ee84744.png)

[^token]: https://platform.openai.com/account/api-keys
[^black]: https://github.com/psf/black

### Processing a Directory of Files

You can now process a directory containing markdown files (.md and .qmd) in a single command:

```shell
python3 make_book.py --book_name path/to/your/directory --openai_key ${openai_key} --language zh-hans
```

This will:
- Find all markdown files in the directory (both .md and .qmd)
- Skip any files with "_bilingual" in the name (already processed files)
- Translate each file using the markdown processor
- Output translated files with "_bilingual" suffix in the same directory

This is particularly useful for translating a collection of markdown chapter files or a complete manuscript split into multiple documents.

## Processing Directories of Markdown Files

You can now process entire directories containing markdown files:

```shell
python3 make_book.py --book_name path/to/markdown_directory --openai_key ${openai_key}
```

This will:
- Recursively find all markdown files (`.md` and `.qmd`) in the directory
- Process each file to create a bilingual version with "_bilingual" added to the filename
- Skip any files that already have "_bilingual" in their name
- Display a summary of successful and failed translations

You can combine this with other options like `--language`, `--model`, and `--test`.
