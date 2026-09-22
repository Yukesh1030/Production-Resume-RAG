from sentence_transformers import CrossEncoder


MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

model = CrossEncoder(MODEL_NAME)


def rerank(
    query: str,
    documents: list,
    top_k: int = 5
):

    pairs = [
        [query, document["document"]]
        for document in documents
    ]

    scores = model.predict(pairs)

    results = []

    for document, score in zip(
        documents,
        scores
    ):

        results.append({

            "id": document["id"],

            "document": document["document"],

            "metadata": document.get(
                "metadata",
                {}
            ),

            "score": float(score)
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    for rank, result in enumerate(
        results[:top_k],
        start=1
    ):

        result["rank"] = rank

    return results[:top_k]