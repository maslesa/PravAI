from sentence_transformers import CrossEncoder
from .models import SearchResult


DEFAULT_RERANKER_MODEL = 'cross-encoder/mmarco-mMiniLMv2-L12-H384-v1'


class CrossEncoderReranker:
    def __init__(self, model_name: str = DEFAULT_RERANKER_MODEL):
        self.model_name = model_name
        self.model = CrossEncoder(model_name)


    def rerank(self, query: str, results: list[SearchResult], top_k: int = 5) -> list[SearchResult]:
        if not query.strip():
            raise ValueError("Query can not be empty")

        if top_k <= 0:
            raise ValueError("top_k must be greater than 0")

        if not results:
            return []

        pairs = [(query, result.text) for result in results]

        scores = self.model.predict(pairs)

        for result, score in zip(results, scores):
            result.reranker_score = float(score)

        results.sort(key=lambda result: result.reranker_score, reverse=True)

        return results[:top_k]