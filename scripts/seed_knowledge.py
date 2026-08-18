#!/usr/bin/env python3
"""Seed sample iran-tax knowledge into the vector store.

Usage (from repo root):
  export EMBEDDING_PROVIDER=fallback
  export VECTOR_DB_PATH=$PWD/data/iran_tax_vectors.json
  python scripts/seed_knowledge.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "packages" / "document-parser"))
sys.path.insert(0, str(ROOT / "packages" / "embedding-service" / "app"))
sys.path.insert(0, str(ROOT / "packages" / "retrieval-engine" / "app"))
sys.path.insert(0, str(ROOT / "packages" / "knowledge-core"))

from app.parser import DocumentParser  # noqa: E402
from knowledge_core import KnowledgeService  # noqa: E402

KNOWLEDGE_DIR = ROOT / "domains" / "iran-tax" / "knowledge"


def main() -> None:
    os.environ.setdefault("EMBEDDING_PROVIDER", "fallback")
    db_path = os.environ.get("VECTOR_DB_PATH") or str(ROOT / "data" / "iran_tax_vectors.json")
    os.environ["VECTOR_DB_PATH"] = db_path
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    ks = KnowledgeService(persist_path=db_path)
    parser = DocumentParser(chunk_size=900, chunk_overlap=150)

    files = sorted(KNOWLEDGE_DIR.glob("*.md"))
    files = [f for f in files if f.name.lower() != "readme.md"]
    if not files:
        print("No knowledge markdown files found.", file=sys.stderr)
        sys.exit(1)

    total = 0
    for path in files:
        doc = parser.parse_file(path, source_id=path.stem, title=path.stem)
        if not doc.success:
            print(f"FAIL {path.name}: {doc.error}", file=sys.stderr)
            continue
        records = []
        for ch in doc.chunks:
            records.append(
                {
                    "chunk_id": f"{doc.source_id}::c{ch.chunk_index}",
                    "source_id": doc.source_id,
                    "source_type": "markdown",
                    "title": doc.title,
                    "text": ch.text,
                    "page": ch.page,
                    "section": ch.section,
                    "url": None,
                    "metadata": {
                        "char_start": ch.char_start,
                        "char_end": ch.char_end,
                        "sample": True,
                    },
                }
            )
        n = ks.index_records(records)
        total += n
        print(f"Indexed {n:3d} chunks ← {path.name}")

    print(f"Done. store_count={ks.count()} total_upserted={total}")
    print(f"VECTOR_DB_PATH={db_path}")
    print("Next: start API with same VECTOR_DB_PATH and GET /v1/knowledge/status")


if __name__ == "__main__":
    main()
