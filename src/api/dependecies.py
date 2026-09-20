from functools import lru_cache
from src.generation.generator import AnswerGenerator
from src.generation.llm import OllamaLLM
from src.retrieval.bm25 import BM25Retriever
from src.retrieval.hybrid import HybridRetriever
from src.retrieval.reranker import CrossEncoderReranker
from src.retrieval.search import SemanticRetriever
from src.embeddings.chroma import ChromaStore
from src.embeddings.model import EmbeddingModel
from .services.query_service import QueryService


DEFAULT_LLM_MODEL = 'qwen3:8b'


@lru_cache
def get_query_service() -> QueryService:
    embedding_model = EmbeddingModel()
    chroma_store = ChromaStore()

    semantic_retriever = SemanticRetriever(embedding_model, chroma_store)
    bm25_retriever = BM25Retriever()
    hybrid_retriever = HybridRetriever(semantic_retriever, bm25_retriever)

    reranker = CrossEncoderReranker()

    llm = OllamaLLM(model=DEFAULT_LLM_MODEL)
    generator = AnswerGenerator(llm=llm)

    return QueryService(
        hybrid_retriever=hybrid_retriever,
        reranker=reranker,
        generator=generator,
    )