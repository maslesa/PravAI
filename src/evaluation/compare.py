import json
from pathlib import Path


BASELINE_PATH = Path('data/evaluation/legal_results.json')
RERANKER_PATH = Path('data/evaluation/legal_reranker_results.json')


def load_results(path: Path):
    with path.open('r', encoding='utf-8') as file:
        return json.load(file)


def calculate_metrics(results: list[dict]) -> dict:
    total = len(results)

    recall_at_1 = sum(result['hit_at_1'] for result in results) / total
    recall_at_3 = sum(result['hit_at_3'] for result in results) / total
    recall_at_5 = sum(result['hit_at_5'] for result in results) / total
    mrr = sum(result['reciprocal_rank'] for result in results) / total

    return {
        'Recall@1': recall_at_1,
        'Recall@3': recall_at_3,
        'Recall@5': recall_at_5,
        'MRR': mrr,
    }


def calculate_delta(baseline: dict, reranker: dict) -> dict:
    return {metric: reranker[metric] - baseline[metric] for metric in baseline}


def print_comparison(baseline: dict, reranker: dict):
    delta = calculate_delta(baseline, reranker)

    print(
        f'{'Metric':<12}'
        f'{'Baseline':>12}'
        f'{'Reranker':>12}'
        f'{'Delta':>12}'
    )
    print("-" * 50)

    for metric in baseline:
        print(
            f'{metric:<12}'
            f'{baseline[metric]:>12.4f}'
            f'{reranker[metric]:>12.4f}'
            f'{delta[metric]:>+12.4f}'
        )


def main():
    baseline_results = load_results(BASELINE_PATH)
    reranker_results = load_results(RERANKER_PATH)

    if len(baseline_results) != len(reranker_results):
        raise ValueError('Baseline and reranker results must have same length.')

    baseline_metrics = calculate_metrics(baseline_results)
    reranker_metrics = calculate_metrics(reranker_results)

    print('\nRetrieval comparison')
    print('=' * 50 + '\n')
    print_comparison(baseline_metrics, reranker_metrics)


if __name__ == '__main__':
    main()