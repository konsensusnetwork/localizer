import tiktoken
import datetime
import json
import os
from pathlib import Path

# Borrowed from : https://github.com/openai/whisper
LANGUAGES = {
    "en": "english",
    "zh-hans": "simplified chinese",
    "zh": "simplified chinese",
    "zh-hant": "traditional chinese",
    "zh-yue": "cantonese",
    "de": "german",
    "es": "spanish",
    "ru": "russian",
    "ko": "korean",
    "fr": "français",
    "ja": "japanese",
    "pt": "portuguese",
    "tr": "turkish",
    "pl": "polish",
    "ca": "catalan",
    "nl": "nederlands",
    "ar": "arabic",
    "sv": "swedish",
    "it": "italian",
    "id": "indonesian",
    "hi": "hindi",
    "fi": "finnish",
    "vi": "vietnamese",
    "he": "hebrew",
    "uk": "ukrainian",
    "el": "greek",
    "ms": "malay",
    "cs": "czech",
    "ro": "romanian",
    "da": "danish",
    "hu": "hungarian",
    "ta": "tamil",
    "no": "norwegian",
    "th": "thai",
    "ur": "urdu",
    "hr": "croatian",
    "bg": "bulgarian",
    "lt": "lithuanian",
    "la": "latin",
    "mi": "maori",
    "ml": "malayalam",
    "cy": "welsh",
    "sk": "slovak",
    "te": "telugu",
    "fa": "persian",
    "lv": "latvian",
    "bn": "bengali",
    "sr": "serbian",
    "az": "azerbaijani",
    "sl": "slovenian",
    "kn": "kannada",
    "et": "estonian",
    "mk": "macedonian",
    "br": "breton",
    "eu": "basque",
    "is": "icelandic",
    "hy": "armenian",
    "ne": "nepali",
    "mn": "mongolian",
    "bs": "bosnian",
    "kk": "kazakh",
    "sq": "albanian",
    "sw": "swahili",
    "gl": "galician",
    "mr": "marathi",
    "pa": "punjabi",
    "si": "sinhala",
    "km": "khmer",
    "sn": "shona",
    "yo": "yoruba",
    "so": "somali",
    "af": "afrikaans",
    "oc": "occitan",
    "ka": "georgian",
    "be": "belarusian",
    "tg": "tajik",
    "sd": "sindhi",
    "gu": "gujarati",
    "am": "amharic",
    "yi": "yiddish",
    "lo": "lao",
    "uz": "uzbek",
    "fo": "faroese",
    "ht": "haitian creole",
    "ps": "pashto",
    "tk": "turkmen",
    "nn": "nynorsk",
    "mt": "maltese",
    "sa": "sanskrit",
    "lb": "luxembourgish",
    "my": "myanmar",
    "bo": "tibetan",
    "tl": "tagalog",
    "mg": "malagasy",
    "as": "assamese",
    "tt": "tatar",
    "haw": "hawaiian",
    "ln": "lingala",
    "ha": "hausa",
    "ba": "bashkir",
    "jw": "javanese",
    "su": "sundanese",
}

# language code lookup by name, with a few language aliases
TO_LANGUAGE_CODE = {
    **{language: code for code, language in LANGUAGES.items()},
    "burmese": "my",
    "valencian": "ca",
    "flemish": "nl",
    "haitian": "ht",
    "letzeburgesch": "lb",
    "pushto": "ps",
    "panjabi": "pa",
    "moldavian": "ro",
    "moldovan": "ro",
    "sinhalese": "si",
    "castilian": "es",
}


def prompt_config_to_kwargs(prompt_config):
    prompt_config = prompt_config or {}
    return dict(
        prompt_template=prompt_config.get("user", None),
        prompt_sys_msg=prompt_config.get("system", None),
        system_role=prompt_config.get("system_role", None),
    )


# ref: https://platform.openai.com/docs/guides/chat/introduction
def num_tokens_from_text(text, model="gpt-3.5-turbo-0301"):
    messages = (
        {
            "role": "user",
            "content": text,
        },
    )

    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
        num_tokens = 0
        for message in messages:
            num_tokens += (
                4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            )
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not presently implemented for model {model}.
  See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )

def count_tokens_with_tiktoken(messages, model="gpt-3.5-turbo"):
    """
    Returns the number of tokens used by a list of messages using tiktoken.
    Follows OpenAI's token counting approach for chat completions.
    
    Args:
        messages: List of message dictionaries with role and content
        model: The model name to use for tokenization
    
    Returns:
        int: Number of tokens used by the messages
    """
    import tiktoken
    
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # Fall back to cl100k_base encoding if model-specific encoding not found
        encoding = tiktoken.get_encoding("cl100k_base")
    
    # Base tokens for the entire messages array
    num_tokens = 3  # every reply is primed with <|start|>assistant<|message|>
    
    for message in messages:
        # Each message follows: <|im_start|>{role/name}\n{content}<|im_end|>\n
        num_tokens += 4
        
        for key, value in message.items():
            if key == "role":
                # Role is always required and usually 1 token
                num_tokens += 1
            elif key == "content" and value:
                # Add the encoded content length
                num_tokens += len(encoding.encode(value))
            elif key == "name":
                # If there's a name, the role is omitted
                num_tokens += len(encoding.encode(value))
    
    return num_tokens

def generate_output_filename(input_path, language, model_name):
    """Generate standardized output filename with date, time and model info.
    
    Args:
        input_path: Original file path
        language: Target language code (used in logs but not in filename)
        model_name: Name of the translation model used
        
    Returns:
        String containing the new filename path with pattern: 
        original_YYYYMMDD_HHMM_model.ext
    """
    path = Path(input_path)
    date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    stem = path.stem

    # Clean up model name for filename (remove special chars, limit length)
    safe_model_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in model_name)
    if len(safe_model_name) > 30:  # Limit length to avoid too long filenames
        safe_model_name = safe_model_name[:30]

    # Create new filename with pattern: original_YYYYMMDD_HHMM_model.ext
    new_filename = f"{stem}_{date_str}_{safe_model_name}{path.suffix}"

    return str(path.parent / new_filename)

def log_translation_run(input_path, output_path, run_params):
    """Log translation run parameters to a log file in the same directory.
    
    Args:
        input_path: Original file path
        output_path: Output file path
        run_params: Dictionary of run parameters
    """
    log_dir = Path(input_path).parent
    log_file = log_dir / "translation_log.json"
    
    # Count lines in input file
    input_line_count = 0
    input_file_tokens = 0
    if os.path.exists(input_path):
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                input_text = f.read()
                # Reset file pointer to beginning to count lines
                f.seek(0)
                input_line_count = sum(1 for _ in f)
            
            # Count tokens in input file
            encoding = tiktoken.get_encoding("cl100k_base")
            input_file_tokens = len(encoding.encode(input_text))
        except Exception as e:
            print(f"Warning: Could not process input file: {e}")
    
    # Count lines in output file if it exists
    output_line_count = 0
    output_file_tokens = 0
    if os.path.exists(output_path):
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                output_text = f.read()
                # Reset file pointer to beginning to count lines
                f.seek(0)
                output_line_count = sum(1 for _ in f)
            
            # Count tokens in output file
            output_file_tokens = len(encoding.encode(output_text))
        except Exception as e:
            print(f"Warning: Could not process output file: {e}")
    
    # Extract translator object if present
    translator = run_params.pop('translate_model', None)
    
    # Add timestamp and file info to parameters
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "input_file": str(Path(input_path).name),
        "input_line_count": input_line_count,
        "input_file_tokens": input_file_tokens,
        "output_file": str(Path(output_path).name),
        "output_line_count": output_line_count,
        "output_file_tokens": output_file_tokens,
        # Add batch_size if it exists in run_params
        "batch_size": run_params.get('batch_size', None),
        **run_params
    }
    
    # Check for new token info structure on the translator
    if translator and hasattr(translator, 'token_info'):
        # First check if we have cumulative token info
        if hasattr(translator, 'cumulative_token_info'):
            # Add detailed cumulative token information
            token_info = translator.cumulative_token_info
            log_entry.update({
                "system_tokens": token_info.get("system_tokens", 0),
                "user_tokens": token_info.get("user_tokens", 0),
                "intermediate_tokens": token_info.get("intermediate_tokens", 0),
                "prompt_tokens": token_info.get("prompt_tokens", 0),
                "completion_tokens": token_info.get("completion_tokens", 0),
                "total_tokens": token_info.get("total_tokens", 0),
                "total_cost": token_info.get("cost", 0)  # Add cost information
            })
        else:
            # Fall back to the last call's token info
            token_info = translator.token_info
            log_entry.update({
                "system_tokens": token_info.get("system_tokens", 0),
                "user_tokens": token_info.get("user_tokens", 0),
                "intermediate_tokens": token_info.get("intermediate_tokens", 0),
                "prompt_tokens": token_info.get("estimated_prompt_tokens", 0),
                "total_cost": token_info.get("cost", 0)  # Add cost information
            })
    
    # Add prompt info if available
    if 'prompt_file' in run_params and run_params['prompt_file']:
        # Extract the prompt template string
        prompt_template = run_params['prompt_file']
        
        # Check if it's a file path or a direct template string
        prompt_file_path = None
        if isinstance(prompt_template, str) and os.path.exists(prompt_template):
            prompt_file_path = prompt_template
            log_entry['prompt_filename'] = os.path.basename(prompt_file_path)
        elif isinstance(prompt_template, str) and len(prompt_template) > 20:
            # It's likely a direct template string, not a file path
            log_entry['prompt_filename'] = "inline_template"
        
        # Helper function to remove example text section
        def remove_example_text(text):
            if not text:
                return text
            
            # Check for the Example Text section and remove it
            example_text_markers = ["### Example Text", "### Examples", "### Example"]
            for marker in example_text_markers:
                if marker in text:
                    return text.split(marker)[0].strip()
            return text
            
        # Add full user message if we have it in the params
        if 'full_user_message' in run_params and run_params['full_user_message']:
            user_message = run_params['full_user_message']
            log_entry['full_user_message'] = remove_example_text(user_message)
        # Otherwise fallback to truncated preview from translator object 
        elif translator and hasattr(translator, 'prompt_template'):
            max_preview_length = 100
            prompt_template = getattr(translator, 'prompt_template', '')
            if prompt_template and isinstance(prompt_template, str):
                if len(prompt_template) > max_preview_length:
                    log_entry['user_message_preview'] = prompt_template[:max_preview_length] + "..."
                else:
                    log_entry['user_message_preview'] = prompt_template
        
        # Add full system message if we have it in the params
        if 'full_system_message' in run_params and run_params['full_system_message']:
            system_message = run_params['full_system_message']
            log_entry['full_system_message'] = remove_example_text(system_message)
        # Otherwise fallback to truncated preview from translator
        elif translator and hasattr(translator, 'prompt_sys_msg'):
            system_message = getattr(translator, 'prompt_sys_msg', None)
            if system_message:
                if len(system_message) > max_preview_length:
                    log_entry['system_message_preview'] = system_message[:max_preview_length] + "..."
                else:
                    log_entry['system_message_preview'] = system_message
    
    # Adjust total_cost based on the token counts and pricing model
    # Uncached tokens are billed at half the price of regular input tokens
    if "prompt_tokens" in log_entry and input_file_tokens > 0 and log_entry["prompt_tokens"] > 0:
        # Store the total maximum cost (without any caching benefit)
        uncached_cost = log_entry.get("total_cost", 0)
        log_entry["total_cost_maximum_uncached"] = uncached_cost
        
        # Calculate uncached vs cached tokens
        if log_entry["prompt_tokens"] > input_file_tokens:
            # Calculate the number of cached tokens
            cached_tokens = log_entry["prompt_tokens"] - input_file_tokens
            uncached_tokens = input_file_tokens
            
            # Calculate the cost with the pricing model:
            # - Uncached tokens billed at half price
            # - Total = (cached_tokens * full_price) + (uncached_tokens * half_price)
            
            # Calculate the proportion of each token type
            cached_ratio = cached_tokens / log_entry["prompt_tokens"]
            uncached_ratio = uncached_tokens / log_entry["prompt_tokens"]
            
            # Apply the pricing rule (uncached at half price)
            # The total cost formula: Cost = (cached_portion * full_price) + (uncached_portion * half_price)
            # Which simplifies to: Cost = full_price * (cached_ratio + uncached_ratio/2)
            adjusted_cost = uncached_cost * (cached_ratio + (uncached_ratio / 2))
            
            # Store the adjusted cost
            log_entry["total_cost"] = adjusted_cost
            
            # Print explanation of calculation
            print(f"Cost calculation with caching benefit:")
            print(f"  Maximum cost (no caching): ${uncached_cost:.6f}")
            print(f"  Cached tokens: {cached_tokens} ({cached_ratio:.2%} of total)")
            print(f"  Uncached tokens: {uncached_tokens} ({uncached_ratio:.2%} of total, billed at half price)")
            print(f"  Formula: ${uncached_cost:.6f} * ({cached_ratio:.4f} + {uncached_ratio:.4f}/2)")
            print(f"  Adjusted cost: ${adjusted_cost:.6f}")
        else:
            # If input_file_tokens >= prompt_tokens, no caching benefit was detected
            print("No caching benefit detected: input file tokens <= prompt tokens reported by API")
            log_entry["total_cost"] = uncached_cost
    
    # Write log entry to file
    log_data = {"runs": []}
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
                # Check the format of the loaded data to support both old and new formats
                if isinstance(log_data, list):
                    # New format - convert to old format with "runs" key
                    log_data = {"runs": log_data}
                elif not isinstance(log_data, dict) or "runs" not in log_data:
                    # Invalid format - reset
                    log_data = {"runs": []}
        except json.JSONDecodeError:
            # If JSON is invalid, start fresh
            log_data = {"runs": []}
    
    # Add new entry and save
    log_data["runs"].append(log_entry)
    
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)
    
    print(f"Translation run logged to {log_file}")
