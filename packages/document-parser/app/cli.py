"""CLI for testing Document Parser locally."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow running as python -m app.cli from packages/document-parser
try:
    from .parser import DocumentParser
except ImportError:
    from parser import DocumentParser


def main() -> None:
    ap = argparse.ArgumentParser(description="MousaviTax Document Parser")
    ap.add_argument("path", help="Path to PDF/DOCX/TXT file")
    ap.add_argument("--source-id", default=None)
    ap.add_argument("--chunks", action="store_true", help="Print chunks")
    ap.add_argument("--json", action="store_true", help="JSON output")
    args = ap.parse_args()

    parser = DocumentParser()
    doc = parser.parse_file(args.path, source_id=args.source_id)

    if args.json:
        payload = {
            "source_id": doc.source_id,
            "title": doc.title,
            "source_type": doc.source_type,
            "success": doc.success,
            "error": doc.error,
            "page_count": doc.page_count,
            "metadata": doc.metadata,
            "full_text_preview": doc.full_text[:500] if doc.full_text else "",
            "chunk_count": len(doc.chunks),
        }
        if args.chunks:
            payload["chunks"] = [
                {"index": c.chunk_index, "page": c.page, "text": c.text[:200]}
                for c in doc.chunks[:10]
            ]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    if not doc.success:
        print(f"ERROR: {doc.error}", file=sys.stderr)
        sys.exit(1)

    print(f"Title: {doc.title}")
    print(
        f"Type: {doc.source_type} | pages={doc.page_count} | "
        f"chars={len(doc.full_text)} | chunks={len(doc.chunks)}"
    )
    print("--- preview ---")
    print(doc.full_text[:800])
    if args.chunks:
        print("\n--- first chunks ---")
        for c in doc.chunks[:5]:
            print(f"[{c.chunk_index}] page={c.page} | {c.text[:120]}...")


if __name__ == "__main__":
    main()
