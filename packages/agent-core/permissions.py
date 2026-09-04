from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class AgentActor:
    actor_id: str
    role: str

class PermissionDenied(PermissionError):
    pass

class PermissionGate:
    WRITE_ROLES = {"platform_admin", "office_manager", "tax_advisor"}

    def assert_read(self, actor: AgentActor | None) -> None:
        if actor is None or not actor.actor_id:
            raise PermissionDenied("authenticated actor is required")

    def assert_write_allowed(self, actor: AgentActor | None) -> None:
        self.assert_read(actor)
        if actor.role not in self.WRITE_ROLES:
            raise PermissionDenied("actor is not permitted for operational write actions")
