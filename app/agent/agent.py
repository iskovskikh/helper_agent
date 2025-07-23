from langgraph.graph.state import StateGraph, START, END

from agent.nodes import chatbot_node
from agent.state import AgentState

graph_builder = StateGraph(AgentState)

graph_builder.add_node("chatbot_node", chatbot_node)

graph_builder.add_edge(START, 'chatbot_node')
graph_builder.add_edge('chatbot_node', END)

graph = graph_builder.compile()
