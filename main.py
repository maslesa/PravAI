from src.ingestion.pipeline import process_directory

process_directory(
    input_dir='data/raw/laws',
    extracted_output_dir='data/processed/extracted',
    document_output_dir='data/processed/documents',
)