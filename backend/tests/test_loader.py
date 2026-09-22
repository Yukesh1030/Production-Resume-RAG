from src.loaders import load_pdf

PDF_PATH = 'data/resume.pdf'

text = load_pdf(PDF_PATH)

print("Character count:", len(text))
print("\n--- Resume Preview ---\n")

print(text[:2000])  # Print the first 2000 characters of the extracted text