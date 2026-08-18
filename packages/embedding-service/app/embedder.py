"""Embedding Service – provider-agnostic text embeddings.

Default: Ollama (nomic-embed-text).
Fallback: deterministic hash vector (dev only).
"""

from __future__ import annotations

import hashlib
import os
from typing import Sequence

import httpx
import numpy as np


class EmbeddingError(Exception):
    pass


class Embedder:
    def __init__(self) -> None:
        self.provider = os.getenv("EMBEDDING_PROVIDER", "ollama").lower()
        self.ollama_base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.ollama_model = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
        self._dim: int | None = None

    @property
    def dimension(self) -> int:
        if self._dim is None:
            v = self.embed_one("test")
            self._dim = len(v)
        return self._dim

    def embed_one(self, text: str) -> list[float]:
        return self.embed_batch([text])[0]

    def embed_batch(self, texts: Sequence[str]) -> list[list[float]]:
        if not texts:
            return []
        if self.provider == "ollama":
            return self._ollama_batch(list(texts))
        return [self._fallback_vec(t) for t in texts]

    def _ollama_batch(self, texts: list[str]) -> list[list[float]]:
        out: list[list[float]] = []
        try:
            with httpx.Client(timeout=120.0) as client:
                for t in texts:
                    r = client.post(
                        f"{self.ollama_base}/api/embeddings",
                        json={"model": self.ollama_model, "prompt": t},
                    )
                    if r.status_code != 200:
                        raise EmbeddingError(
                            f"Ollama embeddings HTTP {r.status_code}: {r.text[:200]}"
                        )
                    data = r.json()
                    emb = data.get("embedding")
                    if not emb:
                        raise EmbeddingError("No embedding in Ollama response")
                    out.append(emb)
            return out
        except httpx.HTTPError as e:
            raise EmbeddingError(f"Ollama connection failed: {e}") from e

    def _fallback_vec(self, text: str, dim: int = 384) -> list[float]:
        h = hashlib.sha256(text.encode("utf-8")).digest()
        rng = np.random.default_rng(int.from_bytes(h[:8], "little"))
        v = rng.standard_normal(dim).astype(np.float32)
        v /= np.linalg.norm(v) + 1e-9
        return v.tolist()
