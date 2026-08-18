"""APCS command validator (Phase 1–3)."""

from __future__ import annotations

from .models import APCSCommand, ValidationResult


class APCSValidator:
    def validate(self, cmd: APCSCommand, require_task: bool = False) -> ValidationResult:
        errors: list[str] = []
        warnings: list[str] = []

        if require_task and not cmd.task and not cmd.input_text:
            errors.append("MISSING_TASK_OR_INPUT")

        # Weight check if present in raw SCORE/WEIGHT blocks (future structured parse)
        weight_block = cmd.raw_blocks.get("WEIGHT", "")
        if weight_block and "%" in weight_block:
            total = 0.0
            for part in weight_block.replace(",", "\n").splitlines():
                part = part.strip()
                if ":" in part and "%" in part:
                    try:
                        total += float(part.split(":")[-1].replace("%", "").strip())
                    except ValueError:
                        warnings.append(f"UNPARSEABLE_WEIGHT:{part}")
            if total and abs(total - 100.0) > 0.5:
                errors.append("INVALID_WEIGHT_TOTAL")

        if cmd.format is None:
            warnings.append("DEFAULT_FORMAT_MARKDOWN")

        return ValidationResult(ok=len(errors) == 0, errors=errors, warnings=warnings)
