from src.generation.generator import AnswerGenerator
from src.generation.models import GeneratedAnswer
from src.retrieval.hybrid import HybridRetriever
from src.retrieval.reranker import CrossEncoderReranker
from collections.abc import Iterator
import json


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


    def stream_answer(self, question: str, initial_top_k: int = 20, final_top_k: int = 5) -> Iterator[str]:
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

        for chunk in self.generator.stream(question, reranked_results):
            event = {
                'type': 'token',
                'content': chunk,
            }

            yield json.dumps(event, ensure_ascii=False) + '\n'

        citations = self._build_citations(reranked_results)

        metadata_event = {
            'type': 'metadata',
            'citations': citations,
            'grounded': bool(reranked_results),
        }

        yield json.dumps(metadata_event, ensure_ascii=False) + '\n'

        done_event = {
            'type': 'done',
        }

        yield json.dumps(done_event, ensure_ascii=False) + '\n'


    @staticmethod
    def _build_citations(results) -> list[dict]:
        citations = []
        seen = set()

        for result in results:
            metadata = result.metadata

            law = metadata.get('document_title', metadata.get('document_id', ''))
            article = metadata.get('article', '')

            if not law or not article:
                continue

            law = str(law).strip()
            article = str(article).strip()

            key = (law, article)

            if key in seen:
                continue

            seen.add(key)

            citations.append(
                {
                    'law': law,
                    'article': article,
                }
            )

        return citations