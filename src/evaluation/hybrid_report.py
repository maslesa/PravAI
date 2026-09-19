import json
from pathlib import Path


RESULTS = {
    'Semantic': Path('data/evaluation/hybrid_phase_semantic_results.json'),
    'BM25': Path('data/evaluation/bm25_results.json'),
    'Hybrid': Path('data/evaluation/hybrid_results.json'),
    'Hybrid + Reranker': Path('data/evaluation/hybrid_reranker_results.json'),
}

def load_results(path: Path) -> list[dict]:
    with path.open('r', encoding='utf-8') as file:
        return json.load(file)


def calculate_metrics(results: list[dict]) -> dict:
    total = len(results)

    return {
        'Recall@1': sum(result['hit_at_1'] for result in results) / total,
        'Recall@3': sum(result['hit_at_3'] for result in results) / total,
        'Recall@5': sum(result['hit_at_5'] for result in results) / total,
        'MRR': sum(result['reciprocal_rank'] for result in results) / total,
    }


def main():
    all_metrics = {}

    for name, path in RESULTS.items():
        results = load_results(path)

        all_metrics[name] = calculate_metrics(results)

    print('\nHybrid search evaluation')
    print('=' * 80)
    print(
        f'{'System':<22}'
        f'{'Recall@1':>12}'
        f'{'Recall@3':>12}'
        f'{'Recall@5':>12}'
        f'{'MRR':>12}'
    )
    print('-' * 80)
    for name, metrics in all_metrics.items():
        print(
            f'{name:<22}'
            f'{metrics['Recall@1']:>12.4f}'
            f'{metrics['Recall@3']:>12.4f}'
            f'{metrics['Recall@5']:>12.4f}'
            f'{metrics['MRR']:>12.4f}'
        )


if __name__ == '__main__':
    main()