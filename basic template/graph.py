from langgraph.graph import StateGraph, START, END
from state import AgentState
from nodes import chatbot

graph_builder = StateGraph(AgentState)

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()