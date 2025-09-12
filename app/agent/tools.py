import logging
from datetime import datetime, UTC

from duckduckgo_search import DDGS
from langchain_core.tools import tool

from agent.state import AgentState

logger = logging.getLogger(__name__)



@tool
def current_datetime_tool(state: AgentState):
    """
    Инструмент для получения текущей даты и времени
    """
    result = datetime.now(UTC)

    logger.debug(f"Дата и время сейчас: {result}")

    return result


@tool
def web_search_tool(search: str, state: AgentState):
    """
    Инструмент для поиска в интернете
    """
    results = DDGS().text(search, max_results=5)

    logger.debug(f"поиск в интернете нашел {results}")

    return results


tools_list = [
    current_datetime_tool,
    web_search_tool,
]
