from src.semantic_search import semantic_search


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

    results = semantic_search(query, top_k=3)

    for result in results:
        print(f"\nID: {result['id']}")
        print(f"Distance: {result['distance']:.4f}")
        print(f"Document: {result['document'][:250]}...")