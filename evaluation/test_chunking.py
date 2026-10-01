import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_PATH = PROJECT_ROOT / "backend"

sys.path.insert(0, str(BACKEND_PATH))

from src.loaders import load_pdf
from src.chunking import chunk_text


PDF_PATH = BACKEND_PATH / "data" / "resume.pdf"


def main():

    print("\n" + "=" * 90)
    print("NEW STRUCTURE-AWARE CHUNKS")
    print("=" * 90)

    text = load_pdf(str(PDF_PATH))

    chunks = chunk_text(
        text,
        chunk_size=1200,
        overlap=100
    )

    print(f"\nTotal chunks: {len(chunks)}")

    for chunk in chunks:

        print("\n" + "-" * 90)

        print(
            f"Chunk Index: "
            f"{chunk['chunk_index']}"
        )

        print("-" * 90)

        print(chunk["text"])

    print("\n" + "=" * 90)


if __name__ == "__main__":
    main()