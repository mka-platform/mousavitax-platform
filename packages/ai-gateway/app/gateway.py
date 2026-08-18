"""AI Gateway – provider-agnostic LLM interface."""

from __future__ import annotations

import os
import time

import httpx


class AIGatewayError(Exception):
    pass


class AIGateway:
    def __init__(self) -> None:
        self.provider = os.getenv("LLM_PROVIDER", "gemini").lower()
        self.google_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-lite")

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 1024,
    ) -> tuple[str, str, int]:
        start = time.perf_counter()

        if self.provider == "gemini":
            text, model = await self._call_gemini(
                system_prompt, user_prompt, temperature, max_tokens
            )
        elif self.provider in ("openai", "openrouter", "ollama"):
            text, model = await self._call_openai_compatible(
                system_prompt, user_prompt, temperature, max_tokens
            )
        else:
            raise AIGatewayError(f"Unsupported LLM_PROVIDER: {self.provider}")

        latency_ms = int((time.perf_counter() - start) * 1000)
        return text, model, latency_ms

    async def _call_gemini(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: int,
    ) -> tuple[str, str]:
        if not self.google_api_key:
            raise AIGatewayError("GOOGLE_API_KEY / GEMINI_API_KEY is not set")

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.gemini_model}:generateContent?key={self.google_api_key}"
        )
        payload = {
            "system_instruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            },
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(url, json=payload)
            data = resp.json()
            if resp.status_code != 200:
                msg = data.get("error", {}).get("message", resp.text)
                raise AIGatewayError(f"Gemini API error {resp.status_code}: {msg}")
            try:
                text = data["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError) as e:
                raise AIGatewayError(f"Unexpected Gemini response: {data}") from e
            return text.strip(), self.gemini_model

    async def _call_openai_compatible(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: int,
    ) -> tuple[str, str]:
        if not self.openai_api_key and self.provider != "ollama":
            raise AIGatewayError("OPENAI_API_KEY is not set")

        url = f"{self.openai_base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openai_api_key or 'ollama'}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.openai_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            data = resp.json()
            if resp.status_code != 200:
                msg = data.get("error", {}).get("message", resp.text)
                raise AIGatewayError(
                    f"OpenAI-compatible API error {resp.status_code}: {msg}"
                )
            try:
                text = data["choices"][0]["message"]["content"]
            except (KeyError, IndexError) as e:
                raise AIGatewayError(f"Unexpected response: {data}") from e
            return text.strip(), self.openai_model
