
def recursive_chunks(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:

    if chunk_size <= 0:
        raise ValueError('chunk_size must be greater than 0')

    if chunk_overlap < 0:
        raise ValueError('chunk_overlap cannot be negative')

    if chunk_overlap >= chunk_size:
        raise ValueError('chunk_overlap must be smaller than chunk_size')

    separators = ['\n\n', '\n', '. ', ' ', '']

    chunks = _split_text(text, separators, chunk_size)

    return _add_overlap(chunks, chunk_overlap)


def _split_text(text: str, separators: list[str], chunk_size: int) -> list[str]:
    text = text.strip()

    if not text:
        return []

    if len(text) <= chunk_size:
        return [text]

    if not separators:
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    separator = separators[0]
    remaining_separators = separators[1:]

    if separator == '':
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    parts = text.split(separator)

    chunks = []
    current = ''

    for part in parts:
        if not part:
            continue

        candidate = f'{current}{separator}{part}' if current else part

        if len(candidate) <= chunk_size:
            current = candidate
            continue

        if current:
            chunks.extend(_split_text(current, remaining_separators, chunk_size))

        if len(part) <= chunk_size:
            current = part
        else:
            chunks.extend(_split_text(part, remaining_separators, chunk_size))

    if current:
        chunks.extend(_split_text(current, remaining_separators, chunk_size))

    return chunks


def _add_overlap(chunks: list[str], chunk_overlap: int) -> list[str]:

    if chunk_overlap == 0:
        return chunks

    results = []

    for index, chunk in enumerate(chunks):
        if index == 0:
            results.append(chunk)
            continue

        previous = chunks[index - 1]
        overlap = previous[-chunk_overlap:]

        results.append(f'{overlap} {chunk}'.strip())

    return results