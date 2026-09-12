from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class DocumentMetadata:
    document_id: str
    title: str
    filename: str
    source: str
    source_url: str | None
    language: str
    document_type: str
    status: str
    retrieved_at: str


def create_document_id(filename: str) -> str:
    return Path(filename).stem


def create_document_metadata(pdf_path: Path, title: str, source_url: str | None = None) -> DocumentMetadata:
    path = Path(pdf_path)

    return DocumentMetadata(
        document_id=create_document_id(path.name),
        title=title,
        filename=path.name,
        source='PISRS',
        source_url=source_url,
        language='sr',
        document_type='law',
        status='valid',
        retrieved_at=datetime.now(timezone.utc).isoformat(),
    )