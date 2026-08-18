# Architecture — MousaviTax Platform

## نمای کلی

پلتفرم به صورت **Monorepo** با معماری ماژولار طراحی شده است تا اهداف پروژه‌های MKA، MousaviTax-AI، TAXLAW-GROK، ALTIP و Tax-AI-Bot را در یک ساختار واحد جمع کند.

```
                    ┌─────────────────────────────┐
                    │        Apps / Clients        │
                    │  Web | Telegram Bot | Admin  │
                    └─────────────┬───────────────┘
                                  │
                    ┌─────────────▼───────────────┐
                    │        API Gateway          │
                    └─────────────┬───────────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         │                        │                        │
┌────────▼────────┐    ┌──────────▼──────────┐   ┌─────────▼─────────┐
│ Knowledge Core  │    │   TaxLaw Engine     │   │  Business Modules │
│ RAG + Citation  │    │  Layeha + Analysis  │   │  (Declaration..)  │
└────────┬────────┘    └──────────┬──────────┘   └─────────┬─────────┘
         │                        │                        │
         └────────────────────────┼────────────────────────┘
                                  │
                    ┌─────────────▼───────────────┐
                    │   Shared Services & Data    │
                    │ Parser | Crawler | Storage  │
                    └─────────────────────────────┘
```

## لایه‌ها

1. **Presentation** — Web (Next.js RTL)، Telegram Bot، Admin Panel
2. **API Gateway** — احراز هویت، rate limiting، orchestration
3. **Domain Modules**
   - Knowledge Core (از MKA)
   - TaxLaw Engine (از TAXLAW-GROK + ALTIP)
   - خدمات کسب‌وکاری (اظهارنامه، لایحه، مودیان)
4. **Infrastructure** — Document Parser، Embedding، Vector DB، Crawler، Google Drive Sync

## اصول طراحی

- Clean Architecture / DDD در ماژول‌های حیاتی
- Citation اجباری برای ادعاهای حقوقی-مالیاتی
- Human-in-the-loop برای خروجی‌های حساس (لایحه نهایی)
- جداسازی کامل دانش رسمی از دانش پرونده
- قابلیت تعویض LLM Provider

## تکنولوژی پیشنهادی (قابل تغییر بر اساس ADR)

| لایه | پیشنهاد |
|------|----------|
| Web | Next.js 15 + TypeScript + Tailwind + shadcn/ui (RTL) |
| API | FastAPI یا NestJS |
| Knowledge / RAG | Python packages از MKA |
| Bot | python-telegram-bot یا Telegraf |
| DB | PostgreSQL + Vector extension |
| Infra | Docker Compose → Kubernetes |
