RELEVANCE_THRESHOLD = -5.0


def is_relevant(results, threshold=RELEVANCE_THRESHOLD):
    if not results:
        return False

    best_score = results[0]["score"]

    return best_score >= threshold