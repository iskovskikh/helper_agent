import logging

from colorama.ansi import Fore, Style

from agent.state import AgentState
from settings.config import config

logger = logging.getLogger(__name__)

from langchain_ollama import ChatOllama

from langchain_core.messages import (SystemMessage, BaseMessage)

llm = ChatOllama(model="deepseek-r1:8b")


async def analyze_node(state: AgentState):
    system: BaseMessage = SystemMessage(content=config.prompt.system_prompt)
    messages: list[BaseMessage] = [system] + state.messages
    response: BaseMessage = await llm.ainvoke(messages)
    logger.debug(f'{Fore.MAGENTA}{state.messages}{Style.RESET_ALL}')
    return dict(messages=[response])


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