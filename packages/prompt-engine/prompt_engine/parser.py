"""APCS text parser – extracts /COMMAND blocks into APCSCommand."""

from __future__ import annotations

import re
from typing import Optional

from .models import APCSCommand, EvidenceLevel, OutputFormat

# Match /COMMAND or /COMMAND: value  (value may span lines until next /CMD)
_BLOCK_RE = re.compile(
    r"^/([A-Z][A-Z0-9_-]*)\s*:?\s*(.*)$",
    re.MULTILINE,
)


class APCSParser:
    """Parse APCS command text into structured APCSCommand (Phase 1)."""

    def parse(self, text: str) -> APCSCommand:
        if not text or not text.strip():
            return APCSCommand()

        blocks: dict[str, str] = {}
        current_key: Optional[str] = None
        current_lines: list[str] = []

        for line in text.splitlines():
            m = re.match(r"^/([A-Z][A-Z0-9_-]*)\s*:?\s*(.*)$", line)
            if m:
                if current_key is not None:
                    blocks[current_key] = "\n".join(current_lines).strip()
                current_key = m.group(1).upper()
                rest = m.group(2).strip()
                current_lines = [rest] if rest else []
            else:
                if current_key is not None:
                    current_lines.append(line)
        if current_key is not None:
            blocks[current_key] = "\n".join(current_lines).strip()

        def lines_list(key: str) -> list[str]:
            v = blocks.get(key, "")
            if not v:
                return []
            return [ln.strip().lstrip("-•").strip() for ln in v.splitlines() if ln.strip()]

        fmt_raw = blocks.get("FORMAT", "MARKDOWN").strip().upper()
        try:
            fmt = OutputFormat(fmt_raw)
        except ValueError:
            fmt = OutputFormat.MARKDOWN

        evidence_level = None
        ev = blocks.get("EVIDENCE", "")
        for level in EvidenceLevel:
            if level.value in ev.upper():
                evidence_level = level
                break

        return APCSCommand(
            role=blocks.get("ROLE") or None,
            persona=blocks.get("PERSONA") or None,
            task=blocks.get("TASK") or None,
            objective=blocks.get("OBJECTIVE") or None,
            success=blocks.get("SUCCESS") or None,
            context=blocks.get("CONTEXT") or None,
            input=blocks.get("INPUT") or None,
            evidence=blocks.get("EVIDENCE") or None,
            evidence_level=evidence_level,
            rules=lines_list("RULES"),
            constraints=lines_list("CONSTRAINTS"),
            guardrail=blocks.get("GUARDRAIL") or None,
            method=blocks.get("METHOD") or None,
            perspectives=lines_list("PERSPECTIVES") or lines_list("MULTI-PERSPECTIVE"),
            compare=blocks.get("COMPARE") or None,
            risk=blocks.get("RISK") or None,
            pitfalls=blocks.get("PITFALLS") or None,
            metrics=lines_list("METRICS"),
            format=fmt,
            audience=blocks.get("AUDIENCE") or None,
            tone=blocks.get("TONE") or None,
            decision_rule=blocks.get("DECISION-RULE") or None,
            raw_blocks=blocks,
        )
