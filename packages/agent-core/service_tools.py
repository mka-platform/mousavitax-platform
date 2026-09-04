from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Protocol
from .permissions import AgentActor, PermissionGate
from .audit import AuditLogger

class PlatformServiceClient(Protocol):
    def get_case(self, case_id: str, actor_id: str) -> dict[str, Any]: ...
    def list_cases(self, actor_id: str) -> list[dict[str, Any]]: ...
    def list_clients(self, actor_id: str) -> list[dict[str, Any]]: ...
    def list_deadlines(self, actor_id: str) -> list[dict[str, Any]]: ...
    def list_tasks(self, actor_id: str) -> list[dict[str, Any]]: ...

@dataclass
class AgentServiceTools:
    client: PlatformServiceClient
    gate: PermissionGate
    audit: AuditLogger

    def list_cases(self, actor: AgentActor) -> list[dict[str, Any]]:
        self.gate.assert_read(actor)
        data = self.client.list_cases(actor.actor_id)
        self.audit.record("agent.tool.list_cases", actor.actor_id, "office-agent", count=len(data))
        return data

    def get_case(self, actor: AgentActor, case_id: str) -> dict[str, Any]:
        self.gate.assert_read(actor)
        data = self.client.get_case(case_id, actor.actor_id)
        self.audit.record("agent.tool.get_case", actor.actor_id, "case-agent", case_id=case_id)
        return data

    def list_clients(self, actor: AgentActor) -> list[dict[str, Any]]:
        self.gate.assert_read(actor)
        return self.client.list_clients(actor.actor_id)

    def list_deadlines(self, actor: AgentActor) -> list[dict[str, Any]]:
        self.gate.assert_read(actor)
        return self.client.list_deadlines(actor.actor_id)

    def list_tasks(self, actor: AgentActor) -> list[dict[str, Any]]:
        self.gate.assert_read(actor)
        return self.client.list_tasks(actor.actor_id)
