from langchain_groq import ChatGroq
from dotenv import load_dotenv

from models import SQLResponse

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

structured_llm = llm.with_structured_output(SQLResponse)
