from src.semantic_search import semantic_search
from src.corpus import get_all_documents
from src.keyword_search import BM25Retriever
from src.rrf import reciprocal_rank_fusion


class HybridRetriever:

    def __init__(self):

        document_ids, documents, metadatas = get_all_documents()

        self.bm25 = BM25Retriever(
            document_ids,
            documents,
            metadatas
        )

    def search(
        self,
        query: str,
        top_k: int = 5
    ):

        semantic_results = semantic_search(
            query,
            top_k=top_k
        )

        keyword_results = self.bm25.search(
            query,
            top_k=top_k
        )

        hybrid_results = reciprocal_rank_fusion(
            [
                semantic_results,
                keyword_results
            ]
        )

        return hybrid_results[:top_k]