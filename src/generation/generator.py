import json
from src.retrieval.models import SearchResult
from .llm import OllamaLLM
from .models import Citation, GeneratedAnswer
from .prompt import SYSTEM_PROMPT, build_prompt, STREAMING_SYSTEM_PROMPT, build_streaming_prompt
from collections.abc import Iterator


class AnswerGenerator:
    def __init__(self, llm: OllamaLLM):
        self.llm = llm


    def generate(self, question: str, results: list[SearchResult]) -> GeneratedAnswer:
        if not question.strip():
            raise ValueError('Question must not be empty.')

        if not results:
            return GeneratedAnswer(
                answer='Na osnovu dostupnih izvora nije moguće dati pouzdan odgovor na ovo pitanje.',
                citations=[],
                grounded=False,
            )

        prompt = build_prompt(question, results)

        raw_response = self.llm.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=prompt,
            temperature=0.0
        )

        return self._parse_response(raw_response, results)


    def _parse_response(self, raw_response: str, results: list[SearchResult]) -> GeneratedAnswer:
        try:
            data = json.loads(raw_response)
        except json.JSONDecodeError as error:
            raise RuntimeError('LLM returned invalid json') from error

        answer = data.get('answer')

        if not isinstance(answer, str):
            raise RuntimeError('LLM response does not contain a valid answer.')

        grounded = data.get('grounded')

        if not isinstance(grounded, bool):
            grounded = False

        citations = self._validate_citations(data.get('citations', []), results)

        if not grounded:
            citations = []

        return GeneratedAnswer(
            answer=answer.strip(),
            citations=citations,
            grounded=grounded,
        )


    def _validate_citations(self, citations_data, results: list[SearchResult]) -> list[Citation]:
        if not isinstance(citations_data, list):
            return []

        valid_sources = set()

        for result in results:
            metadata = result.metadata

            law = metadata.get('document_title', metadata.get('document_id', ''))
            article = metadata.get('article', '')

            if law and article:
                valid_sources.add((str(law).strip(), str(article).strip()))

        citations = []

        for citation in citations_data:
            if not isinstance(citation, dict):
                continue

            law = str(citation.get('law', '')).strip()
            article = str(citation.get('article', '')).strip()

            if not law or not article:
                continue

            if (law, article) not in valid_sources:
                continue

            citations.append(
                Citation(
                    law=law,
                    article=article,
                )
            )

        return self._remove_duplicate_citations(citations)


    @staticmethod
    def _remove_duplicate_citations(citations: list[Citation]) -> list[Citation]:
        unique = []
        seen = set()

        for citation in citations:
            key = (citation.law, citation.article)

            if key in seen:
                continue

            seen.add(key)
            unique.append(citation)

        return unique


    def stream(self, question: str, results: list[SearchResult]) -> Iterator[str]:
        if not question.strip():
            raise ValueError('Question must not be empty.')

        if not results:
            yield 'Na osnovu dostupnih izvora nije moguće dati pouzdan odgovor na ovo pitanje.'
            return

        prompt = build_streaming_prompt(question, results)

        yield from self.llm.stream(
            system_prompt=STREAMING_SYSTEM_PROMPT,
            user_prompt=prompt,
            temperature=0.0
        )