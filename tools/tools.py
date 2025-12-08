import os
import csv
from datetime import datetime
from langchain.tools import tool
from stores import document_store
from utils import logger
from consts import CSV_DIR


@tool
def retrieve_document_data(query: str) -> str:
    """
    Retrieves information from the document embedded

    Parameters:
    - query (str): Query used to retrieve relevant documents.

    Returns:
    - str: The relevant documents serialized.
    """
    logger.info("=" * 60)
    logger.info("retrieve_document_data")
    logger.info("=" * 60)
    logger.debug(f"Retrieving document data for query: {query}")

    docs = document_store.similarity_search(query, k=5)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in docs
    )

    logger.debug(f"Retrieved documents: {serialized}")
    logger.info("=" * 60)
    logger.info("end retrieve_document_data")
    logger.info("=" * 60)

    return serialized


@tool
def write_csv(title: str, author: str, publish_date: str, summary: str) -> str:
    """
    Writes the provided data to a CSV file.

    Parameters:
    - title (str): Title of the document.
    - author (str): Author of the document.
    - publish_date (str): Publication date of the document.
    - summary (str): Summary of the document.

    Returns:
    - str: Confirmation message.
    """
    logger.info("=" * 60)
    logger.info("write_csv")
    logger.info("=" * 60)

    try:
        file_name = f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        file_path = os.path.join(CSV_DIR, file_name)
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([title, author, publish_date, summary])

        confirmation_message = f"Data successfully written to {file_name}"
        logger.debug(confirmation_message)
    except Exception as e:
        error_message = f"Failed to write data to CSV: {e}"
        logger.error(error_message)
        logger.error(e, exc_info=True)
        confirmation_message = error_message

    logger.info("=" * 60)
    logger.info("end write_csv")
    logger.info("=" * 60)

    return confirmation_message
