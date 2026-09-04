from __future__ import annotations
from typing import Any
from agent_core.permissions import AgentActor
from agent_core.service_tools import AgentServiceTools
from .agent import OfficeAgent

class OfficeOperations:
    def __init__(self, tools: AgentServiceTools, agent: OfficeAgent | None = None) -> None:
        self.tools = tools
        self.agent = agent or OfficeAgent()

    def daily_summary(self, actor: AgentActor) -> dict[str, Any]:
        cases = self.tools.list_cases(actor)
        clients = self.tools.list_clients(actor)
        deadlines = self.tools.list_deadlines(actor)
        tasks = self.tools.list_tasks(actor)
        summary = {
            "active_cases": len(cases),
            "clients": len(clients),
            "upcoming_deadlines": len(deadlines),
            "unassigned_tasks": len([t for t in tasks if not t.get("assignee_id")]),
        }
        suggestions = [s.__dict__ for s in self.agent.analyze(summary)]
        return {"summary": summary, "suggestions": suggestions, "automation": "read_and_suggest"}
