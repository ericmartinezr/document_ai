from langchain.agents import create_agent
from langchain.messages import SystemMessage
from tools.tools import write_csv
from models import small_model
from prompts import WRITER_AGENT_SYSTEM_PROMPT
from consts import DEV

writer_agent = create_agent(
    small_model,
    tools=[write_csv],
    system_prompt=SystemMessage(content=WRITER_AGENT_SYSTEM_PROMPT),
    debug=DEV
)
