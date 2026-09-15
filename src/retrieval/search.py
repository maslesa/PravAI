from src.embeddings.chroma import ChromaStore
from src.embeddings.model import EmbeddingModel
from .models import SearchResult


class SemanticRetriever:
    def __init__(self, embedding_model: EmbeddingModel, chroma_store: ChromaStore):
        self.embedding_model = embedding_model
        self.chroma_store = chroma_store


    def search(self, query: str, strategy: str = 'legal', top_k: int = 5) -> list[SearchResult]:
        if not query.strip():
            raise ValueError("Query cannot be empty")

        if top_k <= 0:
            raise ValueError("Top k must be greater than 0")

        collection_name = f'PravAI_{strategy}'

        collection = self.chroma_store.get_or_create_collection(collection_name)

        query_embedding = self.embedding_model.encode_one(query)

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=['documents', 'metadatas', 'distances']
        )

        return self._parse_results(results)


    def _parse_results(self, results: dict) -> list[SearchResult]:
        ids = results['ids'][0]
        documents = results['documents'][0]
        metadatas = results['metadatas'][0]
        distances = results['distances'][0]

        search_results = []

        for index in range(len(ids)):
            search_results.append(SearchResult(
                chunk_id=ids[index],
                text=documents[index],
                metadata=metadatas[index],
                distance=distances[index],
            ))

        return search_results