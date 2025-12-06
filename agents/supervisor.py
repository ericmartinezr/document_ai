from langchain.agents import create_agent
from models import small_model
from prompts import SUPERVISOR_SYSTEM_PROMPT


supervisor = create_agent(
    small_model,
    system_prompt=SUPERVISOR_SYSTEM_PROMPT
)
