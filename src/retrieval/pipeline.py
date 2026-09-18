from src.embeddings.chroma import ChromaStore
from src.embeddings.model import EmbeddingModel
from .reranker import CrossEncoderReranker
from .search import SemanticRetriever


def run_retrieval(query: str, strategy: str = 'legal', top_k: int = 5, chroma_path: str = 'data/chroma'):
    embedding_model = EmbeddingModel()
    chroma_store = ChromaStore(path=chroma_path)

    retriever = SemanticRetriever(
        embedding_model=embedding_model,
        chroma_store=chroma_store,
    )

    results = retriever.search(
        query=query,
        strategy=strategy,
        top_k=top_k,
    )

    print('\n' + '=' * 50)
    print(f'Query: {query}')
    print(f'Strategy: {strategy}')
    print(f'Results: {len(results)}')
    print('=' * 50)

    for index, result in enumerate(results, start=1):
        print(f'\n[{index}]')
        print(f'Chunk ID: {result.chunk_id}')
        print(f'Similarity: {result.similarity:.4f}')
        print(f'Distance: {result.distance:.4f}')
        print(f'Document: {result.metadata.get('document_title')}')
        print(f'Article: {result.metadata.get('article')}')
        print('-' * 50)
        print(result.text)


def run_reranked_retrieval(
    query: str,
    strategy: str = 'legal',
    initial_top_k: int = 20,
    final_top_k: int = 5
):
    embedding_model = EmbeddingModel()
    chroma_store = ChromaStore()
    retriever = SemanticRetriever(embedding_model, chroma_store)
    reranker = CrossEncoderReranker()

    initial_results = retriever.search(query=query, strategy=strategy, top_k=initial_top_k)

    reranked_results = reranker.rerank(query=query, results=initial_results, top_k=final_top_k)

    return reranked_results