import logging
from pyexpat.errors import messages
from typing import cast

from agent.config import CustomContext
from agent.prompt import get_system_prompt
from agent.state import AgentState


from colorama.ansi import Fore, Style


from langchain_core.runnables import RunnableConfig

from langchain_core.messages import SystemMessage, BaseMessage
from langchain_core.language_models.chat_models import BaseChatModel

from agent.tools import tools_list

logger = logging.getLogger(__name__)


async def analyze_node(
        state: AgentState,
        config: RunnableConfig,
        # context: CustomContext
):
    llm: BaseChatModel = cast(BaseChatModel, config.get("configurable").get("llm"))
    # llm: BaseChatModel = context.llm

    logger.debug(f"{analyze_node.__name__}: {state=}")
    system: BaseMessage = SystemMessage(content=get_system_prompt())
    messages: list[BaseMessage] = [system] + state.messages
    response: BaseMessage = await llm.ainvoke([message.model_dump() for message in messages])
    logger.debug(f"{Fore.MAGENTA}{state.messages}{Style.RESET_ALL}")
    return dict(messages=[response])


async def response_node(state: AgentState):
    logger.debug(f"{response_node.__name__}: {state=}")
    return state


def after_analyze_condition(state: AgentState):
    logger.debug(f"{after_analyze_condition.__name__}: {state=}")
    last_message: BaseMessage = state.messages[-1]

    if last_message.tool_calls:
        for tool_call in last_message.tool_calls:
            logger.debug(
                f"{Fore.YELLOW}"
                f"LLM решила вызвать tool "
                f"{tool_call['name']} "
                f"c аргументами "
                f"{tool_call['args']}"
                f"{Style.RESET_ALL}"
            )
        return "tool_node"
    return "response_node"
