from src.generation.generator import AnswerGenerator
from src.generation.models import GeneratedAnswer
from src.retrieval.hybrid import HybridRetriever
from src.retrieval.reranker import CrossEncoderReranker


class QueryService:
    def __init__(self, hybrid_retriever: HybridRetriever, reranker: CrossEncoderReranker, generator: AnswerGenerator):
        self.hybrid_retriever = hybrid_retriever
        self.reranker = reranker
        self.generator = generator


    def answer_question(self, question: str, initial_top_k: int = 20, final_top_k: int = 5) -> GeneratedAnswer:
        hybrid_results = self.hybrid_retriever.search(
            query=question,
            semantic_top_k=initial_top_k,
            bm25_top_k=initial_top_k,
            final_top_k=initial_top_k,
        )

        reranked_results = self.reranker.rerank(
            query=question,
            results=hybrid_results,
            top_k=final_top_k,
        )

        return self.generator.generate(
            question=question,
            results=reranked_results,
        )