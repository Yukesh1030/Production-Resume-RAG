import re
from rank_bm25 import BM25Okapi


def tokenize(text: str):
    return re.findall(
        r"\b\w+\b",
        text.lower()
    )


class BM25Retriever:

    def __init__(
        self,
        document_ids,
        documents,
        metadatas
    ):

        self.document_ids = document_ids
        self.documents = documents
        self.metadatas = metadatas

        tokenized_documents = [
            tokenize(document)
            for document in documents
        ]

        self.bm25 = BM25Okapi(
            tokenized_documents
        )

    def search(
        self,
        query: str,
        top_k: int = 5
    ):

        query_tokens = tokenize(query)

        scores = self.bm25.get_scores(
            query_tokens
        )

        ranked_indices = scores.argsort()[::-1]

        results = []

        for rank, index in enumerate(
            ranked_indices[:top_k],
            start=1
        ):

            results.append({
                "id": self.document_ids[index],
                "document": self.documents[index],
                "metadata": self.metadatas[index],
                "score": float(scores[index]),
                "rank": rank
            })

        return results