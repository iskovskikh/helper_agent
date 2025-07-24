import asyncio
import logging
import sys

from colorama import Fore, Style

from agent.agent import BaseAgent, MyAgent
from agent.state import AgentState
from langchain_core.messages import HumanMessage

import     logging.config

from settings.config import config
from settings.logger import get_logger_config

logger = logging.getLogger(__name__)


async def main():

    agent: BaseAgent = MyAgent()

    state: AgentState = AgentState()

    while True:
        # try:
        #     user_input = input("User: ")
        # except UnicodeDecodeError:
        #     user_input = sys.stdin.buffer.read().decode('utf-8', errors='replace')

        user_input = input("User: ")

        print(f'{Fore.GREEN}{user_input}{Style.RESET_ALL}')

        state.messages.append(HumanMessage(content=user_input))
        state = await agent.process(state=state)
        resource = state.messages[-1].content

        print(f'{Fore.BLUE}{resource}{Style.RESET_ALL}')

if __name__ == "__main__":
    logging.config.dictConfig(get_logger_config(config=config))
    asyncio.run(main())
