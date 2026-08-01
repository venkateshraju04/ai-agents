from state import AgentState
from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()

llm=ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
)

def chatbot(state: AgentState):
    response=llm.invoke(state["query"])
    return {
        "answer": response.content
    }