from dataclasses import dataclass


@dataclass
class EvaluationQuestion:
    question_id: str
    question: str
    expected_document: str
    expected_articles: list[str]


@dataclass
class QuestionEvaluation:
    question_id: str
    strategy: str
    top_k: int
    hit: bool
    first_relevant_rank: int | None
    results: list[dict]


@dataclass
class EvaluationSummary:
    strategy: str
    total_questions: int
    recall_at_1: float
    recall_at_3: float
    recall_at_5: float
    mrr: float