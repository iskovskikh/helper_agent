import logging

from langchain_ollama import ChatOllama
from langgraph.graph.state import END

from agent.state import AgentState

logger = logging.getLogger(__name__)

from colorama.ansi import Fore, Style

from agent.state import AgentState
from settings.config import config

from langchain_ollama import ChatOllama

from langchain_core.messages import (SystemMessage, BaseMessage)


llm = ChatOllama(model="deepseek-r1:8b")


async def analyze_node(state: AgentState):
    system: BaseMessage = SystemMessage(content=config.prompt.system_prompt)
    messages: list[BaseMessage] = [system] + state.messages
    response: BaseMessage = await llm.ainvoke(messages)
    logger.debug(f'{Fore.MAGENTA}{state.messages}{Style.RESET_ALL}')
    return dict(messages=[response])


def route_tools(
    state: AgentState,
):
#     """
#     Use in the conditional_edge to route to the ToolNode if the last message
#     has tool calls. Otherwise, route to the end.
#     """
#     if isinstance(state, list):
#         ai_message = state[-1]
#     elif messages := state.messages:
#         ai_message = messages[-1]
#     else:
#         raise ValueError(f"No messages found in input state to tool_edge: {state}")
#     if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
#         return "tool_node"
#     return END


async def response_node(state: AgentState):
    return dict(messages=[state.messages])


def after_analyze_condition(state: AgentState):
    last_message: BaseMessage = state.messages[-1]

    if last_message.tool_calls:
        for tool_call in last_message.tool_calls:
            logger.debug(
                f'{Fore.YELLOW}'
                f'LLM решила вызвать tool '
                f'{tool_call["name"]} '
                f'c аргументами '
                f'{tool_call["args"]}'
                f'{Style.RESET_ALL}'
            )
        return 'tool_node'
    return 'response_node'
