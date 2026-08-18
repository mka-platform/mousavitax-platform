"""Bale messenger bot skeleton — thin adapter to API Gateway.

Implement with official Bale Bot API when token is available.
Contract mirrors apps/telegram-bot: start/help/status + text → /v1/rag/query.
"""

from __future__ import annotations

import logging
import os

import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mousavitax.bale")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
BALE_BOT_TOKEN = os.getenv("BALE_BOT_TOKEN", "")


async def ask_backend(query: str, user_id: str | None = None) -> dict:
    async with httpx.AsyncClient(timeout=60.0) as client:
        r = await client.post(
            f"{BACKEND_URL}/v1/rag/query",
            json={"query": query, "user_id": user_id, "top_k": 5},
        )
        r.raise_for_status()
        return r.json()


def main() -> None:
    if not BALE_BOT_TOKEN:
        raise RuntimeError(
            "BALE_BOT_TOKEN تنظیم نشده. پس از دریافت توکن بله در .env قرار دهید."
        )
    logger.info("Bale bot skeleton — wire official Bale SDK/webhook here.")
    logger.info("Backend: %s", BACKEND_URL)
    # TODO: register webhook / long-poll with Bale API and call ask_backend


if __name__ == "__main__":
    main()
