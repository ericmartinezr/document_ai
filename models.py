from langchain_ollama import ChatOllama

# True for local execution
# False for execution in Ollama's cloud
LOCAL = False

GPT_OSS = "gpt-oss:20b"
GPT_OSS_20B = "gpt-oss:20b"
QWEN3_CODER = "qwen3-coder:30b"


if not LOCAL:
    GPT_OSS = "gpt-oss:120b-cloud"
    GPT_OSS_20B = "gpt-oss:20b-cloud"
    QWEN3_CODER = "qwen3-coder:480b-cloud"


small_model = ChatOllama(
    model=GPT_OSS,
    temperature=0.2,
    base_url="http://localhost:11434",
    validate_model_on_init=True,
)
