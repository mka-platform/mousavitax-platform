"""APCS command models (Phase 1–3)."""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class EvidenceLevel(str, Enum):
    E0 = "E0"
    E1 = "E1"
    E2 = "E2"
    E3 = "E3"
    E4 = "E4"
    E5 = "E5"


class OutputFormat(str, Enum):
    TEXT = "TEXT"
    TABLE = "TABLE"
    JSON = "JSON"
    MARKDOWN = "MARKDOWN"
    REPORT = "REPORT"
    EXECUTIVE_SUMMARY = "EXECUTIVE_SUMMARY"
    CHECKLIST = "CHECKLIST"
    API_RESPONSE = "API_RESPONSE"
    STRUCTURED_TAX_REPORT = "STRUCTURED_TAX_REPORT"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class APCSCommand(BaseModel):
    role: Optional[str] = None
    persona: Optional[str] = None
    task: Optional[str] = None
    objective: Optional[str] = None
    success: Optional[str] = None
    context: Optional[str] = None
    input_text: Optional[str] = Field(default=None, alias="input")
    evidence: Optional[str] = None
    evidence_level: Optional[EvidenceLevel] = None
    rules: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    guardrail: Optional[str] = None
    method: Optional[str] = None
    analyze: Optional[str] = None
    perspectives: list[str] = Field(default_factory=list)
    compare: Optional[str] = None
    risk: Optional[str] = None
    pitfalls: Optional[str] = None
    assumptions: Optional[str] = None
    metrics: list[str] = Field(default_factory=list)
    verify: bool = False
    self_check: bool = False
    quality_gate: bool = False
    decision: Optional[str] = None
    decision_rule: Optional[str] = None
    format: OutputFormat = OutputFormat.MARKDOWN
    audience: Optional[str] = None
    tone: Optional[str] = None
    exec_summary: bool = False
    domain_id: Optional[str] = None
    raw_blocks: dict[str, str] = Field(default_factory=dict)
    extras: dict[str, Any] = Field(default_factory=dict)

    model_config = {"populate_by_name": True}


class ValidationResult(BaseModel):
    ok: bool = True
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class QualityGateResult(BaseModel):
    passed: bool = True
    status: Optional[str] = None  # INSUFFICIENT_DATA | CONFLICTING_EVIDENCE | ...
    reasons: list[str] = Field(default_factory=list)
