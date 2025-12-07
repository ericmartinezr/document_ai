from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from models import small_model
from tools.agents_as_tools import extractor_agent_tool
from prompts import SUPERVISOR_SYSTEM_PROMPT


supervisor_agent = create_agent(
    small_model,
    tools=[extractor_agent_tool],
    # middleware=[
    #    SummarizationMiddleware(
    #        model=small_model,
    #        trigger=("tokens", 5000),
    #        keep=("messages", 10)
    #    )
    # ],
    system_prompt=SUPERVISOR_SYSTEM_PROMPT
)
