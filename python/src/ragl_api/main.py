from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ragl.embedders.openai import OpenAIEmbedder
from ragl.generators.openai import Answer, OpenAIGenerator
from ragl.retrieval.hybrid import hybrid_search

app = FastAPI(title="RAG LAB API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["hhttp://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
embedder = OpenAIEmbedder()
generator = OpenAIGenerator()


class AskRequest(BaseModel):
    question: str
    k: int = 5


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask")
def ask(request: AskRequest) -> Answer:
    embedding = embedder.embed([request.question])[0]

    chunks = hybrid_search(
        request.question,
        embedding,
        k=request.k,
    )

    return generator.answer(request.question, chunks)
