from langchain.tools import tool
from schemas import DocumentData
from agents.extractor import extractor_agent
from agents.writer import writer_agent
from agents.email import email_agent
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


@tool(args_schema=DocumentData)
def write_to_file(title: str, author: str, publish_date: str, summary: str):
    """
    Writes the information in DocumentData format to a CSV file.

    Use this when the user asks for the information to be saved.

    Parameters:
    - title (str): Title of the document.
    - author (str): Author of the document.
    - publish_date (str): Publication date of the document.
    - summary (str): Summary of the document.
    """
    logger.info("=" * 60)
    logger.info("write_to_file")
    logger.info("=" * 60)

    data = f"""
    Title: {title}
    Author: {author}
    Publish Date: {publish_date}
    Summary: {summary}
    """

    result = writer_agent.invoke(
        {"messages": [{"role": "user", "content": data}]})

    logger.info("=" * 60)
    logger.info("end write_to_file")
    logger.info("=" * 60)

    return result["messages"][-1].content


@tool
def email_to_user(title: str, author: str, publish_date: str, summary: str, attachment_files: list[str]) -> str:
    """
    Sends an email with the provided details.

    Use this when the user asks for the information to be emailed.

    Parameters:
    - title (str): Title of the document.
    - author (str): Author of the document.
    - publish_date (str): Publication date of the document.
    - summary (str): Summary of the document.
    - attachment_paths (list[str]): List of attachment files. (e.g., ["report.csv"])
    """
    logger.info("=" * 60)
    logger.info("send_email")
    logger.info("=" * 60)

    data = f"""
    Title: {title}
    Author: {author}
    Publish Date: {publish_date}
    Summary: {summary}
    Attachment files: {attachment_files if attachment_files else 'None'}
    """

    result = email_agent.invoke(
        {"messages": [{"role": "user", "content": data}]})

    logger.info("=" * 60)
    logger.info("end send_email")
    logger.info("=" * 60)

    return result["messages"][-1].content
