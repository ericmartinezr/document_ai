from langchain.tools import tool
from schemas import DocumentData
from agents.extractor import extractor_agent


@tool
def extract_information(request: str):
    """
    Extracts information from the document store based on the provided natural language query.

    Use this when the user asks for specific information from the documents.

    Input: natural language request asking to extract information from the documents 
    (e.g., "Extract the titles of all documents", "Get me the authors and publication dates", etc.)
    """

    result = extractor_agent.invoke(
        {"messages": [{"role": "user", "content": request}]})
    return result["messages"][-1].content


@tool
def write_to_file(data: DocumentData):
    """Agent that writes the specified data to a csv file"""
    return ""


@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Agent that sends an email with the detail of the information extracted"""
    return ""
