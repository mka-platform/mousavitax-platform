from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timezone

class Role(str, Enum):
    PLATFORM_OWNER="PLATFORM_OWNER"; PLATFORM_ADMIN="PLATFORM_ADMIN"
    CONSULTANT="CONSULTANT"; OFFICE_MANAGER="OFFICE_MANAGER"
    OFFICE_STAFF="OFFICE_STAFF"; PLATFORM_STAFF="PLATFORM_STAFF"
    CLIENT="CLIENT"; AUDITOR="AUDITOR"

class AuditEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    actor_type: str
    actor_id: str | None = None
    action: str
    resource_type: str
    resource_id: str | None = None
    trace_id: str
    outcome: str
    metadata: dict = Field(default_factory=dict)
