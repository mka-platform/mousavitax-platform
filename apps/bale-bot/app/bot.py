"""Bale messenger bot — thin adapter to API Gateway (skeleton).

When BALE_BOT_TOKEN is issued by Bale, wire official Bot API long-poll/webhook
to the same handlers used by Telegram (RAG + contact routing).
"""

from __future__ import annotations

import logging
import os

import httpx
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mousavitax.bale")

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")
BALE_BOT_TOKEN = os.getenv("BALE_BOT_TOKEN", "")
ADVISOR_PHONE = "09153068322"


async def ask_backend(query: str) -> dict:
    async with httpx.AsyncClient(timeout=90.0) as client:
        r = await client.post(
            f"{BACKEND_URL}/v1/rag/query",
            json={"query": query, "top_k": 5},
        )
        r.raise_for_status()
        return r.json()


async def health() -> dict:
    async with httpx.AsyncClient(timeout=8.0) as client:
        r = await client.get(f"{BACKEND_URL}/health")
        r.raise_for_status()
        return r.json()


def format_rag(data: dict) -> str:
    answer = data.get("answer") or "پاسخی دریافت نشد."
    cites = data.get("citations") or []
    text = answer
    if cites:
        text += "\n\n📚 منابع:\n"
        for i, c in enumerate(cites[:8], 1):
            text += f"{i}. {c.get('title') or c.get('source_id')}\n"
    text += (
        "\n\n—\n⚠️ پیشنهاد سیستمی؛ جایگزین مشاور رسمی نیست. "
        f"تماس: {ADVISOR_PHONE}"
    )
    return text[:3900]


def main() -> None:
    if not BALE_BOT_TOKEN:
        raise RuntimeError(
            "BALE_BOT_TOKEN تنظیم نشده. پس از دریافت توکن بله در .env قرار دهید.\n"
            "تا آن زمان از ربات تلگرام @taxiran1395_bot استفاده کنید."
        )
    logger.info("Bale bot token present — implement official Bale long-poll/webhook.")
    logger.info("Backend: %s", BACKEND_URL)
    logger.info("Helpers ready: ask_backend(), health(), format_rag()")
    # TODO: Bale Bot API getUpdates loop → ask_backend → sendMessage


if __name__ == "__main__":
    main()
