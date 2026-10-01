from src.loaders import load_pdf
from src.chunking import chunk_text
from src.embeddings import generate_embeddings
from src.vector_store import store_documents

PDF_PATH = "data/resume.pdf"


def ingest_resume():

    print("Loading PDF...")

    text = load_pdf(PDF_PATH)

    print(f"Loaded {len(text)} characters.")

    print("Chunking...")

    chunks = chunk_text(
        text,
        chunk_size=1200,
        overlap=100
    )

    print(f"Created {len(chunks)} chunks.")

    documents = [
        chunk["text"]
        for chunk in chunks
    ]

    print("Generating embeddings...")

    embeddings = generate_embeddings(documents)

    print(
        f"Embedding dimension: "
        f"{len(embeddings[0])}"
    )

    print("Storing in ChromaDB...")

    ids = store_documents(
        chunks,
        embeddings
    )

    print(f"Stored {len(ids)} documents.")


if __name__ == "__main__":
    ingest_resume()