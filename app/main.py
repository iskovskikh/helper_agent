import asyncio
import logging
import sys

from colorama import Fore, Style, init as colorama_init

from agent.agent import Agent, BaseAgent
from agent.nodes import llm
from agent.state import AgentState
from langchain_core.messages import HumanMessage

from settings.logger import init_logger

init_logger()

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

    agent: BaseAgent = Agent(llm=llm)
    state: AgentState = AgentState()

    while True:
        user_input = input("User: ")
        logger.debug(f'{Fore.GREEN}User: {user_input}{Style.RESET_ALL}')

        state.messages.append(HumanMessage(content=user_input))

        state = await agent.process(state=state)

        logger.debug(f'{Fore.BLUE}Assistant: {state.messages[-1].content}{Style.RESET_ALL}')



if __name__ == "__main__":
    colorama_init()
    asyncio.run(main())
