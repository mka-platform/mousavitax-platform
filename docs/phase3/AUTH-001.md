# AUTH-001 Authentication & JWT

Authentication uses short-lived access tokens and refresh tokens. Secrets are environment variables only.

Required claims: sub, roles, token_type, jti, iat, exp.

Rules:
- Passwords are stored only as strong hashes.
- Refresh tokens are rotated and revocable.
- Protected endpoints require a valid access token.
- trace_id is attached to security-relevant requests.
