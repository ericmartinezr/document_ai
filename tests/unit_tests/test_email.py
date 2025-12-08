import unittest
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage, ToolCall
from langchain_core.runnables import RunnableConfig


@tool
def send_email(to_email: str, from_email: str, subject: str, body: str, attachment_paths: list[str]) -> str:
    """Function to send emails"""
    return "Email sent successfully"


class TestEmailAgent(unittest.TestCase):

    def test_agent_with_tool_call(self):

        mock_responses = iter(
            [
                # Tell the agent to call the 'send_email' tool
                AIMessage(
                    content="",
                    tool_calls=[
                        # to_email: str, from_email: str,
                        # subject: str, body: str, attachment_paths: list[str]
                        ToolCall(
                            name="send_email",
                            args={
                                "to_email": "test@example.com",
                                "from_email": "sender@example.com",
                                "subject": "Test Subject",
                                "body": "This is a test email body.",
                                "attachment_paths": ["path/to/attachment1.pdf"]
                            },
                            id="call_send_email_1"
                        )
                    ]
                ),

                # Final response after tool call
                AIMessage(
                    content="Email sent successfully")
            ]
        )

        fake_llm = GenericFakeChatModel(messages=mock_responses)

        config: RunnableConfig = {}
        result = fake_llm.invoke("Send an email", config=config)

        print(result)
        self.assertEqual(result, "Email sent successfully")


if __name__ == "__main__":
    unittest.main()
