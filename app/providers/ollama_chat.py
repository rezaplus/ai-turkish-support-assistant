import httpx

from app.core.config import get_settings


class OllamaChatProvider:
    def __init__(self) -> None:
        settings = get_settings()
        self.base_url = settings.ollama_url
        self.model = settings.ollama_chat_model

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "stream": False,
                    "format": "json",
                    "think": False,
                    "keep_alive": "1h",
                    "options": {"temperature": 0.2},
                    "messages": [
                        {
                            "role": "system",
                            "content": system_prompt,
                        },
                        {
                            "role": "user",
                            "content": user_prompt,
                        },
                    ],
                },
                timeout=120.0,
            )

            response.raise_for_status()

            data = response.json()

            return data["message"]["content"]
