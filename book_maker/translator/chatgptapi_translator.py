import re
import time
import os
import shutil
from copy import copy
from os import environ
from itertools import cycle
import json

from openai import AzureOpenAI, OpenAI, RateLimitError
from rich import print

from .base_translator import Base
from ..config import config
from ..utils import count_tokens_with_tiktoken

CHATGPT_CONFIG = config["translator"]["chatgptapi"]

PROMPT_ENV_MAP = {
    "user": "BBM_CHATGPTAPI_USER_MSG_TEMPLATE",
    "system": "BBM_CHATGPTAPI_SYS_MSG",
}

GPT35_MODEL_LIST = [
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-1106",
    "gpt-3.5-turbo-16k",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-0301",
    "gpt-3.5-turbo-0125",
]
GPT4_MODEL_LIST = [
    "gpt-4-1106-preview",
    "gpt-4",
    "gpt-4-32k",
    "gpt-4o-2024-05-13",
    "gpt-4-0613",
    "gpt-4-32k-0613",
]

GPT4oMINI_MODEL_LIST = [
    "gpt-4o-mini",
    "gpt-4o-mini-2024-07-18",
]
GPT4o_MODEL_LIST = [
    "gpt-4o",
    "gpt-4o-2024-05-13",
    "gpt-4o-2024-08-06",
    "chatgpt-4o-latest",
]


class ChatGPTAPI(Base):
    DEFAULT_PROMPT = "Please help me to translate,`{text}` to {language}, please return only translated content not include the origin text"

    def __init__(
        self,
        key,
        language,
        api_base=None,
        prompt_template=None,
        prompt_sys_msg=None,
        temperature=1.0,
        context_flag=False,
        context_paragraph_limit=0,
        system_role=None,
        **kwargs,
    ) -> None:
        super().__init__(key, language)
        self.key_len = len(key.split(","))
        self.openai_client = OpenAI(api_key=next(self.keys), base_url=api_base)
        self.api_base = api_base

        self.prompt_template = (
            prompt_template
            or environ.get(PROMPT_ENV_MAP["user"])
            or self.DEFAULT_PROMPT
        )
        self.prompt_sys_msg = (
            prompt_sys_msg
            or environ.get(
                "OPENAI_API_SYS_MSG",
            )  # XXX: for backward compatibility, deprecate soon
            or environ.get(PROMPT_ENV_MAP["system"])
            or ""
        )
        self.system_content = environ.get("OPENAI_API_SYS_MSG") or ""
        self.deployment_id = None
        self.temperature = temperature
        self.model_list = None
        self.context_flag = context_flag
        self.context_list = []
        self.context_translated_list = []
        if context_paragraph_limit > 0:
            # not set by user, use default
            self.context_paragraph_limit = context_paragraph_limit
        else:
            # set by user, use user's value
            self.context_paragraph_limit = CHATGPT_CONFIG["context_paragraph_limit"]
        self.batch_text_list = []
        self.batch_info_cache = None
        self.result_content_cache = {}
        self.system_role = system_role or 'system'
        # Initialize token tracking attributes
        self.token_info = {
            "system_tokens": 0,
            "user_tokens": 0,
            "intermediate_tokens": 0,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
        # Track cumulative tokens across all API calls
        self.cumulative_token_info = {
            "system_tokens": 0,
            "user_tokens": 0,
            "intermediate_tokens": 0,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
        self.api_call_count = 0

    def rotate_key(self):
        self.openai_client.api_key = next(self.keys)

    def rotate_model(self):
        self.model = next(self.model_list)

    def create_messages(self, text, intermediate_messages=None):
        try:
            content = self.prompt_template.format(
                text=text, language=self.language, crlf="\n"
            )
        except (KeyError, IndexError, ValueError) as e:
            print("\n" + "="*80)
            print("ERROR: Failed to format your prompt template")
            print("="*80)
            print(f"Details: {e}")
            print("\nThis error occurs when your prompt file contains unescaped curly braces {}")
            print("that Python mistakenly treats as format placeholders.")
            print("\nPROBLEM DETECTED:")
            
            # Use regex to find the likely problematic patterns
            import re
            markdown_attrs = re.findall(r'\{[\w\s="\'\.]+\}', self.prompt_template)
            if markdown_attrs:
                print("\nFound these Markdown attribute blocks that need escaping:")
                for attr in markdown_attrs:
                    print(f"  ❌ {attr}")
                    # Show how to fix it
                    fixed = attr.replace("{", "{{").replace("}", "}}")
                    print(f"  ✅ {fixed}  (correct version)")
            
            print("\nHOW TO FIX:")
            print("1. Open your prompt file:", self.prompt_file)
            print("2. For any literal curly braces, double them: { → {{ and } → }}")
            print("3. For example, change {width=\"5in\"} to {{width=\"5in\"}}")
            print("\nAborting translation. Please fix your prompt file and try again.")
            raise ValueError("Prompt formatting error - see details above") from e
        
        # Format system content with text and language placeholders too
        try:
            sys_content = self.system_content or self.prompt_sys_msg
            # Format system content with the same parameters as user content
            sys_content = sys_content.format(text=text, language=self.language, crlf="\n")
        except (KeyError, IndexError, ValueError) as e:
            print("\n" + "="*80)
            print("ERROR: Failed to format your system/developer message template")
            print("="*80)
            print(f"Details: {e}")
            print("\nThis error occurs when your system/developer message contains unescaped curly braces {}")
            print("or invalid placeholders.")
            print("\nAborting translation. Please fix your prompt file and try again.")
            raise ValueError("System prompt formatting error") from e
        
        # Use the stored role type from the PromptDown file
        role = getattr(self, 'system_role', 'system')  # Default to 'system' if not specified
        
        # Create individual messages first
        system_message = {"role": role, "content": sys_content}
        user_message = {"role": "user", "content": content}
        
        # Count tokens for each message separately
        model_name = getattr(self, 'model', None)  # Get model if available, otherwise None for default counting
        system_tokens = count_tokens_with_tiktoken([system_message], model=model_name)
        user_tokens = count_tokens_with_tiktoken([user_message], model=model_name)
        
        # Store token counts on self for later access
        self.message_token_info = {
            "system_tokens": system_tokens,
            "user_tokens": user_tokens,
            "intermediate_tokens": 0  # Will be updated if intermediate messages exist
        }
        
        # Build the full messages list
        messages = [system_message]

        if intermediate_messages:
            # Count tokens for intermediate messages if present
            intermediate_tokens = count_tokens_with_tiktoken(intermediate_messages, model=model_name)
            self.message_token_info["intermediate_tokens"] = intermediate_tokens
            messages.extend(intermediate_messages)

        messages.append(user_message)
        
        # Print message structure with clear representation of newlines
        print("\n[bold blue]Messages to API:[/bold blue]")
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            
            # Count total lines in original content
            total_lines = len(content.splitlines())
            
            # Truncate content if too long
            if len(content) > 500:
                truncated_content = content[:500] + "..."
                # Count lines in truncated content
                truncated_lines = len(truncated_content.splitlines())
                # Calculate number of truncated lines
                lines_truncated = total_lines - truncated_lines
                print(f"[bold cyan]{role}:[/bold cyan]")
                # Split by newlines to print each line separately
                for line in truncated_content.splitlines():
                    print(f"  {line}")
                print(f"[dim italic](+ {lines_truncated} more lines truncated)[/dim italic]")
            else:
                print(f"[bold cyan]{role}:[/bold cyan]")
                # Split by newlines to print each line separately
                for line in content.splitlines():
                    print(f"  {line}")
        
        print("[bold blue]End of messages[/bold blue]\n")
        
        return messages

    def create_context_messages(self):
        messages = []
        if self.context_flag:
            messages.append({"role": "user", "content": "\n".join(self.context_list)})
            messages.append(
                {
                    "role": "assistant",
                    "content": "\n".join(self.context_translated_list),
                }
            )
        return messages

    def create_chat_completion(self, text):
        # for issue #350
        if hasattr(self.openai_client, "api_key"):
            self.openai_client.api_key = next(self.keys)
        max_retries = 5
        retry_count = 0
        self.model = next(self.model_list)
        
        # Create messages outside the retry loop to avoid recreating them each time
        messages = self.create_messages(text)
        
        # Token counts were already calculated in create_messages
        total_token_count = sum(self.message_token_info.values())
        
        # Store token count information for logging
        self.token_info = {
            "estimated_prompt_tokens": total_token_count,
            "system_tokens": self.message_token_info["system_tokens"],
            "user_tokens": self.message_token_info["user_tokens"],
            "intermediate_tokens": self.message_token_info["intermediate_tokens"],
            "model": self.model,
            "temperature": self.temperature
        }
        
        # Log token usage information
        print(f"\n[bold blue]API Request Information:[/bold blue]")
        print(f"[cyan]Model:[/cyan] {self.model}")
        print(f"[cyan]System message tokens:[/cyan] {self.token_info['system_tokens']} tokens")
        print(f"[cyan]User message tokens:[/cyan] {self.token_info['user_tokens']} tokens")
        if self.token_info['intermediate_tokens'] > 0:
            print(f"[cyan]Intermediate message tokens:[/cyan] {self.token_info['intermediate_tokens']} tokens")
        print(f"[cyan]Total token count:[/cyan] {total_token_count} tokens")
        print(f"[cyan]Temperature:[/cyan] {self.temperature}")
        
        # Add cumulative statistics
        print(f"\n[bold green]Cumulative Stats (API Call #{self.api_call_count}):[/bold green]")
        print(f"[green]Total prompt tokens:[/green] {self.cumulative_token_info['prompt_tokens']} tokens")
        print(f"[green]Total completion tokens:[/green] {self.cumulative_token_info['completion_tokens']} tokens")
        print(f"[green]Total tokens used:[/green] {self.cumulative_token_info['total_tokens']} tokens")
        print(f"[green]Total estimated cost so far for batch:[/green] ${self.cumulative_token_info.get('cost', 0):.6f}")
        
        print("[bold blue]End of request information[/bold blue]\n")

        while retry_count < max_retries:
            try:
                completion = self.openai_client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                )
                # Increment API call counter
                self.api_call_count += 1
                
                # Store actual token usage information from the API response
                self.token_info.update({
                    "prompt_tokens": completion.usage.prompt_tokens,
                    "completion_tokens": completion.usage.completion_tokens, 
                    "total_tokens": completion.usage.total_tokens
                })
                
                # Calculate cost based on model and token usage
                cost = self._calculate_cost(completion.model, completion.usage.prompt_tokens, completion.usage.completion_tokens)
                self.token_info["cost"] = cost
                
                # Update cumulative token information
                self.cumulative_token_info["system_tokens"] += self.message_token_info["system_tokens"]
                self.cumulative_token_info["user_tokens"] += self.message_token_info["user_tokens"]
                self.cumulative_token_info["intermediate_tokens"] += self.message_token_info["intermediate_tokens"]
                self.cumulative_token_info["prompt_tokens"] += completion.usage.prompt_tokens
                self.cumulative_token_info["completion_tokens"] += completion.usage.completion_tokens
                self.cumulative_token_info["total_tokens"] += completion.usage.total_tokens
                self.cumulative_token_info["cost"] = self.cumulative_token_info.get("cost", 0) + cost
                
                # Log completion information
                print(f"\n[bold green]API Response Information:[/bold green]")
                print(f"[green]Prompt tokens:[/green] {completion.usage.prompt_tokens}")
                print(f"[green]Completion tokens:[/green] {completion.usage.completion_tokens}")
                print(f"[green]Total tokens:[/green] {completion.usage.total_tokens}")
                print(f"[green]Estimated cost:[/green] ${cost:.6f}")
                print("[bold green]End of response information[/bold green]\n")
                
                return completion
            except RateLimitError:
                # Rotate API key and model on rate limit
                if hasattr(self.openai_client, "api_key"):
                    self.openai_client.api_key = next(self.keys)
                self.model = next(self.model_list)
                retry_count += 1
                if retry_count >= max_retries:
                    raise Exception("Rate limit exceeded too many times.")
                time.sleep(3 * retry_count)  # Exponential backoff
            except Exception as e:
                print(f"Error: {e}")
                retry_count += 1
                if retry_count >= max_retries:
                    raise
                time.sleep(1)

    def get_translation(self, text):
        self.rotate_key()
        self.rotate_model()  # rotate all the model to avoid the limit

        completion = self.create_chat_completion(text)

        # TODO work well or exception finish by length limit
        # Check if content is not None before encoding
        if completion.choices[0].message.content is not None:
            t_text = completion.choices[0].message.content.encode("utf8").decode() or ""
        else:
            t_text = ""

        if self.context_flag:
            self.save_context(text, t_text)

        return t_text

    def save_context(self, text, t_text):
        if self.context_paragraph_limit > 0:
            self.context_list.append(text)
            self.context_translated_list.append(t_text)
            # Remove the oldest context
            if len(self.context_list) > self.context_paragraph_limit:
                self.context_list.pop(0)
                self.context_translated_list.pop(0)

    def translate(self, text, needprint=True):
        start_time = time.time()
        # Better formatted input text display
        if needprint:
            max_length = 1000  # maximum number of characters to display
            truncated_text = text if len(text) <= max_length else text[:max_length] + "..."
            clean_text = re.sub("\n{3,}", "\n\n", truncated_text)
            print("\n[bold magenta]Input Text:[/bold magenta]")
            print(clean_text)
            if len(text) > max_length:
                print(f"[dim italic](+ {len(text) - max_length} more characters truncated)[/dim italic]")

        attempt_count = 0
        max_attempts = 3
        t_text = ""

        while attempt_count < max_attempts:
            try:
                t_text = self.get_translation(text)
                break
            except RateLimitError as e:
                # todo: better sleep time? why sleep alawys about key_len
                # 1. openai server error or own network interruption, sleep for a fixed time
                # 2. an apikey has no money or reach limit, don`t sleep, just replace it with another apikey
                # 3. all apikey reach limit, then use current sleep
                sleep_time = int(60 / self.key_len)
                print(e, f"will sleep {sleep_time} seconds")
                time.sleep(sleep_time)
                attempt_count += 1
                if attempt_count == max_attempts:
                    print(f"Get {attempt_count} consecutive exceptions")
                    raise
            except Exception as e:
                print(str(e))
                return

        # todo: Determine whether to print according to the cli option
        if needprint:
            print("[bold green]" + re.sub("\n{3,}", "\n\n", t_text) + "[/bold green]")

        time.time() - start_time
        # print(f"translation time: {elapsed_time:.1f}s")

        return t_text

    def translate_and_split_lines(self, text):
        result_str = self.translate(text, False)
        lines = result_str.splitlines()
        lines = [line.strip() for line in lines if line.strip() != ""]
        return lines

    def get_best_result_list(
        self,
        plist_len,
        new_str,
        sleep_dur,
        result_list,
        max_retries=15,
    ):
        if len(result_list) == plist_len:
            return result_list, 0

        best_result_list = result_list
        retry_count = 0

        while retry_count < max_retries and len(result_list) != plist_len:
            print(
                f"bug: {plist_len} -> {len(result_list)} : Number of paragraphs before and after translation",
            )
            print(f"sleep for {sleep_dur}s and retry {retry_count+1} ...")
            time.sleep(sleep_dur)
            retry_count += 1
            result_list = self.translate_and_split_lines(new_str)
            if (
                len(result_list) == plist_len
                or len(best_result_list) < len(result_list) <= plist_len
                or (
                    len(result_list) < len(best_result_list)
                    and len(best_result_list) > plist_len
                )
            ):
                best_result_list = result_list

        return best_result_list, retry_count

    def log_retry(self, state, retry_count, elapsed_time, log_path="log/buglog.txt"):
        if retry_count == 0:
            return
        print(f"retry {state}")
        with open(log_path, "a", encoding="utf-8") as f:
            print(
                f"retry {state}, count = {retry_count}, time = {elapsed_time:.1f}s",
                file=f,
            )

    def log_translation_mismatch(
        self,
        plist_len,
        result_list,
        new_str,
        sep,
        log_path="log/buglog.txt",
    ):
        if len(result_list) == plist_len:
            return
        newlist = new_str.split(sep)
        with open(log_path, "a", encoding="utf-8") as f:
            print(f"problem size: {plist_len - len(result_list)}", file=f)
            for i in range(len(newlist)):
                print(newlist[i], file=f)
                print(file=f)
                if i < len(result_list):
                    print("............................................", file=f)
                    print(result_list[i], file=f)
                    print(file=f)
                print("=============================", file=f)

        print(
            f"bug: {plist_len} paragraphs of text translated into {len(result_list)} paragraphs",
        )
        print("continue")

    def join_lines(self, text):
        lines = text.splitlines()
        new_lines = []
        temp_line = []

        # join
        for line in lines:
            if line.strip():
                temp_line.append(line.strip())
            else:
                if temp_line:
                    new_lines.append(" ".join(temp_line))
                    temp_line = []
                new_lines.append(line)

        if temp_line:
            new_lines.append(" ".join(temp_line))

        text = "\n".join(new_lines)
        # try to fix #372
        if not text:
            return ""

        # del ^M
        text = text.replace("^M", "\r")
        lines = text.splitlines()
        filtered_lines = [line for line in lines if line.strip() != "\r"]
        new_text = "\n".join(filtered_lines)

        return new_text

    def translate_list(self, plist):
        sep = "\n\n\n\n\n"
        # new_str = sep.join([item.text for item in plist])

        new_str = ""
        i = 1
        for p in plist:
            temp_p = copy(p)
            for sup in temp_p.find_all("sup"):
                sup.extract()
            new_str += f"({i}) {temp_p.get_text().strip()}{sep}"
            i = i + 1

        if new_str.endswith(sep):
            new_str = new_str[: -len(sep)]

        new_str = self.join_lines(new_str)

        plist_len = len(plist)

        print(f"plist len = {len(plist)}")

        result_list = self.translate_and_split_lines(new_str)

        start_time = time.time()

        result_list, retry_count = self.get_best_result_list(
            plist_len,
            new_str,
            6,  # WTF this magic number here?
            result_list,
        )

        end_time = time.time()

        state = "fail" if len(result_list) != plist_len else "success"
        log_path = "log/buglog.txt"

        self.log_retry(state, retry_count, end_time - start_time, log_path)
        self.log_translation_mismatch(plist_len, result_list, new_str, sep, log_path)

        # del (num), num. sometime (num) will translated to num.
        result_list = [re.sub(r"^(\(\d+\)|\d+\.|(\d+))\s*", "", s) for s in result_list]
        return result_list

    def set_deployment_id(self, deployment_id):
        self.deployment_id = deployment_id
        self.openai_client = AzureOpenAI(
            api_key=next(self.keys),
            azure_endpoint=self.api_base,
            api_version="2023-07-01-preview",
            azure_deployment=self.deployment_id,
        )

    def set_gpt35_models(self, ollama_model=""):
        if ollama_model:
            self.model_list = cycle([ollama_model])
            return
        # gpt3 all models for save the limit
        if self.deployment_id:
            self.model_list = cycle(["gpt-35-turbo"])
        else:
            my_model_list = [
                i["id"] for i in self.openai_client.models.list().model_dump()["data"]
            ]
            model_list = list(set(my_model_list) & set(GPT35_MODEL_LIST))
            print(f"Using model list {model_list}")
            self.model_list = cycle(model_list)

    def set_gpt4_models(self):
        # for issue #375 azure can not use model list
        if self.deployment_id:
            self.model_list = cycle(["gpt-4"])
        else:
            my_model_list = [
                i["id"] for i in self.openai_client.models.list().model_dump()["data"]
            ]
            model_list = list(set(my_model_list) & set(GPT4_MODEL_LIST))
            print(f"Using model list {model_list}")
            self.model_list = cycle(model_list)

    def set_gpt4omini_models(self):
        # for issue #375 azure can not use model list
        if self.deployment_id:
            self.model_list = cycle(["gpt-4o-mini"])
        else:
            my_model_list = [
                i["id"] for i in self.openai_client.models.list().model_dump()["data"]
            ]
            model_list = list(set(my_model_list) & set(GPT4oMINI_MODEL_LIST))
            print(f"Using model list {model_list}")
            self.model_list = cycle(model_list)

    def set_gpt4o_models(self):
        # for issue #375 azure can not use model list
        if self.deployment_id:
            self.model_list = cycle(["gpt-4o"])
        else:
            my_model_list = [
                i["id"] for i in self.openai_client.models.list().model_dump()["data"]
            ]
            model_list = list(set(my_model_list) & set(GPT4o_MODEL_LIST))
            print(f"Using model list {model_list}")
            self.model_list = cycle(model_list)

    def set_model_list(self, model_list):
        model_list = list(set(model_list))
        print(f"Using model list {model_list}")
        self.model_list = cycle(model_list)

    def batch_init(self, book_name):
        self.book_name = self.sanitize_book_name(book_name)

    def add_to_batch_translate_queue(self, book_index, text):
        self.batch_text_list.append({"book_index": book_index, "text": text})

    def sanitize_book_name(self, book_name):
        # Replace any characters that are not alphanumeric, underscore, hyphen, or dot with an underscore
        sanitized_book_name = re.sub(r"[^\w\-_\.]", "_", book_name)
        # Remove leading and trailing underscores and dots
        sanitized_book_name = sanitized_book_name.strip("._")
        return sanitized_book_name

    def batch_metadata_file_path(self):
        return os.path.join(os.getcwd(), "batch_files", f"{self.book_name}_info.json")

    def batch_dir(self):
        return os.path.join(os.getcwd(), "batch_files", self.book_name)

    def custom_id(self, book_index):
        return f"{self.book_name}-{book_index}"

    def is_completed_batch(self):
        batch_metadata_file_path = self.batch_metadata_file_path()

        if not os.path.exists(batch_metadata_file_path):
            print("Batch result file does not exist")
            raise Exception("Batch result file does not exist")

        with open(batch_metadata_file_path, "r", encoding="utf-8") as f:
            batch_info = json.load(f)

        for batch_file in batch_info["batch_files"]:
            batch_status = self.check_batch_status(batch_file["batch_id"])
            if batch_status.status != "completed":
                return False

        return True

    def batch_translate(self, book_index):
        if self.batch_info_cache is None:
            batch_metadata_file_path = self.batch_metadata_file_path()
            with open(batch_metadata_file_path, "r", encoding="utf-8") as f:
                self.batch_info_cache = json.load(f)

        batch_info = self.batch_info_cache
        target_batch = None
        for batch in batch_info["batch_files"]:
            if batch["start_index"] <= book_index < batch["end_index"]:
                target_batch = batch
                break

        if not target_batch:
            raise ValueError(f"No batch found for book_index {book_index}")

        if target_batch["batch_id"] in self.result_content_cache:
            result_content = self.result_content_cache[target_batch["batch_id"]]
        else:
            batch_status = self.check_batch_status(target_batch["batch_id"])
            if batch_status.output_file_id is None:
                raise ValueError(f"Batch {target_batch['batch_id']} is not completed")
            result_content = self.get_batch_result(batch_status.output_file_id)
            self.result_content_cache[target_batch["batch_id"]] = result_content

        result_lines = result_content.text.split("\n")
        custom_id = self.custom_id(book_index)
        for line in result_lines:
            if line.strip():
                result = json.loads(line)
                if result["custom_id"] == custom_id:
                    return result["response"]["body"]["choices"][0]["message"][
                        "content"
                    ]

        raise ValueError(f"No result found for custom_id {custom_id}")

    def create_batch_context_messages(self, index):
        messages = []
        if self.context_flag:
            if index % CHATGPT_CONFIG[
                "batch_context_update_interval"
            ] == 0 or not hasattr(self, "cached_context_messages"):
                context_messages = []
                for i in range(index - 1, -1, -1):
                    item = self.batch_text_list[i]
                    if len(item["text"].split()) >= 100:
                        context_messages.append(item["text"])
                        if len(context_messages) == self.context_paragraph_limit:
                            break

                if len(context_messages) == self.context_paragraph_limit:
                    print("Creating cached context messages")
                    self.cached_context_messages = [
                        {"role": "user", "content": "\n".join(context_messages)},
                        {
                            "role": "assistant",
                            "content": self.get_translation(
                                "\n".join(context_messages)
                            ),
                        },
                    ]

            if hasattr(self, "cached_context_messages"):
                messages.extend(self.cached_context_messages)

        return messages

    def make_batch_request(self, book_index, text):
        messages = self.create_messages(
            text, self.create_batch_context_messages(book_index)
        )
        return {
            "custom_id": self.custom_id(book_index),
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                # model shuould not be rotate
                "model": self.batch_model,
                "messages": messages,
                "temperature": self.temperature,
            },
        }

    def create_batch_files(self, dest_file_path):
        file_paths = []
        # max request 50,000 and max size 100MB
        lines_per_file = 40000
        current_file = 0

        for i in range(0, len(self.batch_text_list), lines_per_file):
            current_file += 1
            file_path = os.path.join(dest_file_path, f"{current_file}.jsonl")
            start_index = i
            end_index = i + lines_per_file

            # TODO: Split the file if it exceeds 100MB
            with open(file_path, "w", encoding="utf-8") as f:
                for text in self.batch_text_list[i : i + lines_per_file]:
                    batch_req = self.make_batch_request(
                        text["book_index"], text["text"]
                    )
                    json.dump(batch_req, f, ensure_ascii=False)
                    f.write("\n")
            file_paths.append(
                {
                    "file_path": file_path,
                    "start_index": start_index,
                    "end_index": end_index,
                }
            )

        return file_paths

    def batch(self):
        self.rotate_model()
        self.batch_model = self.model
        # current working directory
        batch_dir = self.batch_dir()
        batch_metadata_file_path = self.batch_metadata_file_path()
        # cleanup batch dir and result file
        if os.path.exists(batch_dir):
            shutil.rmtree(batch_dir)
        if os.path.exists(batch_metadata_file_path):
            os.remove(batch_metadata_file_path)
        os.makedirs(batch_dir, exist_ok=True)
        # batch execute
        batch_files = self.create_batch_files(batch_dir)
        batch_info = []
        for batch_file in batch_files:
            file_id = self.upload_batch_file(batch_file["file_path"])
            batch = self.batch_execute(file_id)
            batch_info.append(
                self.create_batch_info(
                    file_id, batch, batch_file["start_index"], batch_file["end_index"]
                )
            )
        # save batch info
        batch_info_json = {
            "book_id": self.book_name,
            "batch_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "batch_files": batch_info,
        }
        with open(batch_metadata_file_path, "w", encoding="utf-8") as f:
            json.dump(batch_info_json, f, ensure_ascii=False, indent=2)

    def create_batch_info(self, file_id, batch, start_index, end_index):
        return {
            "input_file_id": file_id,
            "batch_id": batch.id,
            "start_index": start_index,
            "end_index": end_index,
            "prefix": self.book_name,
        }

    def upload_batch_file(self, file_path):
        batch_input_file = self.openai_client.files.create(
            file=open(file_path, "rb"), purpose="batch"
        )
        return batch_input_file.id

    def batch_execute(self, file_id):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        res = self.openai_client.batches.create(
            input_file_id=file_id,
            endpoint="/v1/chat/completions",
            completion_window="24h",
            metadata={
                "description": f"Batch job for {self.book_name} at {current_time}"
            },
        )
        if res.errors:
            print(res.errors)
            raise Exception(f"Batch execution failed: {res.errors}")
        return res

    def check_batch_status(self, batch_id):
        return self.openai_client.batches.retrieve(batch_id)

    def get_batch_result(self, output_file_id):
        return self.openai_client.files.content(output_file_id)

    def _calculate_cost(self, model, prompt_tokens, completion_tokens):
        """Calculate the cost of the API call based on model and token usage."""
        # Pricing per million tokens (USD)
        pricing = {
            # GPT-4.5
            "gpt-4.5-preview": {"input": 75.0, "output": 150.0},
            "gpt-4.5-preview-2025-02-27": {"input": 75.0, "output": 150.0},
            
            # GPT-4o
            "gpt-4o": {"input": 2.5, "output": 10.0},
            "gpt-4o-2024-08-06": {"input": 2.5, "output": 10.0},
            "gpt-4o-audio-preview": {"input": 2.5, "output": 10.0},
            "gpt-4o-audio-preview-2024-12-17": {"input": 2.5, "output": 10.0},
            "gpt-4o-realtime-preview": {"input": 5.0, "output": 20.0},
            "gpt-4o-realtime-preview-2024-12-17": {"input": 5.0, "output": 20.0},
            
            # GPT-4o Mini
            "gpt-4o-mini": {"input": 0.15, "output": 0.60},
            "gpt-4o-mini-2024-07-18": {"input": 0.15, "output": 0.60},
            "gpt-4o-mini-audio-preview": {"input": 0.15, "output": 0.60},
            "gpt-4o-mini-audio-preview-2024-12-17": {"input": 0.15, "output": 0.60},
            "gpt-4o-mini-realtime-preview": {"input": 0.60, "output": 2.40},
            "gpt-4o-mini-realtime-preview-2024-12-17": {"input": 0.60, "output": 2.40},
            
            # O1
            "o1": {"input": 15.0, "output": 60.0},
            "o1-2024-12-17": {"input": 15.0, "output": 60.0},
            
            # O3 Mini & O1 Mini
            "o3-mini": {"input": 1.10, "output": 4.40},
            "o3-mini-2025-01-31": {"input": 1.10, "output": 4.40},
            "o1-mini": {"input": 1.10, "output": 4.40},
            "o1-mini-2024-09-12": {"input": 1.10, "output": 4.40},
            
            # Default fallback to GPT-3.5 Turbo pricing
            "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
        }
        
        # Extract model name without version suffix if not found directly
        if model not in pricing:
            base_model = model.split('-2')[0] if '-2' in model else model
            if base_model not in pricing:
                print(f"[yellow]Warning: Unknown model {model}, using gpt-3.5-turbo pricing[/yellow]")
                model = "gpt-3.5-turbo"
            else:
                model = base_model
        
        # Calculate cost - prices are per million tokens
        input_cost = (prompt_tokens / 1_000_000) * pricing[model]["input"]
        output_cost = (completion_tokens / 1_000_000) * pricing[model]["output"]
        total_cost = input_cost + output_cost
        
        return total_cost
