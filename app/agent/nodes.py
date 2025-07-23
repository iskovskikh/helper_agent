import logging

from agent.state import AgentState
from colorama import Fore, Style
# from langchain_deepseek import ChatDeepSeek

# from settings.config import config

logger = logging.getLogger(__name__)

# llm = ChatDeepSeek(
#     model="deepseek-chat",
#     temperature=0,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
#     api_key=config.api_key.get_secret_value(),
#     # other params...
# )

from langchain_ollama import OllamaLLM
from langchain_ollama import ChatOllama

# llm = OllamaLLM(model="deepseek-r1:8b")
llm = ChatOllama(model="deepseek-r1:8b")


def chatbot_node(state: AgentState):
    state.messages = [llm.invoke(state.messages)]

    return state
