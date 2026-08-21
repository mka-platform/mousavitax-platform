# ADR-007: Hybrid AI Tax Platform (پس از Benchmark نما)

## وضعیت
Accepted — 2026-08-21

## زمینه
Benchmark محصول نما نشان داد Marketplace و خدمت‌محوری لازم است؛ اما هویت MousaviTax باید AI-Native باشد نه کلون واسط.

## تصمیم
1. محصول = **AI Tax Platform** (نه فقط Advisor chatbot).
2. جریان پیش‌فرض: **Triage → RAG/APCS → اختیاری Expert**.
3. واحد کار اصلی کاربر: **Tax Case** + **Service Request**.
4. درآمد: Freemium → AI Premium → AI+Expert → Case کامل.
5. Knowledge فقط از منابع رسمی/اعتبارسنجی‌شده.
6. امنیت: RBAC، Audit، جداسازی داده پرونده.

## پیامدها
- Backlog P0 شامل Case، Catalog، Triage، Marketplace، Calendar، Ticket.
- ربات‌ها و وب فقط کانال ورود به همین موتور هستند.
