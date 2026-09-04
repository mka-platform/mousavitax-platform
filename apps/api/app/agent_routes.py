"""Optional HTTP boundary for MousaviTax agents.
Wire this router into the application's FastAPI composition when the API package enables agent routes.
"""
from __future__ import annotations
from pydantic import BaseModel

class AgentQuery(BaseModel):
    text: str
    actor_id: str | None = None
    case_id: str | None = None

def build_agent_router():
    from fastapi import APIRouter
    from agent_core.orchestrator import AgentOrchestrator, AgentRequest
    router = APIRouter(prefix="/agents", tags=["agents"])
    orchestrator = AgentOrchestrator()

    @router.post("/route")
    def route_agent(query: AgentQuery):
        result = orchestrator.route(AgentRequest(text=query.text, actor_id=query.actor_id, case_id=query.case_id))
        return result.__dict__

    return router
