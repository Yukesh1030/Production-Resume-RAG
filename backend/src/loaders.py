from pathlib import Path
from pypdf import PdfReader

def load_pdf(file_path: str) -> str:
    """
    Extracts text from a PDF file.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    reader = PdfReader(str(path))

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)
    return '\n'.join(pages)