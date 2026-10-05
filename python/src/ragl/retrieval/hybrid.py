from ragl.models import ScoredChunk
from ragl.retrieval.fusion import reciprocal_rank_fusion
from ragl.retrieval.keyword import keyword_search
from ragl.retrieval.vector import vector_search


def hybrid_search(
    question: str,
    question_embedding: list[float],
    k: int = 5,
    candidates: int = 20,
) -> list[ScoredChunk]:
    keyword = keyword_search(question, candidates)
    vector = vector_search(question_embedding, candidates)
    return reciprocal_rank_fusion([keyword, vector])[:k]
