from __future__ import annotations

def validate_evidence(citations: list[dict]) -> dict:
    valid = [c for c in citations if c.get("source_id") and c.get("title")]
    return {
        "passed": bool(valid),
        "human_review_required": True,
        "reason": "evidence_present" if valid else "insufficient_evidence",
    }
