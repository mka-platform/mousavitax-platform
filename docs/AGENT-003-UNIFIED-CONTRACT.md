# AGENT-003

Shared contract for all clients:

- status
- answer
- citations
- actions
- trace_id

Tax questions are routed to MKA-Core. Its response and citations are passed through without rewriting.

Unknown intent must return CLARIFICATION_REQUIRED.

Citation creation authority belongs only to MKA-Core.
