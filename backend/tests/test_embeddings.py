from src.embeddings import generate_embeddings


texts = [
    "Yukesh is a React developer.",
    "Yukesh works with artificial intelligence.",
    "Yukesh has experience with Java."
]


embeddings = generate_embeddings(texts)


print("Number of embeddings:", len(embeddings))

print(
    "Embedding dimension:",
    len(embeddings[0])
)


for index, embedding in enumerate(embeddings):

    print(
        f"\nText {index + 1}"
    )

    print(
        "First 5 values:",
        embedding[:5]
    )