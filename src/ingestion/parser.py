import re
from dataclasses import dataclass, field
from .extractor import ExtractedPage

@dataclass
class Item:
    number: str
    text: str


@dataclass
class Paragraph:
    number: int
    text: str
    items: list[Item] = field(default_factory=list)

@dataclass
class Article:
    number: str
    title: str | None
    paragraphs: list[Paragraph] = field(default_factory=list)
    raw_text: str = ""


@dataclass
class Chapter:
    number: str
    title: str
    articles: list[Article] = field(default_factory=list)


@dataclass
class LegalDocument:
    metadata: dict
    chapters: list[Chapter] = field(default_factory=list)


ARTICLE_PATTERN = re.compile(r"(?mi)^\s*Члан\s+([0-9]+[а-яА-Я]?)\.?\s*$")
PARAGRAPH_PATTERN = re.compile(r"(?m)^\s*\((\d+)\)\s*(.*?)(?=\n\s*\(\d+\)|\Z)", re.DOTALL)
ITEM_PATTERN = re.compile(r"(?m)^\s*(\d+)\)\s*(.*?)(?=\n\s*\d+\)|\Z)", re.DOTALL)
CHAPTER_PATTERN = re.compile(r"(?mi)^\s*ГЛАВА\s+(.+?)\.?\s*$")


def combine_pages(pages: list[ExtractedPage]) -> str:
    return '\n\n'.join(page.text for page in pages if page.text.strip())


def parse_paragraphs(text: str) -> list[Paragraph]:
    paragraphs = []

    matches = list(PARAGRAPH_PATTERN.finditer(text))

    for match in matches:
        number = int(match.group(1))
        paragraph_text = match.group(2).strip()

        items = []

        for item_match in ITEM_PATTERN.finditer(paragraph_text):
            items.append(Item(number=item_match.group(1), text=item_match.group(2).strip()))

        paragraphs.append(
            Paragraph(
                number=number,
                text=paragraph_text,
                items=items
            )
        )

    return paragraphs


def parse_article(article_text: str, article_number: str) -> Article:
    article_text = article_text.strip()

    paragraphs = parse_paragraphs(article_text)

    return Article(
        number=article_number,
        title=None,
        paragraphs=paragraphs,
        raw_text=article_text
    )


def parse_articles(text: str) -> list[Article]:
    matches = list(ARTICLE_PATTERN.finditer(text))

    articles = []

    for index, match in enumerate(matches):
        article_number = match.group(1)
        start = match.end()

        if index + 1 < len(matches):
            end = matches[index + 1].start()
        else:
            end = len(text)

        article_text = text[start:end]

        article = parse_article(article_text, article_number)
        articles.append(article)

    return articles


def parse_chapters(text: str) -> list[Chapter]:
    chapter_matches = list(CHAPTER_PATTERN.finditer(text))

    if not chapter_matches:
        return [
            Chapter(number="", title="", articles=parse_articles(text))
        ]

    chapters = []

    for index, match in enumerate(chapter_matches):
        chapter_number = match.group(1).strip()

        start = match.end()

        if index + 1 < len(chapter_matches):
            end = chapter_matches[index + 1].start()
        else:
            end = len(text)

        chapter_text = text[start:end]

        chapters.append(
            Chapter(
                number=chapter_number,
                title="",
                articles=parse_articles(chapter_text),
            )
        )

    return chapters


def parse_document(pages: list[ExtractedPage], metadata: dict) -> LegalDocument:
    text = combine_pages(pages)
    chapters = parse_chapters(text)

    return LegalDocument(
        metadata=metadata,
        chapters=chapters,
    )