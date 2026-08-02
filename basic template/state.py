from typing import TypedDict

class AgentState(TypedDict):
    query: str
    answer: str
    next_node: str
