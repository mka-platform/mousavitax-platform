# AUDIT-001 Immutable Audit Trail

Every security or state-changing operation creates an append-only audit event:
- event_id
- timestamp
- actor_type
- actor_id
- action
- resource_type
- resource_id
- trace_id
- outcome
- metadata

Audit records are never updated in place by application workflows.
