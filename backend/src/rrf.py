def reciprocal_rank_fusion(
    result_lists,
    k=60
):

    scores = {}
    documents = {}
    metadata = {}

    for results in result_lists:

        for result in results:

            document_id = result["id"]
            rank = result["rank"]

            if document_id not in scores:

                scores[document_id] = 0.0

                documents[document_id] = (
                    result["document"]
                )

                metadata[document_id] = (
                    result.get("metadata", {})
                )

            scores[document_id] += (
                1 / (k + rank)
            )

    ranked_results = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    output = []

    for final_rank, (
        document_id,
        score
    ) in enumerate(
        ranked_results,
        start=1
    ):

        output.append({

            "id": document_id,

            "document": documents[
                document_id
            ],

            "metadata": metadata[
                document_id
            ],

            "score": score,

            "rank": final_rank
        })

    return output