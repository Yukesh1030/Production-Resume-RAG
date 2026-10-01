import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_PATH = PROJECT_ROOT / "backend"

sys.path.insert(0, str(BACKEND_PATH))

from src.semantic_search import semantic_search
from src.keyword_search import BM25Retriever
from src.corpus import get_all_documents
from src.rrf import reciprocal_rank_fusion
from src.reranker import rerank


QUERY = "What projects has Yukesh worked on?"


def print_results(title, results):

    print("\n" + "=" * 90)
    print(title)
    print("=" * 90)

    for result in results:

        print("\n" + "-" * 90)

        print(f"Rank: {result.get('rank')}")
        print(f"ID: {result.get('id')}")

        if "score" in result:
            print(f"Score: {result['score']:.4f}")

        if "distance" in result:
            print(f"Distance: {result['distance']:.4f}")

        print("\nDOCUMENT:")
        print(result["document"])


def main():

    print("\n")
    print("#" * 90)
    print("RETRIEVAL DEBUG")
    print("#" * 90)

    print(f"\nQUERY:")
    print(QUERY)

    # -------------------------------------------------
    # 1. SEMANTIC SEARCH
    # -------------------------------------------------

    semantic_results = semantic_search(
        QUERY,
        top_k=10
    )

    print_results(
        "1. SEMANTIC SEARCH",
        semantic_results
    )

    # -------------------------------------------------
    # 2. BM25 SEARCH
    # -------------------------------------------------

    ids, documents, metadatas = get_all_documents()

    bm25 = BM25Retriever(
        ids,
        documents,
        metadatas
    )

    keyword_results = bm25.search(
        QUERY,
        top_k=10
    )

    print_results(
        "2. BM25 KEYWORD SEARCH",
        keyword_results
    )

    # -------------------------------------------------
    # 3. RRF HYBRID SEARCH
    # -------------------------------------------------

    hybrid_results = reciprocal_rank_fusion(
        [
            semantic_results,
            keyword_results
        ]
    )

    print_results(
        "3. RRF HYBRID SEARCH",
        hybrid_results[:5]
    )

    # -------------------------------------------------
    # 4. CROSS-ENCODER RERANKING
    # -------------------------------------------------

    reranked_results = rerank(
        QUERY,
        hybrid_results[:5],
        top_k=5
    )

    print_results(
        "4. CROSS-ENCODER RERANKING",
        reranked_results
    )

    print("\n" + "#" * 90)
    print("DEBUG COMPLETE")
    print("#" * 90)


if __name__ == "__main__":
    main()