from uuid import UUID, uuid4

from pgvector.sqlalchemy import Vector
from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, Session, mapped_column

from ragl.db import Base, engine
from ragl.models import Chunk


class ChunkRecord(Base):
    __tablename__ = "chunks"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    document_source: Mapped[str] = mapped_column(String(500))
    text: Mapped[str] = mapped_column(Text)
    start_char: Mapped[int]
    end_char: Mapped[int]
    embedding: Mapped[list[float] | None] = mapped_column(Vector(1536))


def create_tables() -> None:
    Base.metadata.create_all(engine)


def save_chunks(chunks: list[Chunk], embeddings: list[list[float]]) -> None:
    if len(chunks) != len(embeddings):
        raise ValueError("chunks and embeddings must have the same length")

    with Session(engine) as session:
        for chunk, embedding in zip(chunks, embeddings):
            session.add(
                ChunkRecord(
                    document_source=chunk.document_source,
                    text=chunk.text,
                    start_char=chunk.start_char,
                    end_char=chunk.end_char,
                    embedding=embedding,
                )
            )

        session.commit()
