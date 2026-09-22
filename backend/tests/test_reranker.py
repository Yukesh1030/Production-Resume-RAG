from src.hybrid_search import HybridRetriever
from src.reranker import rerank


retriever = HybridRetriever()


query = "What technologies does Yukesh know?"


hybrid_results = retriever.search(
    query,
    top_k=5
)


results = rerank(
    query,
    hybrid_results,
    top_k=4
)


print("\n" + "=" * 80)
print("RERANKED RESULTS")
print("=" * 80)


for result in results:

    print(f"\nRank: {result['rank']}")
    print(f"ID: {result['id']}")
    print(f"Score: {result['score']:.4f}")

    print("Metadata:")
    print(result["metadata"])

    print("Document:")
    print(result["document"][:300])