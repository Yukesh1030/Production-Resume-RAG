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
        chunk_size=500,
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
        f"Embedding dimension: {len(embeddings[0])}"
    )

    print("Storing in ChromaDB...")

    ids = store_documents(
        chunks,
        embeddings
    )

    print(f"Stored {len(ids)} documents.")


if __name__ == "__main__":
    ingest_resume()


# from src.loaders import load_pdf
# from src.chunking import chunk_text
# from src.embeddings import generate_embeddings
# from src.vector_store import store_documents

# PDF_PATH = "data/resume.pdf"

# def ingest_pdf():
#     print("loading PDF...")

#     text = load_pdf(PDF_PATH)
#     print(f"PDF loaded. Length of text: {len(text)} characters.")

#     print("chunking text...")
#     chunks = chunk_text(text)
#     print(f"Text chunked into {len(chunks)} chunks.")

#     print("generating embeddings...")
#     embeddings = generate_embeddings(chunks)
#     print(f"Embeddings generated. Shape: {len(embeddings)} x {len(embeddings[0])}")

#     print("storing documents and embeddings in vector store...")
#     ids = store_documents(chunks, embeddings)
#     print(f"Documents and embeddings stored with IDs: {ids}")

# if __name__ == "__main__": #Becoz this file is being run directly, not imported
#     ingest_pdf() #for testing purposes, we can run this script directly to ingest the PDF and store the embeddings.