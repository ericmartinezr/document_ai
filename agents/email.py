import os
from langchain.agents import create_agent
from langchain.messages import SystemMessage
from models import small_model
from prompts import EMAIL_AGENT_SYSTEM_PROMPT
from tools.tools import send_email
from consts import DEV
from dotenv import load_dotenv

load_dotenv()


email_agent = create_agent(
    small_model,
    tools=[send_email],
    system_prompt=SystemMessage(content=EMAIL_AGENT_SYSTEM_PROMPT.format(
        to_email=os.getenv('TO_EMAIL'),
        from_email=os.getenv('FROM_EMAIL'))),
    debug=DEV
)
