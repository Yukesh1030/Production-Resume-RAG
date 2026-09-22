import chromadb


CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "resume_documents"


client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_collection(
    name=COLLECTION_NAME
)


def get_all_documents():

    results = collection.get(
        include=[
            "documents",
            "metadatas"
        ]
    )

    return (
        results["ids"],
        results["documents"],
        results["metadatas"]
    )