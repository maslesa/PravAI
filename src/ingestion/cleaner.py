import re
from .extractor import ExtractedPage


def normalize_whitespace(text: str) -> str:
    text = text.replace('\xa0', ' ')
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def clean_page_text(text: str) -> str:
    return normalize_whitespace(text)


def clean_document_text(pages: list[ExtractedPage]) -> list[ExtractedPage]:
    cleaned_pages = []

    for page in pages:
        cleaned_text = clean_page_text(page.text)
        cleaned_pages.append(ExtractedPage(page.page_number, cleaned_text))

    return cleaned_pages