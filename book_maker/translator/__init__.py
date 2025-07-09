from book_maker.translator.chatgptapi_translator import ChatGPTAPI
from book_maker.translator.gemini_translator import Gemini

# Simplified MODEL_DICT with only OpenAI and Gemini providers
# Users must specify exact model names like "gpt-4", "gpt-3.5-turbo", "gemini-1.5-flash-002", etc.
MODEL_DICT = {
    # OpenAI models - all use ChatGPTAPI class
    "gpt-4": ChatGPTAPI,
    "gpt-4-turbo": ChatGPTAPI,
    "gpt-4-32k": ChatGPTAPI,
    "gpt-4-0613": ChatGPTAPI,
    "gpt-4-32k-0613": ChatGPTAPI,
    "gpt-4-1106-preview": ChatGPTAPI,
    "gpt-4-0125-preview": ChatGPTAPI,
    "gpt-3.5-turbo": ChatGPTAPI,
    "gpt-3.5-turbo-0125": ChatGPTAPI,
    "gpt-3.5-turbo-1106": ChatGPTAPI,
    "gpt-3.5-turbo-16k": ChatGPTAPI,
    "gpt-4o": ChatGPTAPI,
    "gpt-4o-mini": ChatGPTAPI,
    "o1-preview": ChatGPTAPI,
    "o1-mini": ChatGPTAPI,
    "o3-mini": ChatGPTAPI,
    
    # Gemini models - all use Gemini class
    "gemini-1.5-flash": Gemini,
    "gemini-1.5-flash-002": Gemini,
    "gemini-1.5-flash-8b": Gemini,
    "gemini-1.5-flash-8b-exp-0924": Gemini,
    "gemini-1.5-pro": Gemini,
    "gemini-1.5-pro-002": Gemini,
    "gemini-1.0-pro": Gemini,
}
