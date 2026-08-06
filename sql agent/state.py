from typing import TypedDict


class AgentState(TypedDict):
    question: str
    generated_sql: str
    query_result: list
    final_answer: str
