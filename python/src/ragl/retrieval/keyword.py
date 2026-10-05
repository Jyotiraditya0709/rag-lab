from sqlalchemy import text
from sqlalchemy.orm import Session

from ragl.db import engine
from ragl.models import ScoredChunk

# plainto_tsquery joins words with AND, so a long question only matches chunks
# containing every word. Swapping & for | turns it into OR and lets ts_rank_cd
# decide which chunks match best.
_KEYWORD_SQL = text(
    """
    WITH q AS (
        SELECT replace(plainto_tsquery('english', :question)::text, '&', '|')::tsquery
            AS query
    )
    SELECT id, document_source, text, start_char, end_char,
           ts_rank_cd(tsv, q.query) AS score
    FROM chunks, q
    WHERE tsv @@ q.query
    ORDER BY score DESC
    LIMIT :k
    """
)


def keyword_search(question: str, k: int = 20) -> list[ScoredChunk]:
    with Session(engine) as session:
        rows = session.execute(_KEYWORD_SQL, {"question": question, "k": k})
        return [ScoredChunk.model_validate(row, from_attributes=True) for row in rows]
