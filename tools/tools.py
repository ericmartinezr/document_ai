from langchain.tools import tool
from stores import document_store
from schemas import DocumentData


@tool
def retrieve_document_data(query: str):
    """Retrieves information from the document embedded"""
    docs = document_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in docs
    )
    return serialized, docs
