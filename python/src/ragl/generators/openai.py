from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

from ragl.models import ScoredChunk

load_dotenv()

_INSTRUCTIONS = """\
Answer the question using only the numbered sources below.
After every sentence, cite the sources that support it, like [1] or [2][3].
If the sources do not contain the answer, reply exactly:
"If can't answer that from the provided documents." and cite nothing."""


class _ModelAnswer(BaseModel):
    answer: str
    cited: list[int]


class Answer(BaseModel):
    text: str
    sources: list[ScoredChunk]


def format_sources(chunks: list[ScoredChunk]) -> str:
    return "\n\n".join(f"[{n}] {chunk.text}" for n, chunk in enumerate(chunks, start=1))


def valid_citations(cited: list[int], source_count: int) -> list[int]:
    return sorted({number for number in cited if 1 <= number <= source_count})


class OpenAIGenerator:
    def __init__(self, model: str = "gpt-4o-mini") -> None:
        self.client = OpenAI()
        self.model = model

    def answer(self, question: str, chunks: list[ScoredChunk]) -> Answer:
        response = self.client.responses.parse(
            model=self.model,
            instructions=_INSTRUCTIONS,
            input=f"Sources:\n\n{format_sources(chunks)}\n\nQuestion:{question}",
            text_format=_ModelAnswer,
            temperature=0,
        )
        parsed = response.output_parsed
        if parsed is None:
            raise RuntimeError(f"{self.model} reutrned no parsable answer")

        cited = valid_citations(parsed.cited, len(chunks))
        return Answer(text=parsed.answer, sources=[chunks[n - 1] for n in cited])
