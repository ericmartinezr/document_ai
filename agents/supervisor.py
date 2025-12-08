from langchain.agents import create_agent
from langchain.messages import SystemMessage
from langchain.agents.middleware import SummarizationMiddleware
from models import small_model
from tools.agents_as_tools import extract_information, write_to_file, send_email
from prompts import SUPERVISOR_SYSTEM_PROMPT
from consts import DEV

supervisor_agent = create_agent(
    small_model,
    tools=[extract_information, write_to_file, send_email],
    # middleware=[
    #    SummarizationMiddleware(
    #        model=small_model,
    #        trigger=("tokens", 5000),
    #        keep=("messages", 10)
    #    )
    # ],
    system_prompt=SystemMessage(content=SUPERVISOR_SYSTEM_PROMPT),
    debug=DEV
)
