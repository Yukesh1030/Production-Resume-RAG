import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_PATH = PROJECT_ROOT / "backend"

sys.path.insert(0, str(BACKEND_PATH))

from src.advanced_retriever import AdvancedRetriever


QUESTIONS = [
    "What is Yukesh's experience with ReactJS?",
    "What is Yukesh's experience with Java Sockets?",
    "What is Yukesh's favorite food?"
]


def main():

    retriever = AdvancedRetriever()

    for query in QUESTIONS:

        print("\n" + "=" * 90)
        print("QUERY:")
        print(query)
        print("=" * 90)

        results = retriever.search(
            query,
            candidate_k=10,
            final_k=5
        )

        for result in results:

            print("\n" + "-" * 90)
            print(f"Rank: {result['rank']}")
            print(f"ID: {result['id']}")
            print(f"Score: {result['score']:.4f}")
            print("\nDOCUMENT:")
            print(result["document"])


if __name__ == "__main__":
    main()