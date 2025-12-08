from langchain_tests.unit_tests import ChatModelUnitTests
from langchain_ollama import ChatOllama
from typing import Type


class TestChat(ChatModelUnitTests):

    @property
    def chat_model_class(self) -> Type[ChatOllama]:
        return ChatOllama

    @property
    def chat_model_params(self) -> dict:
        return {
            "model": "gpt-oss:7b",
            "temperature": 0.7,
            "base_url": "http://localhost:11434",
            "validate_model_on_init": False,
        }
