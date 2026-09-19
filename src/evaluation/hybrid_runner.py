import json
from pathlib import Path
from src.embeddings.chroma import ChromaStore
from src.embeddings.model import EmbeddingModel
from src.retrieval.bm25 import BM25Retriever
from src.retrieval.hybrid import HybridRetriever
from src.retrieval.reranker import CrossEncoderReranker
from src.retrieval.search import SemanticRetriever
from .metrics import first_relevant_rank, hit_at_k, reciprocal_rank


QUESTIONS_PATH = Path('data/evaluation/retrieval_questions.json')
OUTPUT_DIR = Path('data/evaluation')


def load_questions() -> list[dict]:
    with QUESTIONS_PATH.open('r', encoding='utf-8') as file:
        return json.load(file)


def serialize_results(results):
    serialized = []

    for rank, result in enumerate(results, start=1):
        serialized.append({
            'rank': rank,
            'chunk_id': result.chunk_id,
            'text': result.text,
            'metadata': result.metadata,
            'distance': result.distance,
            'similarity': result.similarity,
            'bm25_score': result.bm25_score,
            'hybrid_score': result.hybrid_score,
            'reranker_score': result.reranker_score,
        })

    return serialized


def evaluate_retrieval(questions: list[dict], retrieval_function, retrieval_type: str):
    evaluation_results = []

    for index, question in enumerate(questions, start=1):
        print(f'[{retrieval_type}] Question {index}/{len(questions)}')

        results = retrieval_function(question['question'])
        expected_document = question['expected_document']
        expected_articles = [str(article) for article in question['expected_articles']]

        rank = first_relevant_rank(results, expected_document, expected_articles)

        evaluation_results.append({
            'question_id': question['id'],
            'question': question['question'],
            'retrieval_type': retrieval_type,
            'expected_document': expected_document,
            'expected_articles': expected_articles,
            'first_relevant_rank': rank,
            'hit_at_1': hit_at_k(results, expected_document, expected_articles, 1),
            'hit_at_3': hit_at_k(results, expected_document, expected_articles, 3),
            'hit_at_5': hit_at_k(results, expected_document, expected_articles, 5),
            'reciprocal_rank': reciprocal_rank(results, expected_document, expected_articles),
            'results': serialize_results(results),
        })

    return evaluation_results


def save_results(results: list[dict], filename: str):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / filename

    with output_path.open('w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=2)

    print(f'Saved results to {output_path}')