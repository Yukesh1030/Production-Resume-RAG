import json
import sys
from pathlib import Path


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

BACKEND_PATH = PROJECT_ROOT / "backend"

sys.path.insert(0, str(BACKEND_PATH))


# ============================================================
# IMPORT RAG RETRIEVER
# ============================================================

from src.advanced_retriever import AdvancedRetriever


# ============================================================
# CONFIGURATION
# ============================================================

DATASET_PATH = (
    PROJECT_ROOT
    / "evaluation"
    / "evaluation_dataset.json"
)

TOP_K = 3


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():

    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ============================================================
# HIT@K
# ============================================================

def hit_at_k(
    retrieved_ids,
    relevant_ids
):

    if not relevant_ids:
        return 1 if not retrieved_ids else 0

    return int(
        any(
            document_id in relevant_ids
            for document_id in retrieved_ids
        )
    )


# ============================================================
# PRECISION@K
# ============================================================

def precision_at_k(
    retrieved_ids,
    relevant_ids,
    k
):

    if not retrieved_ids:
        return 0.0

    relevant_count = sum(
        document_id in relevant_ids
        for document_id in retrieved_ids[:k]
    )

    return relevant_count / min(
        k,
        len(retrieved_ids)
    )


# ============================================================
# RECALL@K
# ============================================================

def recall_at_k(
    retrieved_ids,
    relevant_ids,
    k
):

    if not relevant_ids:
        return 1.0

    retrieved_relevant = sum(
        document_id in relevant_ids
        for document_id in retrieved_ids[:k]
    )

    return retrieved_relevant / len(
        relevant_ids
    )


# ============================================================
# MRR
# ============================================================

def reciprocal_rank(
    retrieved_ids,
    relevant_ids
):

    if not relevant_ids:
        return 1.0 if not retrieved_ids else 0.0

    for rank, document_id in enumerate(
        retrieved_ids,
        start=1
    ):

        if document_id in relevant_ids:

            return 1 / rank

    return 0.0


# ============================================================
# MAIN EVALUATION
# ============================================================

def main():

    dataset = load_dataset()

    retriever = AdvancedRetriever()


    total_hit = 0.0

    total_precision = 0.0

    total_recall = 0.0

    total_mrr = 0.0


    print("\n" + "=" * 80)

    print("RAG RETRIEVAL EVALUATION")

    print("=" * 80)

    print(f"\nQuestions evaluated: {len(dataset)}")

    print(f"Top-K: {TOP_K}")


    # ========================================================
    # EVALUATE EACH QUESTION
    # ========================================================

    for item in dataset:

        question = item["question"]

        relevant_ids = set(
            item["relevant_chunk_ids"]
        )


        # ----------------------------------------------------
        # Run actual retriever
        # ----------------------------------------------------

        results = retriever.search(
            question,
            candidate_k=5,
            final_k=TOP_K
        )


        retrieved_ids = [
            result["id"]
            for result in results
        ]


        # ----------------------------------------------------
        # Calculate metrics
        # ----------------------------------------------------

        hit = hit_at_k(
            retrieved_ids,
            relevant_ids
        )

        precision = precision_at_k(
            retrieved_ids,
            relevant_ids,
            TOP_K
        )

        recall = recall_at_k(
            retrieved_ids,
            relevant_ids,
            TOP_K
        )

        mrr = reciprocal_rank(
            retrieved_ids,
            relevant_ids
        )


        total_hit += hit

        total_precision += precision

        total_recall += recall

        total_mrr += mrr


        # ----------------------------------------------------
        # Print result
        # ----------------------------------------------------

        print("\n" + "-" * 80)

        print(f"ID: {item['id']}")

        print(f"Question: {question}")

        print(
            f"Expected: "
            f"{list(relevant_ids)}"
        )

        print(
            f"Retrieved: "
            f"{retrieved_ids}"
        )

        print(
            f"Hit@{TOP_K}: "
            f"{hit:.3f}"
        )

        print(
            f"Precision@{TOP_K}: "
            f"{precision:.3f}"
        )

        print(
            f"Recall@{TOP_K}: "
            f"{recall:.3f}"
        )

        print(
            f"MRR: "
            f"{mrr:.3f}"
        )


    # ========================================================
    # AVERAGES
    # ========================================================

    count = len(dataset)


    average_hit = total_hit / count

    average_precision = (
        total_precision / count
    )

    average_recall = (
        total_recall / count
    )

    average_mrr = (
        total_mrr / count
    )


    # ========================================================
    # FINAL REPORT
    # ========================================================

    print("\n" + "=" * 80)

    print("FINAL RETRIEVAL EVALUATION")

    print("=" * 80)

    print(
        f"\nHit@{TOP_K}: "
        f"{average_hit:.3f}"
    )

    print(
        f"Precision@{TOP_K}: "
        f"{average_precision:.3f}"
    )

    print(
        f"Recall@{TOP_K}: "
        f"{average_recall:.3f}"
    )

    print(
        f"MRR: "
        f"{average_mrr:.3f}"
    )

    print("\n" + "=" * 80)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()