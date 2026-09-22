from src.semantic_search import semantic_search


queries = [
    "What technologies does Yukesh know?",
    "What projects has Yukesh worked on?",
    "What is Yukesh's educational background?",
    "Does Yukesh know ChromaDB?"
]


for query in queries:

    print("\n")
    print("=" * 70)

    print("QUERY:")
    print(query)

    print("=" * 70)


    results = semantic_search(
        query,
        top_k=3
    )


    for result in results:

        print("\nRank:", result["rank"])

        print("ID:", result["id"])

        print(
            "Distance:",
            round(result["distance"], 4)
        )

        print("Document:")

        print(result["document"])