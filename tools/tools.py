from langchain.tools import tool
from stores import document_store
from utils import logger


@tool
def retrieve_document_data(query: str) -> str:
    """
    Retrieves information from the document embedded

    Parameters:
    - query (str): Query used to retrieve relevant documents.

    Returns:
    - str: The relevant documents serialized.
    """
    logger.debug(f"Retrieving document data for query: {query}")

    docs = document_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in docs
    )

    logger.debug(f"Retrieved documents: {serialized}")

    return serialized
