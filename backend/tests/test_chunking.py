from src.loaders import load_pdf
from src.chunking import chunk_text


text = load_pdf("data/resume.pdf")


chunks = chunk_text(
    text,
    chunk_size=500,
    overlap=100
)


print("Total chunks:", len(chunks))


for index, chunk in enumerate(chunks):

    print("\n" + "=" * 60)

    print("Chunk:", index)

    print("=" * 60)

    print(chunk)