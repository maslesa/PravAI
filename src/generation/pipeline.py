from src.embeddings.chroma import ChromaStore
from src.embeddings.model import EmbeddingModel
from src.retrieval.reranker import CrossEncoderReranker
from src.retrieval.search import SemanticRetriever
from src.retrieval.bm25 import BM25Retriever
from src.retrieval.hybrid import HybridRetriever
from .generator import AnswerGenerator
from .llm import OllamaLLM
from .models import GeneratedAnswer


DEFAULT_LLM_MODEL = 'qwen3:8b'


def create_generation_pipeline(llm_model: str = DEFAULT_LLM_MODEL):
    embedding_model = EmbeddingModel()
    chroma_store = ChromaStore()
    semantic_retriever = SemanticRetriever(embedding_model, chroma_store)
    bm25_retriever = BM25Retriever()
    hybrid_retriever = HybridRetriever(semantic_retriever, bm25_retriever)
    reranker = CrossEncoderReranker()
    llm = OllamaLLM(llm_model)
    generator = AnswerGenerator(llm)

    return (hybrid_retriever, reranker, generator)


def run_generation(
    question: str,
    hybrid_retriever: HybridRetriever,
    reranker: CrossEncoderReranker,
    generator: AnswerGenerator,
    initial_top_k: int = 20,
    final_top_k: int = 5,
) -> GeneratedAnswer:

    hybrid_results = hybrid_retriever.search(
        query=question,
        semantic_top_k=initial_top_k,
        bm25_top_k=initial_top_k,
        final_top_k=initial_top_k
    )

    reranked_results = reranker.rerank(
        query=question,
        results=hybrid_results,
        top_k=final_top_k
    )

    return generator.generate(question, reranked_results)