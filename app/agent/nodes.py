import logging
import pprint
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

    # logger.debug(f"{Fore.MAGENTA}{analyze_node.__name__}: {pprint.pformat(state)}{Style.RESET_ALL}")

    system_prompt: SystemMessage = SystemMessage(content=get_system_prompt())

    # logger.debug(f'{Fore.LIGHTGREEN_EX}{pprint.pformat(system_prompt)}{Style.RESET_ALL}')

    messages: list[BaseMessage] = [system_prompt] + state.messages
    response: BaseMessage = await llm.ainvoke(messages)

    logger.debug(f"{Fore.YELLOW}{pprint.pformat(response.content)}{Style.RESET_ALL}")
    return dict(messages=[response])


def after_analyze_condition(state: AgentState):
    # logger.debug(f"{Fore.MAGENTA}{after_analyze_condition.__name__}: {pprint.pformat(state)}{Style.RESET_ALL}")
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
    return "end"
