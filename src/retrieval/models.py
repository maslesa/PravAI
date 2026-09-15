from dataclasses import dataclass


@dataclass
class SearchResult:
    chunk_id: str
    text: str
    metadata: dict
    distance: float

    @property
    def similarity(self) -> float:
        return 1.0 - self.distance