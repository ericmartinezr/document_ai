from langchain.tools import tool
from schemas import DocumentData
from agents.extractor import extractor_agent


@tool("extractor_agent", description="Extracts information from the document")
def extractor_agent_tool(query: str):
    """Agent that extracts information from the document attached"""

    result = extractor_agent.invoke(
        {"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content


@tool("writer_agent", description="Writes the extracted information to a file")
def writer_agent_tool(data: DocumentData):
    """Agent that writes the specified data to a csv file"""
    return ""


@tool("email_agent", description="Sends an email with the extracted information")
def email_agent_tool(to: str, subject: str, body: str) -> str:
    """Agent that sends an email with the detail of the information extracted"""
    return ""
