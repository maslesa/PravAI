import json
from dataclasses import asdict
from pathlib import Path

from .cleaner import clean_document_text
from .extractor import extract_text_from_document
from .loader import load_pdf
from .metadata import create_document_metadata
from .parser import parse_document


def save_extracted_text(pages, output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding='utf-8') as file:
        for page in pages:
            file.write(f'===== PAGE {page.page_number} =====\n\n')
            file.write(page.text)
            file.write("\n\n")


def save_parsed_document(document, output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding='utf-8') as file:
        json.dump(
            asdict(document),
            file,
            ensure_ascii=False,
            indent=2,
        )


def process_pdf(
        pdf_path: str | Path,
        title: str,
        extracted_output_dir: str | Path,
        document_output_dir: str | Path,
        source_url: str | None = None
):
    pdf_path = Path(pdf_path)
    document = load_pdf(pdf_path)

    try:
        pages = extract_text_from_document(document)
        pages = clean_document_text(pages)

        metadata = create_document_metadata(
            pdf_path=pdf_path,
            title=title,
            source_url=source_url,
        )

        extracted_output_path = Path(extracted_output_dir) / f'{pdf_path.stem}.txt'
        save_extracted_text(pages, extracted_output_path)

        legal_document = parse_document(pages, asdict(metadata))
        document_output_path = Path(document_output_dir) / f'{pdf_path.stem}.json'
        save_parsed_document(legal_document, document_output_path)

        return legal_document

    finally:
        document.close()


def process_directory(
        input_dir: str | Path,
        extracted_output_dir: str | Path,
        document_output_dir: str | Path,
):
    input_dir = Path(input_dir)

    if not input_dir.exists():
        raise FileNotFoundError(f'Input directory {input_dir} does not exist')

    pdf_files = sorted(input_dir.glob('*.pdf'))

    if not pdf_files:
        raise FileNotFoundError(f'No PDF files found in input directory {input_dir}')

    print(f'Found {len(pdf_files)} PDF files.\n')

    for index, pdf_path in enumerate(pdf_files, start=1):
        print(f'[{index}/{len(pdf_files)}] Processing: {pdf_path.name}')

        title = pdf_path.stem.replace('_', ' ')

        process_pdf(pdf_path, title, extracted_output_dir, document_output_dir)

        print('\tCompleted!\n')

    print('All documents processed successfully.')