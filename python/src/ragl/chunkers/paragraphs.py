import re

from ragl.models import Chunk, Document


def chunk_by_paragraphs(document: Document) -> list[Chunk]:
    chunks = []

    for match in re.finditer(
        r"\S(?:.*?\S)?(?=\n\s*\n|\Z)",
        document.text,
        re.DOTALL,
    ):
        text = match.group(0)

        chunks.append(
            Chunk(
                document_source=document.source,
                text=text,
                start_char=match.start(),
                end_char=match.end(),
            )
        )

    return chunks
