import logging
import pprint
import traceback
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from colorama import Fore, Style
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.runnables.config import RunnableConfig
from langgraph.graph.state import StateGraph, START, END, CompiledStateGraph
from langgraph.prebuilt import ToolNode

from agent.config import CustomContext
from agent.nodes import analyze_node, response_node, after_analyze_condition
from agent.state import AgentState
from agent.tools import current_datetime_tool, tools_list

logger = logging.getLogger(__name__)


def handle_errors(e: Exception) -> str:
    logger.exception(e)
    formatted_trace = traceback.format_exc()
    return f"An error occurred:\n{formatted_trace}"


# @dataclass
# class BaseAgent(ABC):
#
#     @abstractmethod
#     async def process(self, state: AgentState)-> AgentState: ...
#
#
# @dataclass
# class Agent(BaseAgent):
#     llm: BaseChatModel
#     graph: CompiledStateGraph = field(init=False)
#
#     def __post_init__(self):
#         self.graph = self.get_graph(tools= tools_list)
#
#     def get_graph(self, tools:list[Callable])->CompiledStateGraph:
#
#         self.llm.bind_tools(tools)
#         graph_builder = StateGraph(AgentState)
#
#         tool_node = ToolNode(tools, handle_tool_errors=handle_errors)
#
#         graph_builder.add_node("chatbot_node", chatbot_node)
#         graph_builder.add_node("tool_node", tool_node)
#
#         graph_builder.add_edge(START, 'chatbot_node')
#         graph_builder.add_conditional_edges(
#             "chatbot_node",
#             route_tools,
#             {"tools": "tool_node", END: END},
#         )
#         graph_builder.add_edge('chatbot_node', END)
#
#
#
#         return graph_builder.compile()
#
#     async def process(self, state: AgentState) -> AgentState:
#
#         result = await self.graph.ainvoke(input=state)
#
#         new_state: AgentState = AgentState(**result)
#
#         return new_state


@dataclass
class BaseAgent(ABC):
    graph: CompiledStateGraph = field(init=False)

    @abstractmethod
    async def process(self, state: AgentState) -> AgentState: ...


@dataclass
class Agent(BaseAgent):
    llm: BaseChatModel

    def __post_init__(self):
        self.graph = self.init_graph()

    def init_graph(self) -> CompiledStateGraph:
        graph_builder = StateGraph(AgentState)

        tool_node = ToolNode(tools=tools_list)

        graph_builder.add_node("analyze_node", analyze_node)
        graph_builder.add_node("response_node", response_node)
        graph_builder.add_node("tool_node", tool_node)

        graph_builder.add_edge(START, "analyze_node")
        graph_builder.add_conditional_edges(
            "analyze_node",
            after_analyze_condition,
            ["tool_node", "response_node"],
        )
        graph_builder.add_edge("tool_node", "analyze_node")
        graph_builder.add_edge("response_node", END)

        return graph_builder.compile()

    async def process(self, state: AgentState) -> AgentState:
        logger.debug(f"вызвали агента {state}")

        config = RunnableConfig(
            configurable=dict(
                llm=self.llm,
            )
        )

        context = CustomContext(
            llm=self.llm,
        )
        result = await self.graph.ainvoke(
            input=state,
            config=config,
            # context=context,
        )

        r = pprint.pformat(result)

        logger.debug(f"{Fore.RED}{r=}{Style.RESET_ALL}")
        return AgentState(**result)
