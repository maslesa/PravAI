from src.embeddings.chroma import ChromaStore
from src.embeddings.model import EmbeddingModel
from src.retrieval.bm25 import BM25Retriever
from src.retrieval.hybrid import HybridRetriever
from src.retrieval.reranker import CrossEncoderReranker
from src.retrieval.search import SemanticRetriever
from src.evaluation.hybrid_runner import load_questions, evaluate_retrieval, save_results


questions = load_questions()

embedding_model = EmbeddingModel()
chroma_store = ChromaStore()

semantic_retriever = SemanticRetriever(embedding_model, chroma_store)
bm25_retriever = BM25Retriever()

hybrid_retriever = HybridRetriever(semantic_retriever, bm25_retriever)

reranker = CrossEncoderReranker()


def semantic_search(query: str):
    return semantic_retriever.search(query=query, strategy='legal', top_k=5)


def bm25_search(query: str):
    return bm25_retriever.search(query=query, top_k=5)


def hybrid_search(query: str):
    return hybrid_retriever.search(query=query, semantic_top_k=20, bm25_top_k=20, final_top_k=5)


def hybrid_reranked_search(query: str):
    candidates = hybrid_retriever.search(query=query, semantic_top_k=20, bm25_top_k=20, final_top_k=20)
    return reranker.rerank(query=query, results=candidates, top_k=5)


semantic_results = evaluate_retrieval(
    questions=questions,
    retrieval_function=semantic_search,
    retrieval_type='semantic',
)
save_results(semantic_results, 'hybrid_phase_semantic_results.json')


bm25_results = evaluate_retrieval(
    questions=questions,
    retrieval_function=bm25_search,
    retrieval_type='bm25',
)
save_results(bm25_results, 'bm25_results.json')


hybrid_results = evaluate_retrieval(
    questions=questions,
    retrieval_function=hybrid_search,
    retrieval_type='hybrid',
)
save_results(hybrid_results, 'hybrid_results.json')


hybrid_reranker_results = evaluate_retrieval(
    questions=questions,
    retrieval_function=hybrid_reranked_search,
    retrieval_type='hybrid_reranker',
)
save_results(hybrid_reranker_results, 'hybrid_reranker_results.json')