from src.advanced_retriever import AdvancedRetriever
from src.relevance import is_relevant


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

    best_score = results[0]["score"]

    print(f"Best score: {best_score:.4f}")
    print(f"Relevant: {is_relevant(results)}")