from collections import defaultdict
from uuid import UUID

from ragl.models import ScoredChunk


def reciprocal_rank_fusion(
    rankings: list[list[ScoredChunk]], k: int = 60
) -> list[ScoredChunk]:
    # Uses rank, not score: ts_rank_cd and cosine similarity are on different
    # scales, so their raw scores can't be added together.
    scores: dict[UUID, float] = defaultdict(float)
    chunks: dict[UUID, ScoredChunk] = {}

    for ranking in rankings:
        for rank, chunk in enumerate(ranking, start=1):
            scores[chunk.id] += 1.0 / (k + rank)
            chunks.setdefault(chunk.id, chunk)

    ordered = sorted(scores, key=lambda chunk_id: scores[chunk_id], reverse=True)
    return [chunks[i].model_copy(update={"score": scores[i]}) for i in ordered]
