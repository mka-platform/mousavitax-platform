#!/usr/bin/env python3
"""Seed iran-tax knowledge into the vector store.

Sources (in order):
  1) domains/iran-tax/knowledge/*.md   (sample / curated markdown)
  2) knowledge/official/**            (official PDFs/DOCX/MD drop zone)
  3) knowledge/drive_mirror/**        (from scripts/sync_drive_knowledge.py)

Usage (repo root):
  export EMBEDDING_PROVIDER=fallback   # or ollama
  export VECTOR_DB_PATH=$PWD/data/iran_tax_vectors.json
  python scripts/sync_drive_knowledge.py   # optional
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

SAMPLE_DIR = ROOT / "domains" / "iran-tax" / "knowledge"
OFFICIAL_DIR = ROOT / "knowledge" / "official"
MIRROR_DIR = ROOT / "knowledge" / "drive_mirror"

EXTS = {".md", ".txt", ".pdf", ".docx"}


def iter_files() -> list[tuple[Path, str, bool]]:
    """Return list of (path, source_tag, is_sample)."""
    out: list[tuple[Path, str, bool]] = []
    if SAMPLE_DIR.is_dir():
        for f in sorted(SAMPLE_DIR.rglob("*")):
            if f.is_file() and f.suffix.lower() in EXTS and f.name.lower() != "readme.md":
                out.append((f, "sample-md", True))
    for base, tag in ((OFFICIAL_DIR, "official"), (MIRROR_DIR, "drive")):
        if not base.is_dir():
            continue
        for f in sorted(base.rglob("*")):
            if f.is_file() and f.suffix.lower() in EXTS and f.name.lower() != "readme.md":
                out.append((f, tag, False))
    return out


def main() -> None:
    os.environ.setdefault("EMBEDDING_PROVIDER", "fallback")
    db_path = os.environ.get("VECTOR_DB_PATH") or str(ROOT / "data" / "iran_tax_vectors.json")
    os.environ["VECTOR_DB_PATH"] = db_path
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    ks = KnowledgeService(persist_path=db_path)
    parser = DocumentParser(chunk_size=900, chunk_overlap=150)

    files = iter_files()
    if not files:
        print(
            "No knowledge files found.\n"
            "  - Add markdown under domains/iran-tax/knowledge/\n"
            "  - Or PDFs under knowledge/official/\n"
            "  - Or run scripts/sync_drive_knowledge.py",
            file=sys.stderr,
        )
        sys.exit(1)

    total = 0
    failed = 0
    for path, tag, is_sample in files:
        rel = path.relative_to(ROOT)
        source_id = f"{tag}:{path.stem}"[:120]
        title = path.stem.replace("_", " ")
        doc = parser.parse_file(path, source_id=source_id, title=title)
        if not doc.success:
            print(f"FAIL {rel}: {doc.error}", file=sys.stderr)
            failed += 1
            continue
        records = []
        for ch in doc.chunks:
            records.append(
                {
                    "chunk_id": f"{doc.source_id}::c{ch.chunk_index}",
                    "source_id": doc.source_id,
                    "source_type": doc.source_type,
                    "title": doc.title,
                    "text": ch.text,
                    "page": ch.page,
                    "section": ch.section,
                    "url": None,
                    "metadata": {
                        "char_start": ch.char_start,
                        "char_end": ch.char_end,
                        "sample": is_sample,
                        "path": str(rel),
                        "origin": tag,
                        "official": not is_sample,
                    },
                }
            )
        n = ks.index_records(records)
        total += n
        flag = "sample" if is_sample else "OFFICIAL"
        print(f"[{flag}] {n:3d} chunks ← {rel}")

    print(f"Done. store_count={ks.count()} upserted={total} failed={failed}")
    print(f"VECTOR_DB_PATH={db_path}")
    print("Next: uvicorn apps.api with same VECTOR_DB_PATH → GET /v1/knowledge/status")


if __name__ == "__main__":
    main()
