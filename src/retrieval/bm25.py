import re
import json
from pathlib import Path
from rank_bm25 import BM25Okapi
from .models import SearchResult


DEFAULT_CHUNKS_DIR = Path('data/processed/chunks/legal')


def tokenize(text: str) -> list[str]:
    return re.findall(r'\w+', text.lower(), flags=re.UNICODE)


class BM25Retriever:
    def __init__(self, chunks_dir: Path = DEFAULT_CHUNKS_DIR):
        self.chunks_dir = chunks_dir
        self.results = self._load_chunks()

        if not self.results:
            raise ValueError(f'No chunks found in {self.chunks_dir}')

        corpus = [tokenize(result.text) for result in self.results]
        self.bm25 = BM25Okapi(corpus)


    def _load_chunks(self) -> list[SearchResult]:
        results = []

        files = sorted(self.chunks_dir.glob('*.jsonl'))

        if not files:
            raise FileNotFoundError(f'No jsonl file found in {self.chunks_dir}')

        for file_path in files:
            with file_path.open('r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    chunk = json.loads(line)

                    results.append(
                        SearchResult(
                            chunk_id=chunk['chunk_id'],
                            text=chunk['text'],
                            metadata=chunk['metadata'],
                            distance=0.0
                        )
                    )

        return results

    def search(self, query: str, top_k: int = 20) -> list[SearchResult]:
        if not query.strip():
            raise ValueError('Query cannot be empty')

        if top_k <= 0:
            raise ValueError('Top k must be greater than 0')

        query_tokens = tokenize(query)

        scores = self.bm25.get_scores(query_tokens)

        ranked_indices = sorted(range(len(scores)), key=lambda index: scores[index], reverse=True)

        results = []

        for index in ranked_indices[:top_k]:
            result = self.results[index]

            result.bm25_score = float(scores[index])
            results.append(result)

        return results