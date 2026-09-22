from src.hybrid_search import HybridRetriever
from src.reranker import rerank


class AdvancedRetriever:

    def __init__(self):
        self.hybrid_retriever = HybridRetriever()

    def search(
        self,
        query: str,
        candidate_k: int = 10,
        final_k: int = 5
    ):

        # Step 1: Retrieve candidates
        hybrid_results = self.hybrid_retriever.search(
            query,
            top_k=candidate_k
        )

        # Step 2: Re-rank candidates
        reranked_results = rerank(
            query,
            hybrid_results,
            top_k=final_k
        )

        return reranked_results