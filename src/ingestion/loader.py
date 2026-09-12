import pymupdf
from pathlib import Path


def load_pdf(path: str | Path) -> pymupdf.Document:
    pdf_path = Path(path)

    if not pdf_path.exists():
        raise FileNotFoundError(f'File not found: {pdf_path}')

    if not pdf_path.is_file():
        raise ValueError(f'File not found: {pdf_path}')

    if pdf_path.suffix.lower() != '.pdf':
        raise ValueError(f'File not a PDF: {pdf_path}')

    return pymupdf.open(pdf_path)


def load_pdfs(path: str | Path) -> list[tuple[Path, pymupdf.Document]]:
    directory_path = Path(path)

    if not directory_path.exists():
        raise FileNotFoundError(f'Directory not found: {directory_path}')

    pdf_paths = sorted(directory_path.glob('*.pdf'))

    documents = []
    for pdf_path in pdf_paths:
        document = load_pdf(pdf_path)
        documents.append(tuple((pdf_path, document)))

    return documents