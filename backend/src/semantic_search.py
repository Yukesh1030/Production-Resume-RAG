import chromadb

from src.embeddings import model


CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "resume_documents"


client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_collection(
    name=COLLECTION_NAME
)


def semantic_search(
    query: str,
    top_k: int = 5
):

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k,
        include=[
            "documents",
            "distances",
            "metadatas"
        ]
    )

    documents = results["documents"][0]
    distances = results["distances"][0]
    ids = results["ids"][0]
    metadatas = results["metadatas"][0]

    output = []

    for rank, (
        doc_id,
        document,
        distance,
        metadata
    ) in enumerate(
        zip(
            ids,
            documents,
            distances,
            metadatas
        ),
        start=1
    ):

        output.append({

            "id": doc_id,

            "document": document,

            "distance": float(distance),

            "metadata": metadata,

            "rank": rank

        })

    return output