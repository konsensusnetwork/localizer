import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Dict, Any, Optional

from book_maker.loader import BOOK_LOADER_DICT
from book_maker.translator import MODEL_DICT
from book_maker.utils import LANGUAGES

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_supported_models():
    """Get list of supported models"""
    return list(MODEL_DICT.keys())

def get_supported_languages():
    """Get list of supported languages"""
    return list(LANGUAGES.keys())

def get_project_config(key: str, project_dir: Optional[str] = None) -> Optional[str]:
    """Get API key from project-specific .env file or global .env"""
    if project_dir:
        project_env = Path(project_dir) / '.env'
        if project_env.exists():
            from dotenv import load_dotenv
            load_dotenv(dotenv_path=project_env, override=True)
            value = os.getenv(key)
            if value:
                logger.info(f"Using {key} from project-specific .env file: {project_env}")
                return value
    
    # Fallback to global .env
    from dotenv import load_dotenv
    load_dotenv()
    value = os.getenv(key)
    if value:
        logger.info(f"Using {key} from global .env file")
    return value

def parse_prompt_arg(prompt_arg: Optional[str]):
    """Parse prompt argument exactly like CLI does"""
    prompt = None
    prompt_file_path = None
    
    if prompt_arg is None:
        return prompt, prompt_file_path

    # Check if it's a path to a markdown file (PromptDown format)
    if prompt_arg.endswith(".md") and os.path.exists(prompt_arg):
        try:
            from promptdown import StructuredPrompt
            with open(prompt_arg, 'r', encoding='utf-8') as f:
                promptdown_content = f.read()
            
            structured_prompt = StructuredPrompt.from_promptdown_string(promptdown_content)
            prompt_file_path = prompt_arg
            
            prompt = {}
            system_content = None
            system_role = None
            
            if hasattr(structured_prompt, 'developer_message') and structured_prompt.developer_message:
                system_content = structured_prompt.developer_message
                system_role = 'developer'
            elif hasattr(structured_prompt, 'system_message') and structured_prompt.system_message:
                system_content = structured_prompt.system_message
                system_role = 'system'
            
            if system_content:
                import re
                invalid_placeholders = re.findall(r'\{([^{}]+)\}', system_content)
                if invalid_placeholders:
                    disallowed = [p for p in invalid_placeholders if p not in ['language', 'text', 'crlf']]
                    if disallowed:
                        raise ValueError(f"Invalid placeholders found in system/developer message: {', '.join('{' + p + '}' for p in disallowed)}")
                
                prompt['system'] = system_content
                prompt['system_role'] = system_role
            
            user_message = None
            if hasattr(structured_prompt, 'conversation') and structured_prompt.conversation:
                for message in structured_prompt.conversation:
                    if message.role.lower() == 'user':
                        user_message = message.content
                        break
                        
            if not user_message:
                raise ValueError("PromptDown file must contain at least one user message")
            
            import re
            invalid_placeholders = re.findall(r'\{([^{}]+)\}', user_message)
            allowed_placeholders = ['text', 'language', 'crlf']
            disallowed = [p for p in invalid_placeholders if p not in allowed_placeholders]
            if disallowed:
                raise ValueError(f"Invalid placeholders found in user message: {', '.join('{' + p + '}' for p in disallowed)}")
            
            if '{text}' not in user_message:
                raise ValueError("User message in PromptDown must contain `{text}` placeholder")
                
            prompt['user'] = user_message
            
            logger.info(f"Successfully loaded PromptDown file: {prompt_arg}")
            return prompt, prompt_file_path
            
        except Exception as e:
            logger.error(f"Error parsing PromptDown file: {e}")
            raise
    
    # Existing parsing logic for JSON strings and other formats
    if not any(prompt_arg.endswith(ext) for ext in [".json", ".txt", ".md"]):
        try:
            prompt = json.loads(prompt_arg)
            prompt_file_path = "inline_json"
        except json.JSONDecodeError:
            if "{text}" not in prompt_arg:
                prompt_arg = prompt_arg + " {text}"
            prompt = {"user": prompt_arg}
            prompt_file_path = "inline_template"

    elif os.path.exists(prompt_arg):
        prompt_file_path = prompt_arg
        if prompt_arg.endswith(".txt"):
            with open(prompt_arg, encoding="utf-8") as f:
                prompt = {"user": f.read()}
        elif prompt_arg.endswith(".json"):
            with open(prompt_arg, encoding="utf-8") as f:
                prompt = json.load(f)
    else:
        raise FileNotFoundError(f"{prompt_arg} not found")

    # Validate prompt structure
    if prompt is None:
        raise ValueError("prompt is None")
    
    if not isinstance(prompt, dict):
        raise ValueError(f"prompt must be a dictionary, got {type(prompt)}")
    
    if "user" not in prompt:
        raise ValueError("prompt must contain the key of `user`")
    
    if not isinstance(prompt["user"], str):
        raise ValueError(f"prompt['user'] must be a string, got {type(prompt['user'])}")
    
    if "{text}" not in prompt["user"]:
        raise ValueError("prompt must contain `{text}` placeholder")
    
    if (prompt.keys() - {"user", "system"}) != set():
        raise ValueError("prompt can only contain the keys of `user` and `system`")

    logger.info("prompt config:", prompt)
    return prompt, prompt_file_path

async def translate_book(
    book_path: str,
    model: str,
    language: str,
    model_list: Optional[str] = None,
    batch_size: Optional[int] = None,
    single_translate: bool = False,
    test_mode: bool = False,
    test_num: int = 10,
    use_context: bool = False,
    reasoning_effort: str = "medium",
    temperature: float = 1.0,
    accumulated_num: int = 1,
    block_size: int = -1,
    prompt_file: Optional[str] = None,
    user_id: str = "mock_user"
) -> Dict[str, Any]:
    """
    Translate a book using the same logic as the CLI
    """
    logger.info("=" * 80)
    logger.info("TRANSLATION JOB STARTED")
    logger.info("=" * 80)
    logger.info(f"Book Path: {book_path}")
    logger.info(f"Model: {model}")
    logger.info(f"Language: {language}")
    logger.info(f"Model List: {model_list}")
    logger.info(f"Batch Size: {batch_size}")
    logger.info(f"Single Translate: {single_translate}")
    logger.info(f"Test Mode: {test_mode}")
    logger.info(f"Test Num: {test_num}")
    logger.info(f"Use Context: {use_context}")
    logger.info(f"Reasoning Effort: {reasoning_effort}")
    logger.info(f"Temperature: {temperature}")
    logger.info(f"Accumulated Num: {accumulated_num}")
    logger.info(f"Block Size: {block_size}")
    logger.info("=" * 80)

    # Validate book path
    if not os.path.isfile(book_path):
        raise FileNotFoundError(f"Book file {book_path} does not exist")

    # Get project directory for API keys
    project_dir = os.path.dirname(os.path.abspath(book_path))

    # Get translator class
    translate_model_class = MODEL_DICT.get(model)
    if translate_model_class is None:
        raise ValueError(f"Unsupported model: {model}")

    # Get API key based on model
    api_key = ""
    if model in ["openai", "chatgptapi", "gpt4", "gpt4omini", "gpt4o"]:
        api_key = get_project_config("BBM_OPENAI_API_KEY", project_dir)
        if not api_key:
            raise Exception("OpenAI API key not provided")
    elif model == "caiyun":
        api_key = get_project_config("BBM_CAIYUN_API_KEY", project_dir)
        if not api_key:
            raise Exception("Please provide caiyun key")
    elif model == "deepl":
        api_key = get_project_config("BBM_DEEPL_API_KEY", project_dir)
        if not api_key:
            raise Exception("Please provide deepl key")
    elif model.startswith("claude"):
        api_key = get_project_config("BBM_CLAUDE_API_KEY", project_dir)
        if not api_key:
            raise Exception("Please provide claude key")
    elif model == "customapi":
        api_key = get_project_config("BBM_CUSTOM_API", project_dir)
        if not api_key:
            raise Exception("Please provide custom translate api")
    elif model in ["gemini", "geminipro"]:
        api_key = get_project_config("BBM_GOOGLE_GEMINI_KEY", project_dir)
    elif model == "groq":
        api_key = get_project_config("BBM_GROQ_API_KEY", project_dir)
    elif model == "xai":
        api_key = get_project_config("BBM_XAI_API_KEY", project_dir)

    # Get book loader based on file extension
    book_type = book_path.split(".")[-1]
    support_type_list = list(BOOK_LOADER_DICT.keys())
    if book_type not in support_type_list:
        raise Exception(f"Only support files of these formats: {','.join(support_type_list)}")

    book_loader_class = BOOK_LOADER_DICT.get(book_type)
    if book_loader_class is None:
        raise Exception("Unsupported loader")

    # Parse language
    if language in LANGUAGES:
        language = LANGUAGES.get(language, language)

    # Parse prompt
    prompt_config, prompt_file_path = parse_prompt_arg(prompt_file)

    # Create book loader instance (exactly like CLI does)
    book_loader = book_loader_class(
        book_path,
        translate_model_class,
        api_key,
        False,  # resume
        language=language,
        model_api_base=None,  # Use default
        is_test=test_mode,
        test_num=test_num,
        prompt_config=prompt_config,
        prompt_file_path=prompt_file_path,
        single_translate=single_translate,
        context_flag=use_context,
        context_paragraph_limit=0,
        temperature=temperature,
    )

    # Configure model list and other options (exactly like CLI does)
    if model in ("openai", "groq"):
        if model_list:
            book_loader.translate_model.set_model_list(model_list.split(","))
        else:
            raise ValueError("When using `openai` model, you must also provide `model_list`")
    
    if model == "chatgptapi":
        if model_list:
            book_loader.translate_model.set_model_list(model_list.split(","))
        else:
            book_loader.translate_model.set_gpt35_models()
    
    if model == "gpt4":
        book_loader.translate_model.set_gpt4_models()
    if model == "gpt4omini":
        book_loader.translate_model.set_gpt4omini_models()
    if model == "gpt4o":
        book_loader.translate_model.set_gpt4o_models()
    if model == "o1preview":
        book_loader.translate_model.set_o1preview_models()
    if model == "o1":
        book_loader.translate_model.set_o1_models()
    if model == "o1mini":
        book_loader.translate_model.set_o1mini_models()
    if model == "o3mini":
        book_loader.translate_model.set_o3mini_models()
    if model.startswith("claude-"):
        book_loader.translate_model.set_claude_model(model)
    
    if model in ("gemini", "geminipro"):
        if model_list:
            book_loader.translate_model.set_model_list(model_list.split(","))
        else:
            book_loader.translate_model.set_geminiflash_models()
    if model == "geminipro":
        book_loader.translate_model.set_geminipro_models()

    # Set reasoning effort
    if hasattr(book_loader, "translate_model"):
        book_loader.translate_model.reasoning_effort = reasoning_effort

    # Set other options
    if batch_size:
        book_loader.batch_size = batch_size
    if block_size > 0:
        book_loader.block_size = block_size
    if accumulated_num > 1:
        book_loader.accumulated_num = accumulated_num

    logger.info("Starting translation...")
    logger.info("=" * 60)

    # Call make_bilingual_book (exactly like CLI does)
    result = book_loader.make_bilingual_book()

    logger.info("Translation completed successfully")
    
    # Find the output file
    output_file = None
    if result:
        # Look for the generated file
        base_name = os.path.splitext(book_path)[0]
        dir_name = os.path.dirname(book_path)
        base_name_only = os.path.basename(base_name)
        
        # Check for files with timestamp pattern
        for file in os.listdir(dir_name):
            if file.startswith(base_name_only) and file.endswith(('.md', '.qmd', '.txt')):
                if '_' in file and any(char.isdigit() for char in file):
                    output_file = os.path.join(dir_name, file)
                    break
        
        if not output_file:
            # Fallback to original name with _bilingual suffix
            output_file = f"{base_name}_bilingual.{book_type}"

    return {
        "success": result,
        "output_file": output_file,
        "message": "Translation completed successfully" if result else "Translation failed"
    }