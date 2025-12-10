from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langchain_ollama import ChatOllama
from agentevals.trajectory.match import create_trajectory_match_evaluator
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()


class DocumentData(BaseModel):
    title: str = Field("The title of the document")
    author: str = Field("The author of the document")
    publish_date: str = Field("The year the document was published")
    summary: str = Field("A brief summary of the document")


SUPERVISOR_SYSTEM_PROMPT = """
You're an expert AI agentic system supervisor.
                                         
You can extract information from documents, write to CSV files, and send emails using the tools at your disposal.
                                         
**Instructions:**
- **DO NOT** use your internal knowledge to answer user queries.
- **DO NOT** attempt to answer user queries directly.
- Always delegate tasks to the appropriate specialized agents:
  1. **Extractor Agent**: For reading PDFs and extracting relevant information. 
    1.1. Returns a dictionary.
  2. **CSV Agent**: For writing data to CSV files. 
    2.1. Pass the extracted dictionary to this agent. 
    2.2. Returns a confirmation message with the filename.
  3. **Email Agent**: For sending emails via Gmail or another SMTP service.
    3.1. Pass the filename from the CSV Agent to this agent to send as an attachment.
- Always follow the sequence: Extractor Agent -> CSV Agent -> Email Agent.
- Always provide clear and concise instructions to each agent.
- After each action, confirm the completion and results before proceeding to the next step.
- Confirm that you followed the steps correctly after each action.

**Workflow:**
1. When a user query is received, analyze the request to determine what information is needed.
2. Use the Extractor Agent to retrieve the necessary information from the documents.
3. Once the information is extracted, use the CSV Agent to write the data to a CSV file.
4. If the user requests, use the Email Agent to send the CSV file or relevant information via email.
"""


@tool
def extract_information(request: str):
    """Extracts information from the document store based on the query provided."""
    return f"Extracted information based on the request: {request}."


@tool(args_schema=DocumentData)
def write_to_file(title: str, author: str, publish_date: str, summary: str):
    """Writes the information in DocumentData format to a CSV file."""
    return f"Written to file: {title}, {author}, {publish_date}, {summary}."


@tool
def email_to_user(recipient_email: str, subject: str, body: str, attachment_paths: list[str]):
    """Sends an email to the specified recipient."""
    return f"Email sent to {recipient_email} with subject '{subject}'."


small_model = ChatOllama(
    model="gpt-oss:20b",
    temperature=0.2,
    base_url="http://localhost:11434",
    validate_model_on_init=True,
)

supervisor_agent = create_agent(
    small_model,
    tools=[extract_information, write_to_file, email_to_user],
    system_prompt=SystemMessage(content=SUPERVISOR_SYSTEM_PROMPT)
)


evaluator = create_trajectory_match_evaluator(
    trajectory_match_mode="strict",
)


def test_supervisor_agent():
    # 1. Define the User Message (Input)
    user_message = HumanMessage(
        content="What's the year \"Attention is all your need\" was published?",
        # Including the ID for absolute match, though often optional
        id='de2c0910-c9d2-4e76-b4b3-45cbbb0dc6bd'
    )

    # 2. Invoke the agent to get the actual trace
    result = supervisor_agent.invoke({
        "messages": [user_message]
    })

    # 3. Define the Reference Trajectory
    # This must be an EXACT match (order, content, tool_calls structure)
    # of the full trace you provided.
    reference_trajectory = [
        # Message 1: User Input
        user_message,

        # Message 2: Model calls 'extract_information' tool (LC Run 1)
        AIMessage(
            content='',
            tool_calls=[{
                'name': 'extract_information',
                'args': {'request': 'What is the publication year of the paper titled "Attention Is All You Need"?'},
                'id': '5e84af48-4c83-48c1-abb6-b2253499ffb6',
                'type': 'tool_call'
            }]
            # NOTE: For simplicity and portability, we omit response_metadata/usage_metadata in the reference
            # but they must be included if the evaluator is STRICTLY checking ALL fields.
        ),

        # Message 3: Tool Response for 'extract_information'
        ToolMessage(
            content='Extracted information based on the request: What is the publication year of the paper titled "Attention Is All You Need"?.',
            name='extract_information',
            tool_call_id='5e84af48-4c83-48c1-abb6-b2253499ffb6'
        ),

        # Message 4: Model calls 'write_to_file' tool (LC Run 2)
        AIMessage(
            content='',
            tool_calls=[{
                'name': 'write_to_file',
                'args': {
                    'author': 'Ashish Vaswani et al.',
                    'publish_date': '2017',
                    'summary': 'Introduces the Transformer architecture, eliminating recurrence and using self-attention mechanisms.',
                    'title': 'Attention Is All You Need'
                },
                'id': '1210ced2-4652-425e-bfc1-dd9a2580a588',
                'type': 'tool_call'
            }]
        ),

        # Message 5: Tool Response for 'write_to_file'
        ToolMessage(
            content='Written to file: Attention Is All You Need, Ashish Vaswani et al., 2017, Introduces the Transformer architecture, eliminating recurrence and using self-attention mechanisms..',
            name='write_to_file',
            tool_call_id='1210ced2-4652-425e-bfc1-dd9a2580a588'
        ),

        # Message 6: Final Answer to User (LC Run 3)
        AIMessage(
            content='The paper **“Attention Is All You Need”** was published in **2017**.'
        )
    ]

    evaluation = evaluator(
        outputs=result["messages"],
        reference_outputs=reference_trajectory
    )

    print("***"*60)
    print("Evaluation:", evaluation)
    print("***"*60)

    assert evaluation["score"] is True
