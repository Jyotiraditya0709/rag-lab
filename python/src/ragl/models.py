from pydantic import BaseModel


class Document(BaseModel):
    source: str
    text: str
    title: str | None = None


class Chunk(BaseModel):
    document_source: str
    text: str
    start_char: int
    end_char: int
