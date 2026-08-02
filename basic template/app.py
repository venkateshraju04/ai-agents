from graph import graph
initial_state = {
    "query": "18*33",
    "answer": ""
}

result = graph.invoke(initial_state)

print(result["answer"])