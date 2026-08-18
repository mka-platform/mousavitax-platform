"""Quality gate before accepting model output as final."""

from __future__ import annotations

from typing import Any, Optional, Sequence

from .models import APCSCommand, QualityGateResult


class QualityGate:
    """Structural checks; does not re-call the LLM."""

    def evaluate(
        self,
        cmd: APCSCommand,
        answer: str,
        retrieved: Optional[Sequence[dict[str, Any]]] = None,
        require_retrieval: bool = False,
    ) -> QualityGateResult:
        reasons: list[str] = []
        retrieved = retrieved or []

        if require_retrieval and not retrieved:
            return QualityGateResult(
                passed=False,
                status="INSUFFICIENT_DATA",
                reasons=["No retrieved evidence for legal/tax claim path"],
            )

        if cmd.quality_gate or cmd.verify:
            if not answer or not answer.strip():
                return QualityGateResult(
                    passed=False,
                    status="INSUFFICIENT_DATA",
                    reasons=["Empty model answer"],
                )
            # Soft signal: model admitted lack of data
            upper = answer.upper()
            for token in (
                "INSUFFICIENT_DATA",
                "CONFLICTING_EVIDENCE",
                "HUMAN_REVIEW_REQUIRED",
            ):
                if token in upper:
                    return QualityGateResult(
                        passed=True,
                        status=token,
                        reasons=["Model reported controlled status"],
                    )

        if cmd.self_check:
            reasons.append("SELF_CHECK_REQUESTED_IN_PROMPT")

        return QualityGateResult(passed=True, status=None, reasons=reasons)
