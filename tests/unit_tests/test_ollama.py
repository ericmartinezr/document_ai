from langchain_ollama import ChatOllama


def test_initialize_ollama() -> None:
    llm = ChatOllama(
        model="gpt-oss:120b-cloud",
        temperature=0.2,
        base_url="http://localhost:11434",
        validate_model_on_init=True,
    )
    assert llm.model == "gpt-oss:120b-cloud"
    assert llm.temperature == 0.2
    assert llm.base_url == "http://localhost:11434"
    assert llm.validate_model_on_init is True


# pytest tests/unit_tests/
# https://github.com/langchain-ai/langchain/blob/master/libs/standard-tests/langchain_tests/unit_tests/chat_models.py
# https://reference.langchain.com/python/langchain_tests/
# https://docs.langchain.com/oss/python/langchain/test#strict-match
