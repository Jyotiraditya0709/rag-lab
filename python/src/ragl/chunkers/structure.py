import re

from ragl.chunkers.paragraphs import chunk_by_paragraphs
from ragl.models import Chunk, Document

_heading_pattern = re.compile(r"(?m)^#{1,6}\s+.+$")


def chunk_by_structure(document: Document) -> list[Chunk]:
    matches = list(_heading_pattern.finditer(document.text))

    if not matches:
        return chunk_by_paragraphs(document)

    starts = [0] + [match.start() for match in matches]
    chunks = []

    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else len(document.text)
        text = document.text[start:end].strip()

        if not text:
            continue

        actual_start = document.text.find(text, start)
        actual_end = actual_start + len(text)

        chunks.append(
            Chunk(
                document_source=document.source,
                text=text,
                start_char=actual_start,
                end_char=actual_end,
            )
        )

    return chunks
