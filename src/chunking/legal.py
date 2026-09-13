from .models import Chunk
from src.ingestion.parser import LegalDocument, Article, Paragraph


def legal_chunks(document: LegalDocument, max_chunk_size: int = 2000) -> list[Chunk]:
    chunks = []

    for chapter in document.chapters:
        for article in chapter.articles:
            article_chunks = _chunk_article(document, chapter.number, article, max_chunk_size)
            chunks.extend(article_chunks)

    return chunks


def _chunk_article(document: LegalDocument, chapter_number: str, article: Article, max_chunk_size: int) -> list[Chunk]:

    article_text = _build_article_text(article)

    metadata = {
        'document_id': document.metadata['document_id'],
        'document_title': document.metadata['title'],
        'document_type': document.metadata['document_type'],
        'language': document.metadata['language'],
        'chapter': chapter_number,
        'article': article.number,
        'chunking_strategy': 'legal'
    }

    if len(article_text) <= max_chunk_size:
        return [Chunk(
            chunk_id=f'{document.metadata['document_id']}_article_{article.number}',
            text=article_text,
            metadata=metadata,
        )]

    return _split_large_article(document, article, metadata, max_chunk_size)



def _build_article_text(article: Article) -> str:

    parts = [f'Član {article.number}.']

    if article.title:
        parts.append(article.title)

    if article.paragraphs:
        for paragraph in article.paragraphs:
            paragraph_text = (
                f'({paragraph.number}) '
                f'{paragraph.text}'
            )
            parts.append(paragraph_text)
    else:
        parts.append(article.raw_text)

    return '\n\n'.join(parts).strip()


def _split_large_article(document: LegalDocument, article: Article, metadata: dict, max_chunk_size: int) -> list[Chunk]:
    chunks = []
    current_parts = []
    current_size = 0

    for paragraph in article.paragraphs:
        paragraph_text = (
            f'({paragraph.number}) '
            f'{paragraph.text}'
        )

        paragraph_size = len(paragraph_text)

        if current_parts and current_size + paragraph_size > max_chunk_size:
            chunk_number = len(chunks) + 1
            chunks.append(Chunk(
                chunk_id=f'{document.metadata['document_id']}_article_{article.number}_part_{chunk_number}',
                text=f'Član {article.number}.\n\n' + '\n\n'.join(current_parts),
                metadata={**metadata, 'chunk_part': chunk_number},
            ))

            current_parts = []
            current_size = 0

        current_parts.append(paragraph_text)
        current_size += paragraph_size

    if current_parts:
        chunk_number = len(chunks) + 1
        chunks.append(Chunk(
            chunk_id=f'{document.metadata['document_id']}_article_{article.number}_part_{chunk_number}',
            text=f'Član {article.number}.\n\n' + '\n\n'.join(current_parts),
            metadata={**metadata, 'chunk_part': chunk_number},
        ))

    return chunks