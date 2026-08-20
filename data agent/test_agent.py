from graph import graph

initial_state = {
    "query": "Plot the total sales by region as a bar chart.",
    "dataset_path": "sample.csv"
}

final_state = graph.invoke(initial_state)

print("Generated Code:")
print("===============")
print(final_state["generated_code"])
print("\nAgent Summary:")
print("==============")
print(final_state["analysis"])
