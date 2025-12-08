from langchain.tools import tool
from schemas import DocumentData
from agents.extractor import extractor_agent
from agents.writer import writer_agent
from utils import logger


@tool
def extract_information(request: str):
    """
    Extracts information from the document store based on the provided natural language query.

    Use this when the user asks for specific information from the documents.

    Input: natural language request asking to extract information from the documents 
    (e.g., "Extract the titles of all documents", "Get me the authors and publication dates", etc.)
    """
    logger.info("=" * 60)
    logger.info("extract_information")
    logger.info("=" * 60)

    result = extractor_agent.invoke(
        {"messages": [{"role": "user", "content": request}]})

    logger.info("=" * 60)
    logger.info("end extract_information")
    logger.info("=" * 60)

    return result["messages"][-1].content


@tool
def write_to_file(data: DocumentData):
    """
    Writes the information in DocumentData format to a CSV file.

    Use this when the user asks for the information to be saved.

    Input: Data in DocumentData format to be written to a CSV file
    (e.g., "{'title': 'Document 1', 'author': 'Author A', 'publication_date': '2023-01-01', 'summary': '...'}")
    """
    logger.info("=" * 60)
    logger.info("write_to_file")
    logger.info("=" * 60)

    result = writer_agent.invoke(
        {"messages": [{"role": "user", "content": data}]})

    logger.info("=" * 60)
    logger.info("end write_to_file")
    logger.info("=" * 60)

    return result["messages"][-1].content


@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Agent that sends an email with the detail of the information extracted"""
    return ""
