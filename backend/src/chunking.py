import re


def clean_text(text: str) -> str:
    """
    Clean extracted PDF text while preserving
    meaningful structure.
    """

    # Normalize different whitespace characters
    text = text.replace("\u00a0", " ")

    # Normalize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove excessive spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def split_into_sections(text: str):
    """
    Split resume text into logical sections.

    The function keeps section headings with
    the content that follows them.
    """

    text = clean_text(text)

    section_patterns = [
        r"Technical Skills",
        r"Software Engineering Projects",
        r"Achievements",
        r"Education",
        r"Experience",
        r"Internship"
    ]

    pattern = "(" + "|".join(section_patterns) + ")"

    parts = re.split(
        pattern,
        text,
        flags=re.IGNORECASE
    )

    sections = []

    current_section = ""

    for part in parts:

        part = part.strip()

        if not part:
            continue

        if re.fullmatch(
            pattern,
            part,
            flags=re.IGNORECASE
        ):
            current_section = part
            continue

        if current_section:
            sections.append(
                f"{current_section}\n{part}"
            )

            current_section = ""

        else:
            sections.append(part)

    return sections


def chunk_text(
    text: str,
    chunk_size: int = 1200,
    overlap: int = 100
):
    """
    Create structure-aware chunks.

    Sections are preserved first.
    Large sections are split into smaller
    overlapping chunks.
    """

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than 0"
        )

    if overlap < 0:
        raise ValueError(
            "overlap cannot be negative"
        )

    if overlap >= chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size"
        )

    sections = split_into_sections(text)

    chunks = []
    chunk_index = 0

    for section in sections:

        # Keep small logical sections together
        if len(section) <= chunk_size:

            chunks.append({
                "chunk_index": chunk_index,
                "text": section.strip()
            })

            chunk_index += 1

            continue

        # Split large sections
        start = 0

        while start < len(section):

            end = start + chunk_size

            chunk = section[start:end].strip()

            if chunk:

                chunks.append({
                    "chunk_index": chunk_index,
                    "text": chunk
                })

                chunk_index += 1

            start += chunk_size - overlap

    return chunks