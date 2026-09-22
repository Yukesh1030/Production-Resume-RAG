#For inspect the reranker scores

from src.advanced_retriever import AdvancedRetriever


retriever = AdvancedRetriever()

queries = [
    "What technologies does Yukesh know?",
    "What is Yukesh's educational background?",
    "What is Yukesh's favorite food?",
    "What is Yukesh's experience with React?",
]


for query in queries:

    print("\n" + "=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)

    results = retriever.search(
        query,
        candidate_k=7,
        final_k=5
    )

    for result in results:
        print(f"\nID: {result['id']}")
        print(f"Rank: {result['rank']}")
        print(f"Reranker Score: {result['score']:.4f}")
        print(f"Document: {result['document'][:250]}...")