from src.corpus import get_all_documents
from src.keyword_search import BM25Retriever


document_ids, documents = get_all_documents()


print(
    "Documents loaded:",
    len(documents)
)


retriever = BM25Retriever(
    document_ids,
    documents
)


query = "What technologies does Yukesh know?"


results = retriever.search(
    query,
    top_k=5
)


for result in results:

    print("\nRank:", result["rank"])

    print("ID:", result["id"])

    print(
        "BM25 Score:",
        round(result["score"], 4)
    )

    print("Document:")

    print(result["document"])