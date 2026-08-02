from graph import graph
from langchain_core.messages import HumanMessage

initial_state = {
    "messages": [
        HumanMessage(content="bangalore news today")
    ]
}

result = graph.invoke(initial_state)

print(result["messages"][-1].content)