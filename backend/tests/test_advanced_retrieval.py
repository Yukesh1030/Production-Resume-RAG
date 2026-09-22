from src.advanced_retriever import AdvancedRetriever


retriever = AdvancedRetriever()


queries = [

    "What technologies does Yukesh know?",

    "What projects has Yukesh worked on?",

    "What is Yukesh's educational background?",

    "Does Yukesh know ChromaDB?"

]


for query in queries:

    print("\n")

    print("=" * 80)

    print("QUERY:")

    print(query)

    print("=" * 80)


    results = retriever.search(
        query,
        candidate_k=5,
        final_k=3
    )


    for rank, result in enumerate(
        results,
        start=1
    ):

        print("\nRank:", rank)

        print(
            "Relevance:",
            round(result["score"], 4)
        )

        print("Document:")

        print(result["document"])