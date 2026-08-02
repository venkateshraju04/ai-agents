from tools import web_search
from state import AgentState
from langchain_groq import ChatGroq
from prompts import SEARCH_SUMMARY_PROMPT
from pydantic import BaseModel
from typing import Literal

class RouteDecision(BaseModel):
    route: Literal["search", "answer"]



llm=ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
)

router_llm = llm.with_structured_output(RouteDecision)

def route(state:AgentState):
    question=state["messages"][-1].content
    decision = router_llm.invoke(
        f"""
        Decide whether this question
        requires web search.

        Question:
        {question}
        """
    )
    return decision.route


def search_node(state: AgentState):
    question=state["messages"][-1].content
    results=web_search(question)
    return{
        "search_results":results
    }

def summarize(state: AgentState):
    results=state["search_results"]
    question=state["messages"][-1].content
    context=""

    for item in results["results"]:
        context += f"""
        Title: {item["title"]}

        Content:
        {item["content"]}

        Source:
        {item["url"]}

-------------------------
    """
    prompt = SEARCH_SUMMARY_PROMPT.format(
        context=context,
        question=question
    )

    response = llm.invoke(prompt)

    return {
        "messages": [response]
    }

def direct_answer(state: AgentState):
    response = llm.invoke(state["messages"])

    return {
        "messages": [response]
    }