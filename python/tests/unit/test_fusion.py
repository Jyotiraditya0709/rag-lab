from uuid import uuid4

from pytest import approx

from ragl.models import ScoredChunk
from ragl.retrieval.fusion import reciprocal_rank_fusion


def make_chunk(name: str) -> ScoredChunk:
    return ScoredChunk(
        id=uuid4(),
        document_source="test.md",
        text=name,
        start_char=0,
        end_char=len(name),
        score=0.0,
    )


def test_chunk_found_by_both_retrievers_wins() -> None:
    a, b, c = make_chunk("a"), make_chunk("b"), make_chunk("c")

    fused = reciprocal_rank_fusion([[a, b], [c, b]], k=60)

    assert [chunk.text for chunk in fused] == ["b", "a", "c"]
    assert fused[0].score == approx(1 / 62 + 1 / 62)
    assert fused[1].score == approx(1 / 61)


def test_empty_rankings() -> None:
    assert reciprocal_rank_fusion([[], []]) == []
