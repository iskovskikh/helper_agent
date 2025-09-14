import logging
from datetime import datetime, UTC

import requests
from colorama import Fore, Style
from langchain_core.tools import tool

from agent.state import AgentState

logger = logging.getLogger(__name__)



@tool
def current_datetime_tool():
    """
    Инструмент для получения текущей даты и времени в формате ISO8601
    """
    result = datetime.now(UTC)


    logger.debug(f"{Fore.RED}Дата и время сейчас: {result}{Style.RESET_ALL}")

    return result


@tool
def web_search_tool(query: str, state: AgentState):
    """
    Делает поиск в интернете по запросу и возвращает краткие результаты.
    Использует DuckDuckGo API.
    """
    url = "https://api.duckduckgo.com/"
    params = {"q": query, "format": "json", "no_html": 1, "skip_disambig": 1}

    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
    except Exception as e:
        return f"Ошибка при запросе: {e}"

    results = []

    # Берём краткие данные
    if data.get("AbstractText"):
        results.append(data["AbstractText"])
    if data.get("RelatedTopics"):
        for t in data["RelatedTopics"][:3]:
            if "Text" in t:
                results.append(t["Text"])

    if not results:
        return "Ничего не найдено."

    logger.debug(f'{Fore.RED}{results}{Style.RESET_ALL}')
    return "\n".join(results)


tools_list = [
    current_datetime_tool,
    web_search_tool,
]
