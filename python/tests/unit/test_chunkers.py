from ragl.chunkers.paragraphs import chunk_by_paragraphs
from ragl.chunkers.structure import chunk_by_structure
from ragl.chunkers.tokens import chunk_by_tokens
from ragl.models import Document


def test_token_chunker_has_overlap() -> None:
    document = Document(
        source="test.md",
        text=" ".join(f"word{i}" for i in range(50)),
    )

    chunks = chunk_by_tokens(document, chunk_size=10, overlap=2)

    assert len(chunks) > 1


def test_paragraph_chunker() -> None:
    document = Document(
        source="test.md",
        text="First paragraph.\n\nSecond paragraph.",
    )

    chunks = chunk_by_paragraphs(document)

    assert [chunk.text for chunk in chunks] == [
        "First paragraph.",
        "Second paragraph.",
    ]


def test_structure_chunker() -> None:
    document = Document(
        source="test.md",
        text="# Intro\n\nHello.\n\n## Embeddings\n\nVectors.\n",
    )

    chunks = chunk_by_structure(document)

    assert len(chunks) == 2
    assert chunks[0].text.startswith("# Intro")
    assert chunks[1].text.startswith("## Embeddings")
