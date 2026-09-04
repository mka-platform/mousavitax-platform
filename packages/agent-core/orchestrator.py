from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from .policies import DEFAULT_POLICY, AgentPolicy

@dataclass
class AgentRequest:
    text: str
    actor_id: str | None = None
    case_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class AgentResult:
    route: str
    message: str
    suggestions: list[str] = field(default_factory=list)
    human_review_required: bool = True
    audit: dict[str, Any] = field(default_factory=dict)

class AgentOrchestrator:
    """Safe router. Agents suggest actions; services enforce authorization."""
    def __init__(self, policy: AgentPolicy = DEFAULT_POLICY) -> None:
        self.policy = policy

    def route(self, request: AgentRequest) -> AgentResult:
        text = request.text.lower()
        if any(k in text for k in ("مهلت", "deadline", "سررسید")):
            route = "deadline-agent"
        elif any(k in text for k in ("پرونده", "case")):
            route = "case-agent"
        elif any(k in text for k in ("وظیفه", "کار", "task")):
            route = "office-agent"
        else:
            route = "platform-agent"
        return AgentResult(
            route=route,
            message="درخواست به عامل تخصصی مناسب ارجاع شد.",
            suggestions=["خروجی‌های عملیاتی ابتدا به‌صورت پیشنهاد ارائه می‌شوند."],
            audit={"actor_id": request.actor_id, "case_id": request.case_id, "policy": self.policy.name},
        )
