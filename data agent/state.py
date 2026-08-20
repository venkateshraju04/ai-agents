from typing import TypedDict, Optional

class AgentState(TypedDict):
    query: str
    dataset_path: str
    df_head: Optional[str]
    generated_code: Optional[str]
    analysis: Optional[str]
    error: Optional[str]
    next_node: str
