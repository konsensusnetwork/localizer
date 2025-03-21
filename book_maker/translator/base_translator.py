import itertools
from abc import ABC, abstractmethod


class Base(ABC):
    def __init__(self, key, language) -> None:
        self.keys = itertools.cycle(key.split(","))
        self.language = language
        self.api_call_count = 0
        self.prompt_file = None  # Store the original prompt file path/name

    @abstractmethod
    def rotate_key(self):
        pass

    @abstractmethod
    def translate(self, text):
        pass

    def set_deployment_id(self, deployment_id):
        pass
