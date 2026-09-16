import json
from pathlib import Path
from src.embeddings.chroma import ChromaStore
from src.embeddings.model import EmbeddingModel
from src.retrieval.search import SemanticRetriever
from .dataset import load_evaluation_questions
from .metrics import first_relevant_rank, hit_at_k, reciprocal_rank
from .models import EvaluationSummary


STRATEGIES = ['fixed', 'recursive', 'legal']


def evaluate_question(retriever: SemanticRetriever, item, strategy: str) -> dict:
    search_results = retriever.search(query=item.question, strategy=strategy, top_k=5)

    results =[
        {
            'rank': index + 1,
            'chunk_id': result.chunk_id,
            'text': result.text,
            'metadata': result.metadata,
            'distance': result.distance,
            'similarity': result.similarity,
        }
        for index, result in enumerate(search_results)
    ]

    return {
        "question_id": item.question_id,
        "question": item.question,
        "strategy": strategy,
        "expected_document": item.expected_document,
        "expected_articles": item.expected_articles,
        "first_relevant_rank": first_relevant_rank(results, item.expected_document, item.expected_articles),
        "hit_at_1": hit_at_k(results, item.expected_document, item.expected_articles, 1),
        "hit_at_3": hit_at_k(results, item.expected_document, item.expected_articles, 3),
        "hit_at_5": hit_at_k(results, item.expected_document, item.expected_articles, 5),
        "reciprocal_rank": reciprocal_rank(results, item.expected_document, item.expected_articles),
        "results": results,
    }


def evaluate_strategy(retriever: SemanticRetriever, questions, strategy: str):
    evaluations = []

    for index, item in enumerate(questions, start=1):
        print(f'[{strategy}] Question {index}/{len(questions)}')

        evaluation = evaluate_question(retriever, item, strategy)
        evaluations.append(evaluation)

    total = len(evaluations)

    recall_at_1 = sum(item['hit_at_1'] for item in evaluations) / total
    recall_at_3 = sum(item['hit_at_3'] for item in evaluations) / total
    recall_at_5 = sum(item['hit_at_5'] for item in evaluations) / total
    mrr = sum(item['reciprocal_rank'] for item in evaluations) / total

    summary = EvaluationSummary(
        strategy=strategy,
        total_questions=total,
        recall_at_1=recall_at_1,
        recall_at_3=recall_at_3,
        recall_at_5=recall_at_5,
        mrr=mrr,
    )

    return summary, evaluations


def save_evaluation_results(evaluations: list[dict], output_path: str | Path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open('w', encoding='utf-8') as file:
        json.dump(evaluations, file, ensure_ascii=False, indent=2)

    print(f'\tSaved evaluation results to {output_path}')


def evaluate_all_strategies(dataset_path: str, chroma_path: str = 'data/chroma', output_dir: str = 'data/evaluation'):
    questions = load_evaluation_questions(dataset_path)

    embedding_model = EmbeddingModel()
    chroma_store = ChromaStore(chroma_path)
    retriever = SemanticRetriever(embedding_model, chroma_store)

    summaries = []

    for strategy in STRATEGIES:
        summary, evaluations = evaluate_strategy(retriever, questions, strategy)
        summaries.append(summary)

        output_path = Path(output_dir) / f'{strategy}_results.json'
        save_evaluation_results(evaluations, output_path)

    return summaries