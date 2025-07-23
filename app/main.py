import logging
import sys

from colorama import Fore, Style

from agent.agent import graph
logger = logging.getLogger(__name__)

def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print(f'{Fore.BLUE}Assistant: {value["messages"][-1].content}{Style.RESET_ALL}')


def main():
    while True:
        try:
            user_input = input("User: ")
        except UnicodeDecodeError:
            user_input = sys.stdin.buffer.read().decode('utf-8', errors='replace')
        logger.debug(user_input)
        if user_input.lower() in ["quit", "exit", "q"]:
            break

        stream_graph_updates(user_input)

if __name__ == "__main__":
    main()
