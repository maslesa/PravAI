import json
from pathlib import Path
from src.embeddings.chroma import ChromaStore
from src.embeddings.model import EmbeddingModel
from src.retrieval.reranker import CrossEncoderReranker
from src.retrieval.search import SemanticRetriever


QUESTIONS_PATH = Path('data/evaluation/retrieval_questions.json')
OUTPUT_DIR = Path('data/evaluation')


def load_questions(path: Path) -> list[dict]:
    with path.open('r', encoding='utf-8') as file:
        return json.load(file)


def evaluate_question(
        question: dict,
        retriever: SemanticRetriever,
        reranker: CrossEncoderReranker,
        initial_top_k: int,
        final_top_k: int,
) -> dict:
    query = question['question']
    expected_document = question['expected_document']
    expected_articles = [str(article) for article in question['expected_articles']]

    initial_results = retriever.search(query=query, strategy='legal', top_k=initial_top_k)
    reranked_results = reranker.rerank(query=query, results=initial_results, top_k=final_top_k)

    first_relevant_rank = None

    for rank, result in enumerate(reranked_results, start=1):
        document_id = result.metadata.get('document_id')
        articles = [str(article) for article in result.metadata.get('articles', [])]

        if document_id == expected_document and any(article in expected_articles for article in articles):
            first_relevant_rank = rank
            break

    hit_at_1 = first_relevant_rank is not None and first_relevant_rank <= 1
    hit_at_3 = first_relevant_rank is not None and first_relevant_rank <= 3
    hit_at_5 = first_relevant_rank is not None and first_relevant_rank <= 5
    reciprocal_rank = 1.0 / first_relevant_rank if first_relevant_rank is not None else 0.0

    results = []

    for rank, result in enumerate(reranked_results, start=1):
        results.append(
            {
                'rank': rank,
                'chunk_id': result.chunk_id,
                'text': result.text,
                'metadata': result.metadata,
                'distance': result.distance,
                'similarity': result.similarity,
                'reranker_score': result.reranker_score,
            }
        )

    return {
        'question_id': question['id'],
        'question': query,
        'strategy': 'legal',
        'retrieval_type': 'semantic_plus_reranker',
        'initial_top_k': initial_top_k,
        'final_top_k': final_top_k,
        'expected_document': expected_document,
        'expected_articles': expected_articles,
        'first_relevant_rank': first_relevant_rank,
        'hit_at_1': hit_at_1,
        'hit_at_3': hit_at_3,
        'hit_at_5': hit_at_5,
        'reciprocal_rank': reciprocal_rank,
        'results': results,
    }


def run_evaluation(initial_top_k: int = 20, final_top_k: int = 5):
    questions = load_questions(QUESTIONS_PATH)

    embedding_model = EmbeddingModel()
    chroma_store = ChromaStore()
    retriever = SemanticRetriever(embedding_model, chroma_store)
    reranker = CrossEncoderReranker()

    results = []

    for index, question in enumerate(questions, start=1):
        print(f'Evaluating question {index}/{len(questions)}...')

        result = evaluate_question(question, retriever, reranker, initial_top_k, final_top_k)
        results.append(result)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / 'legal_reranker_results.json'

    with output_path.open('w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)

    print(f'\nResults saved to {output_path}')