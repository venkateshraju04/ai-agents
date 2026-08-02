from state import AgentState
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from tools import calculator

load_dotenv()



llm=ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
)

def router(state: AgentState):
    query=state["query"]
    if any(op in query for op in ["+", "-", "*", "/"]):
        return{
            "next_node":"calculator_node"
        }
    return{
        "next_node":"chatbot"
    }

def chatbot(state: AgentState):
    response=llm.invoke(state["query"])
    return {
        "answer": response.content
    }

def calculator_node(state: AgentState):
    expression=state["query"]
    answer=calculator(expression)
    return {
        "answer": answer
    }
