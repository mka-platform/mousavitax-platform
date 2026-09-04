from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class ActionMode(str, Enum):
    READ_ONLY = "read_only"
    SUGGEST = "suggest"
    CONFIRM = "confirm"

@dataclass(frozen=True)
class AgentPolicy:
    name: str = "mousavitax-safe-default"
    action_mode: ActionMode = ActionMode.SUGGEST
    require_ownership_check: bool = True
    require_audit: bool = True
    require_evidence_for_tax_answer: bool = True
    direct_database_access: bool = False

DEFAULT_POLICY = AgentPolicy()
