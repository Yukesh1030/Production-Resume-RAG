def build_sources(results):

    sources = []

    for result in results:

        metadata = result.get(
            "metadata",
            {}
        )

        sources.append({

            "id": result["id"],

            "source": metadata.get(
                "source",
                "unknown"
            ),

            "chunk_index": metadata.get(
                "chunk_index"
            ),

            "score": result.get(
                "score"
            )

        })

    return sources