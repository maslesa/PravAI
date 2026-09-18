from src.ingestion.pipeline import process_directory
from src.chunking.pipeline import process_all_documents
from src.embeddings.pipeline import run_embedding_pipeline
from src.evaluation.pipeline import run_evaluation
# from src.evaluation.reranker_runner import run_evaluation


process_directory(
    input_dir='data/raw/laws',
    extracted_output_dir='data/processed/extracted',
    document_output_dir='data/processed/documents',
)


process_all_documents(
    input_dir='data/processed/documents',
    output_dir='data/processed/chunks',
    chunk_size=1000,
    chunk_overlap=200,
    legal_max_chunk_size=2000
)


run_embedding_pipeline(
    chunks_dir='data/processed/chunks',
    chroma_path='data/chroma'
)


run_evaluation(
    dataset_path='data/evaluation/retrieval_questions.json',
    chroma_path='data/chroma'
)


# function for rerank pipeline call
# run_evaluation(
#     initial_top_k=20,
#     final_top_k=5
# )