import chromadb


CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "resume_documents"


client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


def store_documents(chunks, embeddings):

    ids = [
        f"resume_chunk_{chunk['chunk_index']}"
        for chunk in chunks
    ]

    documents = [
        chunk["text"]
        for chunk in chunks
    ]

    metadatas = [
        {
            "source": "resume.pdf",
            "chunk_index": chunk["chunk_index"]
        }
        for chunk in chunks
    ]

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    return ids


# import chromadb

# CHROMA_PATH = './chroma_db'

# collection_name = 'resume_documents'

# client = chromadb.PersistentClient(path=CHROMA_PATH)

# collection = client.get_or_create_collection(name=collection_name)

# def store_documents(documents,embeddings):
#     ids =[f"resume_chunk_{index}" for index in range(len(documents))]

#     collection.add(ids=ids,documents=documents,embeddings=embeddings.tolist())

#     return ids

