import sys
from pathlib import Path


# ============================================================
# ADD BACKEND TO PYTHON PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_PATH = PROJECT_ROOT / "backend"

sys.path.insert(0, str(BACKEND_PATH))


# ============================================================
# IMPORT PROJECT MODULES
# ============================================================

from src.corpus import get_all_documents


# ============================================================
# INSPECT CHUNKS
# ============================================================

def main():

    ids, documents, metadatas = get_all_documents()

    print("\n" + "=" * 80)
    print("RESUME CHUNKS")
    print("=" * 80)

    for document_id, document, metadata in zip(
        ids,
        documents,
        metadatas
    ):

        print("\n" + "-" * 80)

        print(f"ID: {document_id}")

        print(
            f"Chunk Index: "
            f"{metadata.get('chunk_index')}"
        )

        print("-" * 80)

        print(document)

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()