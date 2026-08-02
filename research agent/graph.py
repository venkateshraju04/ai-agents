from langgraph.graph import StateGraph, START, END
from state import AgentState
from nodes import search_node, summarize, route, direct_answer

graph_builder=StateGraph(AgentState)

graph_builder.add_node("search",search_node)
graph_builder.add_node("summarize", summarize)
graph_builder.add_node("direct_answer", direct_answer)

graph_builder.add_conditional_edges(
    START,
    route,
    {
        "search":"search",
        "answer":"direct_answer",
    },
)
graph_builder.add_edge("search", "summarize")

graph_builder.add_edge("summarize", END)
graph_builder.add_edge("direct_answer", END)

graph = graph_builder.compile()