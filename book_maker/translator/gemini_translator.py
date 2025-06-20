import re
import time
from os import environ
from itertools import cycle

import google.generativeai as genai
from google.generativeai.types.generation_types import (
    StopCandidateException,
    BlockedPromptException,
)
from rich import print

from .base_translator import Base

generation_config = {
    "temperature": 1.0,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 8192,
}

safety_settings = {
    "HATE": "BLOCK_NONE",
    "HARASSMENT": "BLOCK_NONE",
    "SEXUAL": "BLOCK_NONE",
    "DANGEROUS": "BLOCK_NONE",
}

PROMPT_ENV_MAP = {
    "user": "BBM_GEMINIAPI_USER_MSG_TEMPLATE",
    "system": "BBM_GEMINIAPI_SYS_MSG",
}

# Gemini API pricing (per 1M tokens)
GEMINI_PRICING = {
    "gemini-1.5-pro": {
        "input": 1.25,  # $1.25 per 1M tokens for prompts <= 128k tokens
        "output": 5.00,  # $5.00 per 1M tokens for prompts <= 128k tokens
    },
    "gemini-1.5-flash": {
        "input": 0.075,  # $0.075 per 1M tokens for prompts <= 128k tokens
        "output": 0.30,  # $0.30 per 1M tokens for prompts <= 128k tokens
    },
    "gemini-2.5-pro-preview": {
        "input": 1.25,  # $1.25 per 1M tokens for prompts <= 200k tokens
        "output": 10.00,  # $10.00 per 1M tokens for prompts <= 200k tokens
    },
    "gemini-2.5-flash-preview": {
        "input": 0.15,  # $0.15 per 1M tokens
        "output": 0.60,  # $0.60 per 1M tokens (non-thinking)
    }
}

GEMINIPRO_MODEL_LIST = [
    "gemini-1.5-pro",
    "gemini-1.5-pro-latest",
    "gemini-1.5-pro-001",
    "gemini-1.5-pro-002",
]

GEMINIFLASH_MODEL_LIST = [
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-1.5-flash-001",
    "gemini-1.5-flash-002",
    "gemini-2.0-flash-exp",
]


class Gemini(Base):
    """
    Google gemini translator
    """

    DEFAULT_PROMPT = "Please help me to translate,`{text}` to {language}, please return only translated content not include the origin text"

    def __init__(
        self,
        key,
        language,
        prompt_template=None,
        prompt_sys_msg=None,
        context_flag=False,
        temperature=1.0,
        **kwargs,
    ) -> None:
        super().__init__(key, language)
        self.context_flag = context_flag
        self.prompt = (
            prompt_template
            or environ.get(PROMPT_ENV_MAP["user"])
            or self.DEFAULT_PROMPT
        )
        self.prompt_sys_msg = (
            prompt_sys_msg
            or environ.get(PROMPT_ENV_MAP["system"])
            or None  # Allow None, but not empty string
        )
        self.interval = 3
        genai.configure(api_key=next(self.keys))
        generation_config["temperature"] = temperature
        
        # Initialize token tracking
        self.log_info = {
            "input_uncached_tokens": 0,
            "input_system_tokens": 0,
            "input_user_tokens": 0,
            "input_intermediate_tokens": 0,
            "input_total_tokens": 0,
            "output_prompt_tokens": 0,
            "output_completion_tokens": 0,
            "output_total_tokens": 0,
            "cost": 0
        }
        
        # Track cumulative tokens across all API calls
        self.cumulative_log_info = {
            "input_uncached_tokens": 0,
            "input_system_tokens": 0,
            "input_user_tokens": 0,
            "input_intermediate_tokens": 0,
            "input_total_tokens": 0,
            "output_prompt_tokens": 0,
            "output_completion_tokens": 0,
            "output_total_tokens": 0,
            "cost": 0
        }
        self.api_call_count = 0
        self.context_list = []
        self.context_translated_list = []

    def calculate_cost(self, input_tokens, output_tokens, model_name, input_uncached_tokens=0):
        """Calculate cost based on token usage and model pricing."""
        # Get base model name without version suffix
        base_model = model_name.split("-")[0] + "-" + model_name.split("-")[1]
        
        # Get pricing for the model
        pricing = GEMINI_PRICING.get(base_model, GEMINI_PRICING["gemini-1.5-pro"])
        
        # Calculate cached vs uncached input tokens
        input_cached_tokens = input_tokens - input_uncached_tokens
        
        # Calculate costs (convert to per token pricing)
        # Cached tokens are charged at half the rate
        input_cost_cached = (input_cached_tokens / 1_000_000) * pricing["input"] / 2
        input_cost_uncached = (input_uncached_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        
        return input_cost_cached + input_cost_uncached + output_cost

    def create_convo(self):
        model = genai.GenerativeModel(
            model_name=self.model,
            generation_config=generation_config,
            safety_settings=safety_settings,
            system_instruction=self.prompt_sys_msg,
        )
        self.convo = model.start_chat()
        # print(model)  # Uncomment to debug and inspect the model details.

    def rotate_model(self):
        self.model = next(self.model_list)
        self.create_convo()
        print(f"Using model {self.model}")

    def rotate_key(self):
        genai.configure(api_key=next(self.keys))
        self.create_convo()

    def translate(self, text):
        delay = 1
        exponential_base = 2
        attempt_count = 0
        max_attempts = 7

        t_text = ""
        print(text)
        # same for caiyun translate src issue #279 gemini for #374
        text_list = text.splitlines()
        num = None
        if len(text_list) > 1:
            if text_list[0].isdigit():
                num = text_list[0]

        while attempt_count < max_attempts:
            try:
                # Count tokens for the input text
                input_tokens = self.convo.model.count_tokens(text).total_tokens
                system_tokens = self.convo.model.count_tokens(self.prompt_sys_msg).total_tokens if self.prompt_sys_msg else 0
                prompt_tokens = self.convo.model.count_tokens(self.prompt.format(text=text, language=self.language)).total_tokens
                total_input_tokens = system_tokens + prompt_tokens
                
                # Calculate uncached tokens (new content)
                input_uncached_tokens = input_tokens
                
                # Update log info
                self.log_info.update({
                    "input_uncached_tokens": input_uncached_tokens,
                    "input_system_tokens": system_tokens,
                    "input_user_tokens": prompt_tokens,
                    "input_total_tokens": total_input_tokens,
                })
                
                # Update cumulative log info
                self.cumulative_log_info.update({
                    "input_uncached_tokens": self.cumulative_log_info["input_uncached_tokens"] + input_uncached_tokens,
                    "input_system_tokens": self.cumulative_log_info["input_system_tokens"] + system_tokens,
                    "input_user_tokens": self.cumulative_log_info["input_user_tokens"] + prompt_tokens,
                    "input_total_tokens": self.cumulative_log_info["input_total_tokens"] + total_input_tokens,
                })
                
                # Send message and get response
                response = self.convo.send_message(
                    self.prompt.format(text=text, language=self.language)
                )
                t_text = "".join(part.text for part in response.parts).strip()
                
                # Count tokens for the response
                output_tokens = self.convo.model.count_tokens(t_text).total_tokens
                
                # Calculate cost for this translation
                cost = self.calculate_cost(total_input_tokens, output_tokens, self.model, input_uncached_tokens)
                
                # Update log info with output tokens and cost
                self.log_info.update({
                    "output_completion_tokens": output_tokens,
                    "output_total_tokens": output_tokens,
                    "cost": cost
                })
                
                # Update cumulative log info with output tokens and cost
                self.cumulative_log_info.update({
                    "output_completion_tokens": self.cumulative_log_info["output_completion_tokens"] + output_tokens,
                    "output_total_tokens": self.cumulative_log_info["output_total_tokens"] + output_tokens,
                    "cost": self.cumulative_log_info["cost"] + cost
                })
                
                # Increment API call count
                self.api_call_count += 1
                
                # 检查是否包含特定标签,如果有则只返回标签内的内容
                tag_pattern = (
                    r"<step3_refined_translation>(.*?)</step3_refined_translation>"
                )
                tag_match = re.search(tag_pattern, t_text, re.DOTALL)
                if tag_match:
                    print(
                        "[bold green]"
                        + re.sub("\n{3,}", "\n\n", t_text)
                        + "[/bold green]"
                    )
                    t_text = tag_match.group(1).strip()
                    # print("[bold green]" + re.sub("\n{3,}", "\n\n", t_text) + "[/bold green]")
                break
            except StopCandidateException as e:
                print(
                    f"Translation failed due to StopCandidateException: {e} Attempting to switch model..."
                )
                self.rotate_model()
            except BlockedPromptException as e:
                print(
                    f"Translation failed due to BlockedPromptException: {e} Attempting to switch model..."
                )
                self.rotate_model()
            except Exception as e:
                print(
                    f"Translation failed due to {type(e).__name__}: {e} Will sleep {delay} seconds"
                )
                time.sleep(delay)
                delay *= exponential_base

                self.rotate_key()
                if attempt_count >= 1:
                    self.rotate_model()

            attempt_count += 1

        if attempt_count == max_attempts:
            print(f"Translation failed after {max_attempts} attempts.")
            return

        if self.context_flag:
            if len(self.convo.history) > 10:
                self.convo.history = self.convo.history[2:]
        else:
            self.convo.history = []

        print("[bold green]" + re.sub("\n{3,}", "\n\n", t_text) + "[/bold green]")
        # for rate limit(RPM)
        time.sleep(self.interval)
        if num:
            t_text = str(num) + "\n" + t_text
        return t_text

    def set_interval(self, interval):
        self.interval = interval

    def set_geminipro_models(self):
        self.set_models(GEMINIPRO_MODEL_LIST)

    def set_geminiflash_models(self):
        self.set_models(GEMINIFLASH_MODEL_LIST)

    def set_models(self, allowed_models):
        available_models = [
            re.sub(r"^models/", "", i.name) for i in genai.list_models()
        ]
        model_list = sorted(
            list(set(available_models) & set(allowed_models)),
            key=allowed_models.index,
        )
        print(f"Using model list {model_list}")
        self.model_list = cycle(model_list)
        self.rotate_model()

    def set_model_list(self, model_list):
        # keep the order of input
        model_list = sorted(list(set(model_list)), key=model_list.index)
        print(f"Using model list {model_list}")
        self.model_list = cycle(model_list)
        self.rotate_model()
