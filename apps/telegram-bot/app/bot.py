"""Telegram Bot – @taxiran1395_bot (thin adapter → MousaviTax API Gateway).

Waiver calculator stays on the web UI; this bot focuses on RAG Q&A + routing to human channels.
"""

from __future__ import annotations

import logging
import os

import httpx
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("mousavitax.telegram")

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
WEB_PUBLIC_URL = os.getenv("WEB_PUBLIC_URL", "http://localhost:3000")
ADVISOR_PHONE = "09153068322"
DISCLAIMER = (
    "\n\n—\n⚠️ پیشنهاد سیستمی است و جایگزین مشاور رسمی/رأی سازمان نیست. "
    "HUMAN_REVIEW_REQUIRED · تماس: " + ADVISOR_PHONE
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    user = update.effective_user
    name = (user.first_name if user else "") or ""
    await update.message.reply_text(
        f"سلام {name} 👋\n\n"
        "دستیار مالیاتی *MousaviTax* (هسته MKA)\n\n"
        "سوال مالیاتی بپرسید تا با استناد از دانش ایندکس‌شده پاسخ داده شود.\n\n"
        "/help – راهنما\n"
        "/status – وضعیت API\n"
        "/contact – مشاور حقیقی/حقوقی\n"
        "/jobs – استخدام\n"
        "/web – لینک وب\n\n"
        f"مشاور رسمی: ضیاءالدین موسوی جراحی — {ADVISOR_PHONE}",
        parse_mode="Markdown",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    await update.message.reply_text(
        "📖 راهنما\n\n"
        "• متن آزاد بفرستید → پاسخ RAG با منبع\n"
        "• بخشودگی جرائم روی وب: /web و مسیر /waiver\n"
        "• ارتباط با مشاورین حقیقی و حقوقی: /contact\n"
        "• درخواست استخدام: /jobs\n\n"
        "مثال پرسش:\n"
        "نرخ ارزش افزوده چیست؟\n"
        "اعتراض به برگ تشخیص چگونه است؟"
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            r = await client.get(f"{BACKEND_URL}/health")
            data = r.json()
            k = await client.get(f"{BACKEND_URL}/v1/knowledge/status")
            kd = k.json() if k.status_code == 200 else {}
        await update.message.reply_text(
            "✅ سرویس فعال\n"
            f"وضعیت: {data.get('status')}\n"
            f"نسخه API: {data.get('version')}\n"
            f"قطعات دانش: {kd.get('chunks', data.get('knowledge_chunks', '?'))}\n"
            f"Backend: {BACKEND_URL}"
        )
    except Exception as e:
        logger.error("Health check failed: %s", e)
        await update.message.reply_text(
            f"❌ Backend در دسترس نیست ({BACKEND_URL}).\nAPI را روی پورت 8000 اجرا کنید."
        )


async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    await update.message.reply_text(
        "ارتباط با مشاورین حقیقی و حقوقی\n\n"
        f"📞 {ADVISOR_PHONE}\n"
        "ضیاءالدین موسوی جراحی — مشاور رسمی مالیاتی\n\n"
        f"فرم وب (اعتبارسنجی مدارک): {WEB_PUBLIC_URL}/advisors\n"
        "مدارک و عناوین پس از بررسی انسان تأیید می‌شوند."
    )


async def jobs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    await update.message.reply_text(
        "درخواست کار و استخدام\n\n"
        f"فرم ارسال رزومه: {WEB_PUBLIC_URL}/careers\n"
        f"یا تماس: {ADVISOR_PHONE}"
    )


async def web(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    await update.message.reply_text(
        f"🌐 وب MousaviTax\n{WEB_PUBLIC_URL}\n"
        f"بخشودگی: {WEB_PUBLIC_URL}/waiver\n"
        f"چت: {WEB_PUBLIC_URL}/chat\n"
        f"مشاورین: {WEB_PUBLIC_URL}/advisors\n"
        f"استخدام: {WEB_PUBLIC_URL}/careers"
    )


def _truncate(text: str, limit: int = 3900) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 20] + "\n\n[ادامه کوتاه شد]"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return
    query = update.message.text.strip()
    if not query:
        return

    await update.message.chat.send_action(action="typing")
    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            payload = {"query": query, "top_k": 5}
            r = await client.post(f"{BACKEND_URL}/v1/rag/query", json=payload)
            r.raise_for_status()
            data = r.json()

        answer = data.get("answer") or "پاسخی دریافت نشد."
        citations = data.get("citations") or []
        text = answer
        if citations:
            text += "\n\n📚 منابع:\n"
            for i, c in enumerate(citations[:8], 1):
                title = c.get("title") or c.get("source_id") or "منبع"
                text += f"{i}. {title}\n"
        text += DISCLAIMER
        await update.message.reply_text(_truncate(text))
    except httpx.HTTPError as e:
        logger.error("Backend error: %s", e)
        await update.message.reply_text(
            "⚠️ خطا در ارتباط با سرویس دانش. API را چک کنید یا کمی بعد تلاش کنید.\n"
            f"تماس اضطراری مشاور: {ADVISOR_PHONE}"
        )
    except Exception:
        logger.exception("Unexpected error")
        await update.message.reply_text("خطای داخلی رخ داد.")


def main() -> None:
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN تنظیم نشده. توکن @taxiran1395_bot را در .env قرار دهید."
        )
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("contact", contact))
    application.add_handler(CommandHandler("jobs", jobs))
    application.add_handler(CommandHandler("web", web))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )
    logger.info("Starting MousaviTax Telegram Bot → %s", BACKEND_URL)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
