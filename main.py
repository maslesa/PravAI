from src.ingestion.pipeline import process_directory
from src.chunking.pipeline import process_all_documents

# process_directory(
#     input_dir='data/raw/laws',
#     extracted_output_dir='data/processed/extracted',
#     document_output_dir='data/processed/documents',
# )

process_all_documents(
    input_dir='data/processed/documents',
    output_dir='data/processed/chunks',
    chunk_size=1000,
    chunk_overlap=200,
    legal_max_chunk_size=2000
)