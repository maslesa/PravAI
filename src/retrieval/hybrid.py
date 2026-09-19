from .models import SearchResult
from .search import SemanticRetriever
from .bm25 import BM25Retriever


DEFAULT_RRF_K = 60


class HybridRetriever:
    def __init__(self, semantic_retriever: SemanticRetriever, bm25_retriever: BM25Retriever, rrf_k: int = DEFAULT_RRF_K):
        self.semantic_retriever = semantic_retriever
        self.bm25_retriever = bm25_retriever
        self.rrf_k = rrf_k


    def search(self, query: str, semantic_top_k: int = 20, bm25_top_k: int = 20, final_top_k: int = 20) -> list[SearchResult]:

        semantic_results= self.semantic_retriever.search(query=query, strategy='legal', top_k=semantic_top_k)
        bm25_results = self.bm25_retriever.search(query=query, top_k=bm25_top_k)

        return self._fuse_results(semantic_results, bm25_results, top_k=final_top_k)

    def _fuse_results(
        self,
        semantic_results: list[SearchResult],
        bm25_results: list[SearchResult],
        top_k: int,
    ) -> list[SearchResult]:

        results_by_id = {}

        for result in semantic_results:
            results_by_id[result.chunk_id] = result

        for result in bm25_results:
            if result.chunk_id not in results_by_id:
                results_by_id[result.chunk_id] = result

        rrf_scores = {}

        for rank, result in enumerate(semantic_results, start=1):
            rrf_scores[result.chunk_id] = rrf_scores.get(result.chunk_id, 0.0) + 1.0 / (self.rrf_k  + rank)

        for rank, result in enumerate(bm25_results, start=1):
            rrf_scores[result.chunk_id] = rrf_scores.get(result.chunk_id, 0.0) + 1.0 / (self.rrf_k + rank)

        results = []

        for chunk_id, score in rrf_scores.items():
            result = results_by_id[chunk_id]
            result.hybrid_score = score

            results.append(result)

        results.sort(key=lambda result: result.hybrid_score, reverse=True)

        return results[:top_k]