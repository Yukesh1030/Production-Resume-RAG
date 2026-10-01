def is_relevant(results):
    """
    Determine whether retrieval produced usable evidence.

    We intentionally do not use a fixed cross-encoder
    score threshold because reranker scores depend on
    the model, query, corpus and chunking strategy.
    """

    if not results:
        return False

    return True