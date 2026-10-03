from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class OpenAIEmbedder:
    def __init__(self, model: str = "text-embedding-3-small") -> None:
        self.client = OpenAI()
        self.model = model

    def embed(self, texts: list[str]) -> list[list[float]]:
        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
        )

        return [
            item.embedding
            for item in sorted(response.data, key=lambda item: item.index)
        ]
