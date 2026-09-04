from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any

@dataclass
class AuditEvent:
    event_type: str
    actor_id: str | None
    agent: str
    payload: dict[str, Any]
    created_at: str

class AuditLogger:
    """Adapter-friendly audit logger. Persistence can be wired to the platform audit service."""
    def __init__(self) -> None:
        self.events: list[AuditEvent] = []

    def record(self, event_type: str, actor_id: str | None, agent: str, **payload: Any) -> AuditEvent:
        event = AuditEvent(event_type, actor_id, agent, payload, datetime.now(timezone.utc).isoformat())
        self.events.append(event)
        return event

    def export(self) -> list[dict[str, Any]]:
        return [asdict(event) for event in self.events]
