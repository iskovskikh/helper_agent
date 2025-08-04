import logging

from duckduckgo_search import DDGS
from langchain_core.tools import tool

from agent.state import AgentState

logger = logging.getLogger(__name__)

@tool
def web_search_tool(
        search: str,
        state: AgentState
):
    """
    Инструмент для поиска в интернете
    """
    results = DDGS().text(search, max_results=5)

    logger.debug(f'поиск в интернете нашел {results}')

    return results

tools_list = [
    web_search_tool,
]