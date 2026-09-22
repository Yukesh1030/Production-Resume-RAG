from src.semantic_search import semantic_search


results = semantic_search(
    "What technologies does Yukesh know?",
    top_k=3
)


for result in results:

    print("\n" + "=" * 60)

    print(f"ID: {result['id']}")

    print(f"Distance: {result['distance']:.4f}")

    print("Document:")
    print(result["document"])

    print("Metadata:")
    print(result.get("metadata"))