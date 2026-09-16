from pathlib import Path
import json
from .models import EvaluationQuestion


def load_evaluation_questions(path: str | Path) -> list[EvaluationQuestion]:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f'Evaluation questions file not found at {path}')

    with path.open('r', encoding='utf-8') as file:
        data = json.load(file)

    questions = []

    for item in data:
        questions.append(EvaluationQuestion(
            question_id=item['id'],
            question=item['question'],
            expected_document=item['expected_document'],
            expected_articles=item['expected_articles'],
        ))

    return questions