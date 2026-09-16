

def is_relevant(result: dict, expected_document: str, expected_articles: list[str]) -> bool:
    metadata = result["metadata"]

    document_id = metadata.get("document_id")
    if document_id != expected_document:
        return False

    articles = metadata.get("articles", [])
    articles = [str(article) for article in articles]

    return any(article in expected_articles for article in articles)


def first_relevant_rank(results: list[dict], expected_document: str, expected_articles: list[str]) -> int | None:
    for rank, result in enumerate(results, start=1):
        if is_relevant(result, expected_document, expected_articles):
            return rank

    return None


def hit_at_k(results: list[dict], expected_document: str, expected_articles: list[str], k: int) -> bool:
    top_results = results[:k]

    return any(is_relevant(result, expected_document, expected_articles) for result in top_results)


def reciprocal_rank(results: list[dict], expected_document: str, expected_articles: list[str]) -> float:
    rank = first_relevant_rank(results, expected_document, expected_articles)

    if rank is None:
        return 0.0

    return 1.0 / rank