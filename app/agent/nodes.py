import logging

from langchain_ollama import ChatOllama
from langgraph.graph.state import END

from agent.state import AgentState

logger = logging.getLogger(__name__)


llm = ChatOllama(model="deepseek-r1:8b")


def chatbot_node(state: AgentState):
    state.messages = [llm.invoke(state.messages)]

    return state

def route_tools(
    state: AgentState,
):
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.messages:
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tool_node"
    return END