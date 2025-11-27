from typing import Any
import httpx
from hmlio_BE.llm.conf import LLM_TIMEOUT_SECONDS, OLLAMA_BASE_URL, OLLAMA_MODEL
from llm.views import BaseLLMClient


class OllamaClient(BaseLLMClient):
    name = "ollama"

    def generate(
        self,
        *,
        message: str,
        temp: float = 0.7,
        tools: list[dict] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> list[str]:
        prompt = message
        payload = {
            "model": (extra or {}).get("model", OLLAMA_MODEL),
            "prompt": prompt,
            "options": {"temperature": temp},
            "stream": False,
        }
        with httpx.Client(timeout=LLM_TIMEOUT_SECONDS) as client:
            res = client.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload)
            res.raise_for_status()
            data = res.json()
            return data.get("response", [""])
