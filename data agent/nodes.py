import pandas as pd
from state import AgentState
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from tools import execute_python
import re

load_dotenv()

# We use the same model as the basic template, as requested by the user.
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
)

def data_inspector_node(state: AgentState):
    path = state["dataset_path"]
    try:
        if path.endswith('.csv'):
            df = pd.read_csv(path)
        else:
            df = pd.read_excel(path)
        
        # Get column info and first few rows
        buffer = []
        buffer.append("Columns and Dtypes:")
        for col, dtype in df.dtypes.items():
            buffer.append(f"- {col}: {dtype}")
        buffer.append("\nFirst 3 rows:")
        buffer.append(df.head(3).to_string())
        
        df_head = "\n".join(buffer)
    except Exception as e:
        df_head = f"Error reading dataset: {e}"
        
    return {"df_head": df_head}

def code_generator_node(state: AgentState):
    query = state["query"]
    df_head = state["df_head"]
    error = state.get("error", None)
    
    prompt_str = """You are a Python Data Analyst AI. 
Your goal is to write Python code to analyze a dataset and answer the user's query.
You have access to a pandas DataFrame called `df`. 
You can use pandas, matplotlib.pyplot as plt, and seaborn as sns.
If the user wants a plot, write the code to create it and save it as 'output_plot.png'. Do NOT use plt.show(), use plt.savefig('output_plot.png').
Make sure to print() any statistical results or answers so we can read them from stdout.

Dataset Info:
{df_head}

User Query: {query}
"""
    if error:
         prompt_str += f"\nPrevious attempt failed with error:\n{error}\nPlease fix the code."
    
    prompt_str += "\nReturn ONLY the Python code inside ```python\n...\n``` tags."
    
    prompt = ChatPromptTemplate.from_template(prompt_str)
    chain = prompt | llm
    
    response = chain.invoke({
        "df_head": df_head,
        "query": query
    })
    
    # Extract code between triple backticks
    content = response.content
    code_match = re.search(r"```python(.*?)```", content, re.DOTALL)
    if code_match:
        code = code_match.group(1).strip()
    else:
        # Fallback if no backticks
        code = content.strip()
        
    return {"generated_code": code}

def code_executor_node(state: AgentState):
    code = state["generated_code"]
    dataset_path = state["dataset_path"]
    
    output = execute_python(code, dataset_path)
    
    if "Error executing code" in output:
        return {"error": output, "next_node": "code_generator_node"}
    else:
        return {"analysis": output, "error": None, "next_node": "summarizer_node"}

def summarizer_node(state: AgentState):
    query = state["query"]
    analysis = state["analysis"]
    
    prompt = ChatPromptTemplate.from_template(
        "The user asked: {query}\n\nThe Python data analysis output was:\n{analysis}\n\nPlease provide a clear, concise summary of these findings to the user."
    )
    chain = prompt | llm
    
    response = chain.invoke({
        "query": query,
        "analysis": analysis
    })
    
    return {"analysis": response.content}
