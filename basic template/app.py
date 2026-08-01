from graph import graph
initial_state = {
    "query": "who invented python?",
    "answer": ""
}

result = graph.invoke(initial_state)

print(result["answer"])