import pytest
from agent_core.permissions import AgentActor, PermissionDenied, PermissionGate
from agent_core.audit import AuditLogger


def test_actor_required_for_agent_read():
    with pytest.raises(PermissionDenied):
        PermissionGate().assert_read(None)


def test_platform_staff_role_is_read_safe():
    PermissionGate().assert_read(AgentActor("staff-1", "platform_staff"))


def test_operational_write_is_restricted():
    with pytest.raises(PermissionDenied):
        PermissionGate().assert_write_allowed(AgentActor("staff-1", "platform_staff"))


def test_agent_actions_are_auditable():
    audit = AuditLogger()
    audit.record("agent.tool.list_cases", "staff-1", "office-agent", count=1)
    assert len(audit.export()) == 1
