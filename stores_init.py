from langchain_postgres import PGEngine
from consts import VECTOR_URI


# Determine if I want all the tables to be overwritten
OVERWRITE_TABLE = True

engine = PGEngine.from_connection_string(url=VECTOR_URI)

# Initialize the tables
engine.init_vectorstore_table(
    table_name="documents",
    vector_size=4096,
    overwrite_existing=OVERWRITE_TABLE
)
