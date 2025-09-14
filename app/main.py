import asyncio
import logging
from pyexpat.errors import messages

from colorama import Fore, Style, init as colorama_init

from agent.agent import Agent, BaseAgent
from agent.state import AgentState
from langchain_core.messages import HumanMessage, AIMessage

from agent.tools import tools_list
from settings import config
from settings.config import print_config
from settings.logger import init_logger
from langchain_ollama import ChatOllama
from langchain_ollama.llms import OllamaLLM

init_logger()

# from agent.agent import BaseAgent, MyAgent
# from agent.state import AgentState
# from langchain_core.messages import HumanMessage
#
import  logging.config
#
# from settings.config import config
# from settings.logger import get_logger_config

logger = logging.getLogger(__name__)

# def stream_graph_updates(user_input: str):
#     for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
#         for value in event.values():
#             print(f'{Fore.BLUE}Assistant: {value["messages"][-1].content}{Style.RESET_ALL}')
#
#
# def main():
#     while True:
#         try:
#             user_input = input("User: ")
#         except UnicodeDecodeError:
#             user_input = sys.stdin.buffer.read().decode('utf-8', errors='replace')
#         logger.debug(user_input)
#         if user_input.lower() in ["quit", "exit", "q"]:
#             break
#
#         stream_graph_updates(user_input)
import datetime
from typing import TypedDict, Annotated
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, create_react_agent

from langgraph.prebuilt import create_react_agent

async def main():

    # # ---------- Инструменты ----------
    # @tool
    # def get_time() -> str:
    #     """Возвращает текущее время"""
    #     return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #
    # @tool
    # def add_numbers(a: int, b: int) -> int:
    #     """Складывает два числа"""
    #     return a + b
    #
    # tools = [get_time, add_numbers]
    #
    # # ---------- Модель ----------
    # llm = ChatOllama(
    #     model="MFDoom/deepseek-r1-tool-calling:8b",
    #     # model="deepseek-r1:8b",
    #     # base_url="http://localhost:11434",  # ollama endpoint
    # )
    #
    # # ---------- Агент ----------
    # # LangGraph уже умеет собирать ReAct-агента (инструменты + LLM)
    # graph = create_react_agent(llm, tools)
    #
    # inputs = {"messages": [("user", "Сколько будет 7 + 12?")]}
    #
    # for step in graph.stream(inputs):
    #     print(step)


    # model = ChatOllama(
    #     model="deepseek-r1:8b",
    #     reasoning=False,
    # )
    # model = ChatOllama(
    #     model="llama3.1:8b",
    #     reasoning=False,
    # )
    model = ChatOllama(
        model="llama3.1:8b-instruct-q6_K",
        reasoning=False,
    )
    # model = ChatOllama(
    #     model="MFDoom/deepseek-r1-tool-calling:8b",
    #     reasoning=False,
    # )
    model = model.bind_tools(tools=tools_list)


    # state: AgentState = AgentState()
    # state.messages.append(HumanMessage(content="Какие сейчас дата и время?"))
    # result = await model.ainvoke(input=state.messages)
    #
    # logger.debug(result)
    #
    # response = model.invoke("поддеживаешь ли ты вызов тулов?")
    #
    # logger.debug(response)

    agent: BaseAgent = Agent(llm=model)

    print(f"\n{agent.graph.get_graph().draw_ascii()}")

    state: AgentState = AgentState()

    while True:
        user_input = input("User: ")
        print(f"{Fore.LIGHTGREEN_EX}User: {user_input}{Style.RESET_ALL}")

        # state.messages.append(HumanMessage(content="Какая сейчас погода в Москве?"))
        # state.messages.append(HumanMessage(content="Какие сейчас дата и время?"))
        state.messages.append(HumanMessage(content=user_input))

        logger.debug(f"{state=}")

        state = await agent.process(state=state)

        if state.messages:
            last_message = state.messages[-1]
            if isinstance(last_message, (HumanMessage, AIMessage)):
                print(f"{Fore.LIGHTBLUE_EX}Assistant: {last_message.content}{Style.RESET_ALL}")
            else:
                print(f"{Fore.LIGHTBLUE_EX}Assistant: {str(last_message)}{Style.RESET_ALL}")


if __name__ == "__main__":
    colorama_init()
    init_logger()
    print_config()
    asyncio.run(main())
# =======
#     while True:
#         # try:
#         #     user_input = input("User: ")
#         # except UnicodeDecodeError:
#         #     user_input = sys.stdin.buffer.read().decode('utf-8', errors='replace')
#
#         user_input = input("User: ")
#
#         print(f'{Fore.GREEN}{user_input}{Style.RESET_ALL}')
#
#         state.messages.append(HumanMessage(content=user_input))
#         state = await agent.process(state=state)
#         resource = state.messages[-1].content
#
#         print(f'{Fore.BLUE}{resource}{Style.RESET_ALL}')
#
# if __name__ == "__main__":
#     logging.config.dictConfig(get_logger_config(config=config))
#     asyncio.run(main())
