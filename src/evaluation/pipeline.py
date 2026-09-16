from .runner import evaluate_all_strategies


def run_evaluation(
        dataset_path: str = 'data/evaluation/retrieval_questions.json',
        chroma_path: str = 'data/chroma'
):
    summaries = evaluate_all_strategies(dataset_path, chroma_path)

    print('\n' + '=' * 80)
    print('Retrieval results')
    print('=' * 80)

    print(
        f'{'Strategy':<15}'
        f'{'Recall@1':<15}'
        f'{'Recall@3':<15}'
        f'{'Recall@5':<15}'
        f'{'MRR':<15}'
    )
    print('-' * 80)

    for summary in summaries:
        print(
            f'{summary.strategy:<15}'
            f'{summary.recall_at_1:<15.4f}'
            f'{summary.recall_at_3:<15.4f}'
            f'{summary.recall_at_5:<15.4f}'
            f'{summary.mrr:<15.4f}'
        )
    print('=' * 80)

    return summaries