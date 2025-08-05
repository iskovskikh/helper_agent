import asyncio
import logging
import sys

from colorama import Fore, Style, init as colorama_init

from agent.agent import Agent, BaseAgent
from agent.nodes import llm
from agent.state import AgentState
from langchain_core.messages import HumanMessage, AIMessage,SystemMessage

from settings.logger import init_logger

init_logger()

# from agent.agent import BaseAgent, MyAgent
# from agent.state import AgentState
# from langchain_core.messages import HumanMessage
#
# import  logging.config
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

async def main():

    agent: BaseAgent = Agent()

    print(f'\n{agent.graph.get_graph().draw_ascii()}')

    state: AgentState = AgentState()

    while True:
        user_input = input("User: ")
        print(f'{Fore.GREEN}User: {user_input}{Style.RESET_ALL}')

        state.messages.append(HumanMessage(content='Какая погода в москве?'))

        logger.debug(f'{state=}')

        state = await agent.process(state=state)

        if state.messages:
            last_message = state.messages[-1]
            if isinstance(last_message, (HumanMessage, AIMessage)):
                print(f'{Fore.BLUE}Assistant: {last_message.content}{Style.RESET_ALL}')
            else:
                print(f'{Fore.BLUE}Assistant: {str(last_message)}{Style.RESET_ALL}')




if __name__ == "__main__":
    colorama_init()
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
