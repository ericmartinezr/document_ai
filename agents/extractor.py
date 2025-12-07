from langchain.agents import create_agent
from langchain.agents.structured_output import ProviderStrategy
from models import small_model
from prompts import EXTRACTOR_AGENT_SYSTEM_PROMPT
from schemas import DocumentData
from tools.tools import retrieve_document_data

extractor_agent = create_agent(
    small_model,
    tools=[retrieve_document_data],
    system_prompt=EXTRACTOR_AGENT_SYSTEM_PROMPT,
    response_format=ProviderStrategy(DocumentData)
)
