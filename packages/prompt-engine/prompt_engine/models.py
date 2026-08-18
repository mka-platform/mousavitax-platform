"""APCS command models (Phase 1 + extensible fields)."""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class EvidenceLevel(str, Enum):
    E0 = "E0"  # no evidence
    E1 = "E1"  # user claim
    E2 = "E2"  # raw data
    E3 = "E3"  # provided document
    E4 = "E4"  # official source
    E5 = "E5"  # multi-confirmed official


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


class APCSCommand(BaseModel):
    """Parsed APCS command – Phase 1 core fields + optional extensions."""

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
    perspectives: list[str] = Field(default_factory=list)
    compare: Optional[str] = None
    risk: Optional[str] = None
    pitfalls: Optional[str] = None
    metrics: list[str] = Field(default_factory=list)
    format: OutputFormat = OutputFormat.MARKDOWN
    audience: Optional[str] = None
    tone: Optional[str] = None
    decision_rule: Optional[str] = None
    domain_id: Optional[str] = None
    raw_blocks: dict[str, str] = Field(default_factory=dict)
    extras: dict[str, Any] = Field(default_factory=dict)

    model_config = {"populate_by_name": True}
