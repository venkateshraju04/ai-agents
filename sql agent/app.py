from graph import graph


while True:

    question = input("\nAsk a question: ")

    if question.lower() == "exit":
        break

    result = graph.invoke(
        {
            "question": question
        }
    )

    print("\nAnswer:\n")

    print(result["final_answer"])
