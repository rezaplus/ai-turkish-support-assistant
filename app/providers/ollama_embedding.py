import httpx

from app.core.config import get_settings


class OllamaEmbeddingProvider:
    def __init__(self) -> None:
        settings = get_settings()

        self.base_url = settings.ollama_url
        self.model = "qwen3-embedding:0.6b"

    async def embed(self, text: str) -> list[float]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/embed",
                json={
                    "model": self.model,
                    "input": text,
                },
                timeout=60.0,
            )

            response.raise_for_status()

            data = response.json()

            return data["embeddings"][0]