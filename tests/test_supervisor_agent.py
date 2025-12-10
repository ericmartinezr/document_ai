import pytest
from langsmith import testing as t
from agents.supervisor import supervisor_agent


@pytest.mark.langsmith
@pytest.mark.parametrize("query", ["Hello!"])
def test_no_tools_on_offtopic_query(query: str) -> None:
    """Test that the agent does not use tools on offtopic queries."""
    # Log the test example
    t.log_inputs({"query": query})
    expected = []
    t.log_reference_outputs({"tool_calls": expected})
    # Call the agent's model node directly instead of running the ReACT loop.
    result = supervisor_agent.invoke(
        {"messages": [{"role": "user", "content": query}]}
    )
    # The example in LangChain's website shows
    # actual = result["messages"][0].tool_calls
    # But that fails with HumanMessage doesn't have a tool_calls attribute.
    result_tool_calls = result.get("tool_calls", [])
    t.log_outputs({"tool_calls": result_tool_calls})
    # Check that no tool calls were made.
    assert result_tool_calls == expected


@pytest.mark.langsmith
@pytest.mark.parametrize("query", ["Who's the first author in Addernet's paper?"])
def test_extraction_tool(query: str) -> None:
    """Test that the agent uses the extraction tool on relevant queries."""
    # Log the test example
    t.log_inputs({"query": query})
    expected = "Hanting Chen"
    t.log_reference_outputs({"author": expected})
    # Call the agent's model node directly instead of running the ReACT loop.
    result = supervisor_agent.invoke(
        {"messages": [{"role": "user", "content": query}]}
    )

    # First message it's the human message therefore there's no tool clal
    # The second message is the tool call from the supervisor calling the extraction agent
    # The third message has the result from the extraction agent in 'content'

    supervisor_tool_name = result["messages"][1].tool_calls[0]["name"]
    actual = result["messages"][2].content.strip()

    t.log_outputs({"author": actual})
    assert supervisor_tool_name == "extract_information"
    assert expected in actual
