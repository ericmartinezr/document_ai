import os
import csv
import smtplib
from schemas import DocumentData
from email.message import EmailMessage
from datetime import datetime
from langchain.tools import tool
from stores import document_store
from utils import logger
from consts import CSV_DIR
from dotenv import load_dotenv

load_dotenv()


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


@tool(args_schema=DocumentData)
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
        file_name = f"output_{datetime.now().strftime('%Y%m%d')}.csv"
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


@tool
def send_email(to_email: str, from_email: str, subject: str, body: str, attachment_paths: list[str]) -> str:
    """
    Sends an email with the provided details.

    Parameters:
    - to_email (str): Recipient email address.
    - from_email (str): Sender email address.
    - subject (str): Subject of the email.
    - body (str): Body content of the email.
    - attachment_paths (list[str]): List of paths to the attachment files.

    Returns:
    - str: Confirmation message.
    """
    logger.info("=" * 60)
    logger.info("send_email")
    logger.info("=" * 60)

    try:
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        port = int(os.getenv("SMTP_PORT", 587))
        password = os.getenv("GOOGLE_APP_PWD")

        # Create the EmailMessage object
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        # Set the main text content
        msg.set_content(body)

        # 2. Handle Attachments
        if attachment_paths:
            logger.debug(
                f"Preparing to attach {len(attachment_paths)} file(s)...")

            for file_path in attachment_paths:
                # Check if the file exists
                file_path = os.path.join(CSV_DIR, file_path)
                if not os.path.exists(file_path):
                    logger.error(
                        f"Warning: File not found at path: {file_path}. Skipping attachment.")
                    continue

                # Determine the main type and subtype based on the file extension
                import mimetypes
                ctype, encoding = mimetypes.guess_type(file_path)

                # Default to application/octet-stream if the type can't be guessed
                if ctype is None or encoding is not None:
                    ctype = 'application/octet-stream'

                maintype, subtype = ctype.split('/', 1)

                # Open the file in binary mode
                with open(file_path, 'rb') as fp:
                    # Attach the file
                    msg.add_attachment(fp.read(),
                                       maintype=maintype,
                                       subtype=subtype,
                                       filename=os.path.basename(file_path))

                logger.debug(f"Attached: {os.path.basename(file_path)}")

        # Connect and Send
        logger.debug(f"Connecting to {smtp_server}:{port}...")

        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()  # Secure the connection
            server.login(from_email, password)
            logger.debug("Successfully logged in.")

            server.send_message(msg)
            logger.debug("Email sent successfully!")

        confirmation_message = f"Email sent to {to_email} with subject '{subject}'"
        if attachment_paths:
            confirmation_message += f" and attachment '{attachment_paths}'"
        logger.debug(confirmation_message)
        return confirmation_message
    except smtplib.SMTPAuthenticationError as e:
        error_message = f"Failed to send email: {e}"
        logger.error("Error: Authentication failed. Check your credentials.")
        logger.error(e, exc_info=True)
        return error_message
    except Exception as e:
        error_message = f"Failed to send email: {e}"
        logger.error(error_message)
        logger.error(e, exc_info=True)
        return error_message
    finally:
        logger.info("=" * 60)
        logger.info("end send_email")
        logger.info("=" * 60)
