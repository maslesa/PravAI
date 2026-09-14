from pathlib import Path
import chromadb


DEFAULT_CHROMA_PATH = 'data/chroma'


class ChromaStore:
    def __init__(self, path: str | Path = DEFAULT_CHROMA_PATH):
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(path=str(self.path))


    def get_or_create_collection(self, name: str):
        return self.client.get_or_create_collection(name=name, metadata={'hnsw:space': 'cosine'})


    def add_chunks(
        self,
        collection,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
    ) -> None:
        collection.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)