from langgraph.graph import StateGraph, START, END
from state import AgentState
from nodes import (data_inspector_node, code_generator_node, code_executor_node, summarizer_node)

graph_builder = StateGraph(AgentState)

graph_builder.add_node("data_inspector", data_inspector_node)
graph_builder.add_node("code_generator", code_generator_node)
graph_builder.add_node("code_executor", code_executor_node)
graph_builder.add_node("summarizer", summarizer_node)

graph_builder.add_edge(START, "data_inspector")
graph_builder.add_edge("data_inspector", "code_generator")
graph_builder.add_edge("code_generator", "code_executor")

# Conditional routing: if execution fails, go back to generator to fix, else summarize
graph_builder.add_conditional_edges(
    "code_executor",
    lambda state: state["next_node"],
    {
        "code_generator_node": "code_generator",
        "summarizer_node": "summarizer"
    }
)

graph_builder.add_edge("summarizer", END)

graph = graph_builder.compile()
