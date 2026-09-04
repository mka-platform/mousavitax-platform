from __future__ import annotations
from dataclasses import dataclass

@dataclass
class OfficeSuggestion:
    title: str
    reason: str
    action: str = "suggest"

class OfficeAgent:
    name = "mousavitax-office-agent"

    def analyze(self, summary: dict) -> list[OfficeSuggestion]:
        suggestions: list[OfficeSuggestion] = []
        if summary.get("upcoming_deadlines", 0):
            suggestions.append(OfficeSuggestion("بررسی مهلت‌های نزدیک", "حداقل یک مهلت نزدیک شناسایی شده است."))
        if summary.get("unassigned_tasks", 0):
            suggestions.append(OfficeSuggestion("تخصیص مسئول پرونده", "وظایف بدون مسئول نیازمند بررسی هستند."))
        return suggestions
