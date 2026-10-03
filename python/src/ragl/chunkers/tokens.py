import tiktoken

from ragl.models import Chunk, Document

_encoder = tiktoken.get_encoding("cl100k_base")


def chunk_by_tokens(
    document: Document,
    chunk_size: int = 400,
    overlap: int = 40,
) -> list[Chunk]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size")

    tokens = _encoder.encode(document.text)
    step = chunk_size - overlap
    chunks = []
    search_from = 0

    for token_start in range(0, len(tokens), step):
        piece = _encoder.decode(tokens[token_start : token_start + chunk_size])

        if not piece:
            continue

        start_char = document.text.find(piece, search_from)
        if start_char == -1:
            raise ValueError("Could not map token chunk back to source text")

        end_char = start_char + len(piece)

        chunks.append(
            Chunk(
                document_source=document.source,
                text=piece,
                start_char=start_char,
                end_char=end_char,
            )
        )

        search_from = start_char + 1

        if token_start + chunk_size >= len(tokens):
            break

    return chunks
