from langchain.agents import create_agent
from langchain.messages import SystemMessage
from langchain.agents.structured_output import ToolStrategy
from models import small_model
from prompts import EXTRACTOR_AGENT_SYSTEM_PROMPT
from schemas import DocumentData
from tools.tools import retrieve_document_data
from consts import DEV

extractor_agent = create_agent(
    small_model,
    tools=[retrieve_document_data],
    system_prompt=SystemMessage(content=EXTRACTOR_AGENT_SYSTEM_PROMPT),
    # https://github.com/langchain-ai/langchain/issues/34144#issuecomment-3596071389
    response_format=ToolStrategy(DocumentData),
    debug=DEV
)
