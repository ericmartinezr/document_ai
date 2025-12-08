from langchain_ollama import ChatOllama

# True for local execution
# False for execution in Ollama's cloud
LOCAL = False

GPT_OSS = "gpt-oss:20b"
GPT_OSS_20B = "gpt-oss:20b"


if not LOCAL:
    GPT_OSS = "gpt-oss:120b-cloud"
    GPT_OSS_20B = "gpt-oss:20b-cloud"


small_model = ChatOllama(
    model=GPT_OSS,
    temperature=0.2,
    base_url="http://localhost:11434",
    validate_model_on_init=True,
)
