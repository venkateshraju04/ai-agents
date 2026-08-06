from langgraph.graph import StateGraph, START, END

from state import AgentState

from nodes import (
    generate_sql_node,
    execute_sql_node,
    generate_answer_node
)

builder = StateGraph(AgentState)

builder.add_node(
    "generate_sql",
    generate_sql_node
)

builder.add_node(
    "execute_sql",
    execute_sql_node
)

builder.add_node(
    "generate_answer",
    generate_answer_node
)

builder.add_edge(
    START,
    "generate_sql"
)

builder.add_edge(
    "generate_sql",
    "execute_sql"
)

builder.add_edge(
    "execute_sql",
    "generate_answer"
)

builder.add_edge(
    "generate_answer",
    END
)

graph = builder.compile()
