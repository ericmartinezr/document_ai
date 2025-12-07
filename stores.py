from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGEngine, PGVectorStore, Column
from consts import VECTOR_URI

embeddings = OllamaEmbeddings(model="qwen3-embedding")

engine = PGEngine.from_connection_string(url=VECTOR_URI)

document_store = PGVectorStore.create_sync(
    engine=engine,
    table_name="documents",
    embedding_service=embeddings
)
