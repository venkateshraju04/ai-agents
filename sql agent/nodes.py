from state import AgentState
from llm import structured_llm, llm
from prompts import SQL_GENERATION_PROMPT
from database import get_connection
from schema import get_schema


def generate_sql_node(state: AgentState):
    question = state["question"]
    schema = get_schema()

    prompt = SQL_GENERATION_PROMPT.format(
        schema=schema,
        question=question
    )

    response = structured_llm.invoke(prompt)

    return {
        "generated_sql": response.sql
    }


def execute_sql_node(state: AgentState):
    sql = state["generated_sql"]

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except Exception as e:
        results = [f"Error executing SQL: {e}"]
    finally:
        conn.close()

    return {
        "query_result": results
    }


def generate_answer_node(state: AgentState):
    question = state["question"]
    sql = state["generated_sql"]
    results = state["query_result"]

    prompt = f"""
You are a helpful assistant.

The user asked: {question}

The SQL query used was:
{sql}

The query returned these results:
{results}

Please provide a clear, natural language answer to the user's question based on the results above.
If the results contain an error, explain what went wrong.
"""

    response = llm.invoke(prompt)

    return {
        "final_answer": response.content
    }
