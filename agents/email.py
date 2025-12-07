from langchain.agents import create_agent
from langchain.messages import SystemMessage
from models import small_model
from prompts import SUPERVISOR_SYSTEM_PROMPT


supervisor = create_agent(
    small_model,
    system_prompt=SystemMessage(content=SUPERVISOR_SYSTEM_PROMPT)
)
