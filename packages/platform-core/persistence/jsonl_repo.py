from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


class JsonlRepository:
    """MVP filesystem store. Swap for SQL without changing service layer."""

    def __init__(self, path: str | Path, audit_path: str | Path | None = None) -> None:
        self.path = Path(path)
        self.audit_path = Path(audit_path) if audit_path else self.path.parent / "audit_events.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _read_all(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        items: list[dict[str, Any]] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return items

    def _write_all(self, items: list[dict[str, Any]]) -> None:
        with self.path.open("w", encoding="utf-8") as f:
            for it in items:
                f.write(json.dumps(it, ensure_ascii=False) + "\n")

    def list(self, filters: Optional[dict[str, Any]] = None) -> list[dict[str, Any]]:
        items = self._read_all()
        if not filters:
            return items
        out = []
        for it in items:
            ok = True
            for k, v in filters.items():
                if v is None:
                    continue
                if it.get(k) != v:
                    ok = False
                    break
            if ok:
                out.append(it)
        return out

    def get(self, id: str) -> Optional[dict[str, Any]]:
        for it in self._read_all():
            if str(it.get("id")) == str(id):
                return it
        return None

    def create(self, entity: dict[str, Any]) -> dict[str, Any]:
        items = self._read_all()
        items.append(entity)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entity, ensure_ascii=False) + "\n")
        return entity

    def update(self, id: str, patch: dict[str, Any]) -> dict[str, Any]:
        items = self._read_all()
        found = None
        for i, it in enumerate(items):
            if str(it.get("id")) == str(id):
                it = {**it, **patch, "updated_at": datetime.now(timezone.utc).isoformat()}
                items[i] = it
                found = it
                break
        if found is None:
            raise KeyError(id)
        self._write_all(items)
        return found

    def append_audit(self, event: dict[str, Any]) -> None:
        self.audit_path.parent.mkdir(parents=True, exist_ok=True)
        if "created_at" not in event:
            event = {
                **event,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        with self.audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
