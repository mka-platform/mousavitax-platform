"""Vector store interface + InMemory implementation (dev / MVP).

Production path (ADR-005): PostgreSQL + pgvector behind the same interface.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Optional

import numpy as np

try:
    from embedder import Embedder, EmbeddingError  # type: ignore
except ImportError:
    Embedder = None  # type: ignore
    EmbeddingError = Exception  # type: ignore


class VectorStore:
    def index(self, records: list[dict[str, Any]]) -> int:
        raise NotImplementedError

    def query(
        self, query_text: str, top_k: int = 5, filters: Optional[dict] = None
    ) -> list[dict[str, Any]]:
        raise NotImplementedError

    def count(self) -> int:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError


class InMemoryVectorStore(VectorStore):
    def __init__(
        self,
        persist_path: str | Path = "data/iran_tax_vectors.json",
        embedder: Any = None,
    ) -> None:
        self.persist_path = Path(persist_path)
        self.embedder = embedder
        self._records: list[dict[str, Any]] = []
        self._matrix: Optional[np.ndarray] = None
        self._load()

    def _load(self) -> None:
        if self.persist_path.exists():
            data = json.loads(self.persist_path.read_text(encoding="utf-8"))
            self._records = data.get("records", [])
            self._rebuild_matrix()

    def _save(self) -> None:
        self.persist_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"records": self._records, "updated_at": time.time()}
        self.persist_path.write_text(
            json.dumps(payload, ensure_ascii=False), encoding="utf-8"
        )

    def _rebuild_matrix(self) -> None:
        if not self._records:
            self._matrix = None
            return
        embs = [r["embedding"] for r in self._records]
        self._matrix = np.array(embs, dtype=np.float32)
        norms = np.linalg.norm(self._matrix, axis=1, keepdims=True) + 1e-9
        self._matrix = self._matrix / norms

    def index(self, records: list[dict[str, Any]]) -> int:
        if not records:
            return 0
        need_embed = [r for r in records if "embedding" not in r or not r["embedding"]]
        if need_embed:
            if self.embedder is None:
                raise RuntimeError("Embedder required to index records without embeddings")
            texts = [r["text"] for r in need_embed]
            vectors = self.embedder.embed_batch(texts)
            for r, v in zip(need_embed, vectors):
                r["embedding"] = v

        by_id = {r["chunk_id"]: i for i, r in enumerate(self._records)}
        for r in records:
            cid = r["chunk_id"]
            if cid in by_id:
                self._records[by_id[cid]] = r
            else:
                self._records.append(r)

        self._rebuild_matrix()
        self._save()
        return len(records)

    def query(
        self,
        query_text: str,
        top_k: int = 5,
        filters: Optional[dict] = None,
    ) -> list[dict[str, Any]]:
        if not self._records or self._matrix is None:
            return []
        if self.embedder is None:
            raise RuntimeError("Embedder required for query")

        q = np.array(self.embedder.embed_one(query_text), dtype=np.float32)
        q = q / (np.linalg.norm(q) + 1e-9)
        scores = self._matrix @ q

        indices = list(range(len(self._records)))
        if filters:

            def ok(i: int) -> bool:
                rec = self._records[i]
                for k, v in filters.items():
                    if rec.get(k) != v:
                        return False
                return True

            indices = [i for i in indices if ok(i)]

        if not indices:
            return []

        scored = [(i, float(scores[i])) for i in indices]
        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:top_k]

        hits = []
        for i, score in top:
            rec = self._records[i]
            hits.append({
                "chunk_id": rec["chunk_id"],
                "text": rec["text"],
                "score": score,
                "source_id": rec.get("source_id"),
                "source_type": rec.get("source_type"),
                "title": rec.get("title"),
                "page": rec.get("page"),
                "section": rec.get("section"),
                "url": rec.get("url"),
                "metadata": rec.get("metadata", {}),
            })
        return hits

    def count(self) -> int:
        return len(self._records)

    def clear(self) -> None:
        self._records = []
        self._matrix = None
        if self.persist_path.exists():
            self.persist_path.unlink()
