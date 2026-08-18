"""KnowledgeService: thin orchestration over embedder + vector store."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "embedding-service" / "app"))
sys.path.insert(0, str(ROOT / "retrieval-engine" / "app"))
sys.path.insert(0, str(ROOT / "document-parser"))

from embedder import Embedder  # noqa: E402
from store import InMemoryVectorStore  # noqa: E402


class KnowledgeService:
    def __init__(
        self,
        persist_path: Optional[str] = None,
        embedder: Any = None,
    ) -> None:
        path = persist_path or os.getenv(
            "VECTOR_DB_PATH", str(ROOT.parent / "data" / "iran_tax_vectors.json")
        )
        self.embedder = embedder or Embedder()
        # Allow offline fallback when Ollama is down
        if os.getenv("EMBEDDING_PROVIDER", "ollama").lower() == "ollama":
            try:
                self.embedder.embed_one("ping")
            except Exception:
                self.embedder.provider = "fallback"
        self.store = InMemoryVectorStore(persist_path=path, embedder=self.embedder)

    def query(
        self,
        text: str,
        top_k: int = 5,
        filters: Optional[dict] = None,
    ) -> list[dict[str, Any]]:
        if not text.strip():
            return []
        try:
            return self.store.query(text, top_k=top_k, filters=filters)
        except Exception:
            return []

    def count(self) -> int:
        return self.store.count()

    def index_records(self, records: list[dict[str, Any]]) -> int:
        return self.store.index(records)
