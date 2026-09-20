from .pipeline import create_generation_pipeline, run_generation


QUESTION = 'Da li poslodavac može da otkaže ugovor o radu zaposlenom?'


def main():
    print('Initializing PravAI generation pipeline...\n')

    hybrid_retriever, reranker, generator = create_generation_pipeline(llm_model='qwen3:8b')

    print(f'Question: {QUESTION}\n')
    print('Retrieving legal context...')

    result = run_generation(
        question=QUESTION,
        hybrid_retriever=hybrid_retriever,
        reranker=reranker,
        generator=generator,
        initial_top_k=20,
        final_top_k=5
    )

    print('\n' + '=' * 80)
    print('ANSWER')
    print('-' * 80)
    print(result.answer)

    print('\n' + '=' * 80)
    print('CITATIONS')
    print('-' * 80)
    if result.citations:
        for citation in result.citations:
            print(f'- {citation.law}, član {citation.article}')
    else:
        print('No valid citations.')

    print('\n' + '=' * 80)
    print('GROUNDED')
    print('-' * 80)
    print(result.grounded)


if __name__ == '__main__':
    main()