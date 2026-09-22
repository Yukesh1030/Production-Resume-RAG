#Added with proper metadata and chunk index for each chunk
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100):
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0:
        raise ValueError("overlap cannot be negative")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []

    start = 0
    chunk_index = 0

    while start < len(text):

        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append({
                "chunk_index": chunk_index,
                "text": chunk
            })

            chunk_index += 1

        start += chunk_size - overlap

    return chunks



# def chunk_text(
#     text: str,
#     chunk_size: int = 500,
#     overlap: int = 100
# ):
#     """
#     Split text into overlapping chunks.
#     """

#     if chunk_size <= 0:
#         raise ValueError(
#             "chunk_size must be greater than 0"
#         )

#     if overlap < 0:
#         raise ValueError(
#             "overlap cannot be negative"
#         )

#     if overlap >= chunk_size:
#         raise ValueError(
#             "overlap must be smaller than chunk_size"
#         )

#     chunks = []

#     start = 0

#     while start < len(text):

#         end = start + chunk_size

#         chunk = text[start:end].strip()

#         if chunk:
#             chunks.append(chunk)

#         start += chunk_size - overlap

#     return chunks