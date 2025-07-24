from abc import ABC, abstractmethod
from dataclasses import dataclass

from langgraph.graph.state import StateGraph, START, END, CompiledStateGraph

from agent.nodes import analyze_node, response_node, after_analyze_condition
from agent.state import AgentState
from langgraph.prebuilt import ToolNode


@dataclass
class BaseAgent(ABC):
    @abstractmethod
    async def process(self, state: AgentState) -> AgentState: ...


@dataclass
class MyAgent(BaseAgent):

    def __post_init__(self):
        self.graph = self.init_graph()

    def init_graph(self) -> CompiledStateGraph:
        graph_builder = StateGraph(AgentState)

        tool_node = ToolNode(tools=[])

        graph_builder.add_node("analyze_node", analyze_node)
        graph_builder.add_node("response_node", response_node)
        graph_builder.add_node("tool_node", tool_node)

        graph_builder.add_edge(START, 'analyze_node')
        graph_builder.add_conditional_edges(
            'analyze_node',
            after_analyze_condition,
            ['tool_node', 'response_node'],
        )
        graph_builder.add_edge('tool_node', 'analyze_node')
        graph_builder.add_edge('response_node', END)

        return graph_builder.compile()

    async def process(self, state: AgentState) -> AgentState:
        result = await self.graph.ainvoke(state)
        return AgentState(**result)
