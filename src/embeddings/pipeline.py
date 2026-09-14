import json
from pathlib import Path
from .chroma import ChromaStore
from .model import EmbeddingModel


def load_chunks(path: str | Path) -> list[dict]:
    path = Path(path)

    chunks = []

    with path.open('r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            chunks.append(json.loads(line))

    return chunks


def create_collection_name(strategy: str) -> str:
    return f'PravAI_{strategy}'


def index_chunks(
    chunks: list[dict],
    strategy: str,
    embedding_model: EmbeddingModel,
    chroma_store: ChromaStore
) -> None:
    if not chunks:
        return

    collection_name = create_collection_name(strategy)

    collection = chroma_store.get_or_create_collection(collection_name)

    texts = [chunk['text'] for chunk in chunks]
    ids = [chunk['chunk_id'] for chunk in chunks]
    metadatas = [chunk['metadata'] for chunk in chunks]

    embeddings = embedding_model.encode(texts)

    chroma_store.add_chunks(
        collection=collection,
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f'Added {len(chunks)} chunks to {collection_name}.')


def process_strategy(
    strategy: str,
    chunks_dir: str | Path,
    embedding_model: EmbeddingModel,
    chroma_store: ChromaStore,
) -> None:
    strategy_dir = Path(chunks_dir) / strategy
    chunks_files = sorted(strategy_dir.glob('*.jsonl'))

    if not chunks_files:
        raise FileNotFoundError(f'No JSONL chunk files found in {strategy_dir}.')

    print(f'\n===== Strategy: {strategy} =====')

    for chunk_file in chunks_files:
        print(f'Processing {chunk_file.name}...')

        chunks = load_chunks(str(chunk_file))

        index_chunks(chunks, strategy, embedding_model, chroma_store)


def run_embedding_pipeline(
    chunks_dir: str | Path,
    chroma_path: str | Path,
) -> None:
    embedding_model = EmbeddingModel()
    chroma_store = ChromaStore(chroma_path)

    strategies = ['fixed', 'recursive', 'legal']

    for strategy in strategies:
        process_strategy(strategy, chunks_dir, embedding_model, chroma_store)

    print(f'\n===== Embedding pipeline completed =====')