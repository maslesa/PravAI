import json
from dataclasses import asdict
from pathlib import Path
from src.ingestion.parser import LegalDocument, Chapter, Article, Paragraph, Item
from .fixed import fixed_size_chunks
from .models import Chunk
from .recursive import recursive_chunks
from .legal import legal_chunks


def load_document(path: str | Path) -> LegalDocument:
    path = Path(path)

    with path.open('r', encoding='utf-8') as file:
        data = json.load(file)

    chapters = []

    for chapter_data in data['chapters']:
        articles = []

        for article_data in chapter_data['articles']:
            paragraphs = []

            for paragraph_data in article_data['paragraphs']:
                items = [Item(number=item['number'], text=item['text']) for item in paragraph_data['items']]

                paragraphs.append(Paragraph(
                    number=paragraph_data['number'],
                    text=paragraph_data['text'],
                    items=items
                ))

            articles.append(Article(
                number=article_data['number'],
                title=article_data['title'],
                paragraphs=paragraphs,
                raw_text=article_data['raw_text'],
            ))

        chapters.append(Chapter(
            number=chapter_data['number'],
            title=chapter_data['title'],
            articles=articles,
        ))

    return LegalDocument(metadata=data['metadata'], chapters=chapters)


def document_to_text(document: LegalDocument) -> str:
    parts = []

    for chapter in document.chapters:
        for article in chapter.articles:
            parts.append(f'Član {article.number}.\n\n{article.raw_text}')

    return '\n\n'.join(parts)


def create_text_chunks(document: LegalDocument, strategy: str, chunk_size: int, chunk_overlap: int) -> list[Chunk]:

    text = document_to_text(document)

    if strategy == 'fixed':
        texts = fixed_size_chunks(text, chunk_size, chunk_overlap)

    elif strategy == 'recursive':
        texts = recursive_chunks(text, chunk_size, chunk_overlap)

    else:
        raise ValueError(f'Invalid chunking strategy {strategy}')

    chunks = []

    for index, chunk_text in enumerate(texts):
        chunks.append(Chunk(
            chunk_id=f'{document.metadata['document_id']}_{strategy}_{index}',
            text=chunk_text,
            metadata={
                "document_id": document.metadata["document_id"],
                "document_title": document.metadata["title"],
                "document_type": document.metadata["document_type"],
                "language": document.metadata["language"],
                "chunking_strategy": strategy,
                "chunk_index": index,
            }
        ))

    return chunks


def save_chunks(chunks: list[Chunk], output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open('w', encoding='utf-8') as file:
        for chunk in chunks:
            file.write(json.dumps(asdict(chunk), ensure_ascii=False) + '\n')


def process_document(
        document_path: str | Path,
        output_dir: str | Path,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        legal_max_chunk_size: int = 1000,
) -> None:

    document = load_document(document_path)
    output_dir = Path(output_dir)

    for strategy in ['fixed', 'recursive']:
        chunks = create_text_chunks(document, strategy, chunk_size, chunk_overlap)
        output_path = output_dir / strategy / f'{document.metadata['document_id']}.jsonl'
        save_chunks(chunks, output_path)

    legal = legal_chunks(document, legal_max_chunk_size)

    save_chunks(legal, output_path=output_dir / 'legal' / f'{document.metadata["document_id"]}.jsonl')


def process_all_documents(
        input_dir: str | Path,
        output_dir: str | Path,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        legal_max_chunk_size: int = 1000,
) -> None:

    input_dir = Path(input_dir)

    document_files = sorted(input_dir.glob('*.json'))

    if not document_files:
        raise FileNotFoundError(f'No JSON documents found in {input_dir}')

    print(f'Found {len(document_files)} documents.\n')

    for index, document_path in enumerate(document_files, start=1):
        print(f'[{index}/{len(document_files)}] {document_path.name}')

        process_document(document_path, output_dir, chunk_size, chunk_overlap, legal_max_chunk_size)
        print('\tCompleted!\n')

    print(f'All documents chunked successfully.')