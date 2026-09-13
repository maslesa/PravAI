

def fixed_size_chunks(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative")

    if chunk_overlap > chunk_size:
        raise ValueError("chunk_overlap must be less than chunk_size")

    chunks = []

    start = 0
    step = chunk_size - chunk_overlap

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start += step

    return chunks