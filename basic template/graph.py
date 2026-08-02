from langgraph.graph import StateGraph, START, END
from state import AgentState
from nodes import (chatbot,router,calculator_node)

graph_builder = StateGraph(AgentState)

graph_builder.add_node("router", router)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("calculator_node", calculator_node)

graph_builder.add_edge(START, "router")
graph_builder.add_conditional_edges(
    "router",
    lambda state: state["next_node"],
)
graph_builder.add_edge("calculator_node", END)
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()