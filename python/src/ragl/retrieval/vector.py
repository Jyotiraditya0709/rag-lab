from sqlalchemy import select
from sqlalchemy.orm import Session

from ragl.db import engine
from ragl.models import ScoredChunk
from ragl.storage import ChunkRecord


def vector_search(question_embedding: list[float], k: int = 20) -> list[ScoredChunk]:
    distance = ChunkRecord.embedding.cosine_distance(question_embedding)
    stmt = select(ChunkRecord, distance.label("distance")).order_by(distance).limit(k)

    with Session(engine) as session:
        return [
            ScoredChunk(
                id=record.id,
                document_source=record.document_source,
                text=record.text,
                start_char=record.start_char,
                end_char=record.end_char,
                score=1 - dist,
            )
            for record, dist in session.execute(stmt)
        ]
