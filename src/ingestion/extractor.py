import pymupdf
from dataclasses import dataclass


@dataclass
class ExtractedPage:
    page_number: int
    text: str


def extract_text_from_page(page: pymupdf.Page) -> str:
    return page.get_text('text')


def extract_text_from_document(document: pymupdf.Document) -> list[ExtractedPage]:
    pages = []

    for page_number, page in enumerate(document, start=1):
        text = extract_text_from_page(page)
        pages.append(ExtractedPage(page_number, text))

    return pages