from dataclasses import dataclass


@dataclass
class SearchResult:
    chunk_id: str
    text: str
    metadata: dict
    distance: float
    reranker_score: float | None = None
    bm25_score: float | None = None
    hybrid_score: float | None = None

    @property
    def similarity(self) -> float:
        return 1.0 - self.distance