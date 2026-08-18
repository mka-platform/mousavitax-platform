"""Build model-facing prompts from APCSCommand + domain profile + retrieved context."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional, Sequence

import yaml

from .models import APCSCommand

REPO_ROOT = Path(__file__).resolve().parents[3]


class PromptBuilder:
    """Compose system + user prompts; does not call the LLM (use ai-gateway)."""

    def __init__(self, domain: str = "iran-tax", domains_root: Optional[Path] = None) -> None:
        self.domain = domain
        self.domains_root = domains_root or (REPO_ROOT / "domains")

    def _load_profile(self) -> dict[str, Any]:
        path = self.domains_root / self.domain / "apcs_profile.yaml"
        if path.exists():
            return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        return {}

    def _load_base_system(self) -> str:
        path = self.domains_root / self.domain / "prompts" / "advisor_system.txt"
        if path.exists():
            return path.read_text(encoding="utf-8").strip()
        return (
            "You are a careful assistant. Cite sources. Do not fabricate facts. "
            "If evidence is insufficient, say so."
        )

    def build(
        self,
        cmd: APCSCommand,
        retrieved_context: Optional[Sequence[dict[str, Any]]] = None,
        user_message: Optional[str] = None,
    ) -> dict[str, str]:
        """
        Returns {"system": ..., "user": ...} ready for AIGateway.generate.
        """
        profile = self._load_profile()
        parts: list[str] = [self._load_base_system()]

        role = cmd.role or profile.get("default_role")
        if role:
            parts.append(f"\n## Role\n{role}")
        if cmd.persona:
            parts.append(f"\n## Persona\n{cmd.persona}")

        rules = list(cmd.rules) or list(profile.get("default_rules") or [])
        # Platform invariants (always on)
        rules.extend(
            [
                "Do not fabricate laws, circulars, or rulings.",
                "Distinguish FACT / SUPPORTED / INFERRED / ASSUMED / UNKNOWN.",
                "If evidence is insufficient, respond with INSUFFICIENT_DATA rather than inventing a conclusion.",
            ]
        )
        if rules:
            parts.append("\n## Rules\n" + "\n".join(f"- {r}" for r in rules))

        if cmd.constraints:
            parts.append(
                "\n## Constraints\n" + "\n".join(f"- {c}" for c in cmd.constraints)
            )
        if cmd.guardrail:
            parts.append(f"\n## Guardrail\n{cmd.guardrail}")
        if cmd.method:
            parts.append(f"\n## Method\n{cmd.method}")
        if cmd.format:
            parts.append(f"\n## Output format\n{cmd.format.value}")

        disclaimer = profile.get("disclaimer")
        if disclaimer:
            parts.append(f"\n## Disclaimer\n{disclaimer}")

        system = "\n".join(parts).strip()

        user_parts: list[str] = []
        if cmd.task:
            user_parts.append(f"## Task\n{cmd.task}")
        if cmd.objective:
            user_parts.append(f"## Objective\n{cmd.objective}")
        if cmd.context:
            user_parts.append(f"## Context\n{cmd.context}")
        if cmd.input_text:
            user_parts.append(f"## Input\n{cmd.input_text}")
        if user_message:
            user_parts.append(f"## User message\n{user_message}")

        if retrieved_context:
            ctx_lines = []
            for i, hit in enumerate(retrieved_context, 1):
                title = hit.get("title") or hit.get("citation", {}).get("title") or ""
                text = hit.get("text") or hit.get("content") or ""
                ctx_lines.append(f"[{i}] {title}\n{text}")
            user_parts.append(
                "## Retrieved evidence (cite by number)\n" + "\n\n".join(ctx_lines)
            )

        if cmd.compare:
            user_parts.append(f"## Compare\n{cmd.compare}")
        if cmd.risk:
            user_parts.append(f"## Risk focus\n{cmd.risk}")

        user = "\n\n".join(user_parts).strip() or (user_message or "")
        return {"system": system, "user": user}
