from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGEngine, PGVectorStore, Column
from consts import VECTOR_URI

embeddings = OllamaEmbeddings(model="qwen3-embedding")

# Determine if I want all the tables to be overwritten
OVERWRITE_TABLE = True


engine = PGEngine.from_connection_string(url=VECTOR_URI)

# qwen3-embedding supports up to 4096 dimension

# Initialize the tables
engine.init_vectorstore_table(
    table_name="documents",
    vector_size=4096,
    overwrite_existing=OVERWRITE_TABLE
)


document_store = PGVectorStore.create_sync(
    engine=engine,
    table_name="documents",
    embedding_service=embeddings
)
