from src.embeddings.chroma import ChromaStore
from src.embeddings.model import EmbeddingModel
from src.retrieval.search import SemanticRetriever
from .dataset import load_evaluation_questions
from .metrics import first_relevant_rank, hit_at_k, reciprocal_rank
from .models import EvaluationSummary


STRATEGIES = ['fixed', 'recursive', 'legal']


def evaluate_strategy(retriever: SemanticRetriever, questions, strategy: str) -> EvaluationSummary:
    total_questions = len(questions)

    hits_at_1 = 0
    hits_at_3 = 0
    hits_at_5 = 0
    reciprocal_ranks = []

    for index, item in enumerate(questions, start=1):
        print(f'[{strategy}] Question {index}/{total_questions}')

        search_results = retriever.search(query=item.question, strategy=strategy, top_k=5)

        results = [
            {
                'chunk_id': result.chunk_id,
                'text': result.text,
                'metadata': result.metadata,
                'distance': result.distance,
            }
            for result in search_results
        ]

        if hit_at_k(results, item.expected_document, item.expected_articles, 1):
            hits_at_1 += 1

        if hit_at_k(results, item.expected_document, item.expected_articles, 3):
            hits_at_3 += 1

        if hit_at_k(results, item.expected_document, item.expected_articles, 5):
            hits_at_5 += 1


        reciprocal_ranks.append(reciprocal_rank(
            results,
            item.expected_document,
            item.expected_articles,
        ))

    return EvaluationSummary(
        strategy=strategy,
        total_questions=total_questions,
        recall_at_1=hits_at_1 / total_questions,
        recall_at_3=hits_at_3 / total_questions,
        recall_at_5=hits_at_5 / total_questions,
        mrr=sum(reciprocal_ranks) / total_questions
    )


def evaluate_all_strategies(dataset_path: str, chroma_path: str = 'data/chroma') -> list[EvaluationSummary]:
    questions = load_evaluation_questions(dataset_path)

    embedding_model = EmbeddingModel()
    chroma_store = ChromaStore(chroma_path)
    retriever = SemanticRetriever(embedding_model, chroma_store)

    summaries = []

    for strategy in STRATEGIES:
        summary = evaluate_strategy(retriever, questions, strategy)
        summaries.append(summary)

    return summaries