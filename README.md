# MousaviTax Platform (MKA Holding)

**هلدینگ پلتفرم دانش‌محور — دامنه اول: مشاوره و خدمات مالیاتی هوشمند ایران**

> هستهٔ Domain-Agnostic (MKA) + Vertical مالیاتی + قابلیت گسترش به حوزه‌های دیگر

سازمان: [mka-platform](https://github.com/mka-platform)  
مرجع یکپارچهٔ اهداف **MKA-Core** و **MousaviTax Platform**

---

## چشم‌انداز هلدینگ

این مخزن **منبع حقیقت واحد** است:

| لایه | نقش |
|------|------|
| **Core (MKA)** | RAG، Citation، Parser، Embedding، AI Gateway، API Gateway — مستقل از دامنه |
| **Vertical: Iran Tax** | دانش رسمی مالیاتی، taxlaw-engine، بازار مشاوران، اظهارنامه، لایحه |
| **Future Verticals** | حقوقی، حسابداری، پزشکی، آموزش، ... از طریق `domains/` و Prompt/Collection جدا |

اصول: Knowledge First · Citation اجباری · Human-in-the-loop · Temporal Validity · Zero Fabrication · Modular & Extensible

---

## ساختار Monorepo

```text
mousavitax-platform/
├── packages/                 # هسته مشترک (Domain-Agnostic)
│   ├── shared/               # مدل‌ها و قراردادها (ADR-002)
│   ├── document-parser/
│   ├── embedding-service/
│   ├── retrieval-engine/
│   ├── ai-gateway/
│   ├── knowledge-core/       # orchestration دانش
│   ├── taxlaw-engine/        # موتور لایحه (دامنه مالیات)
│   └── prompt-engine/
├── apps/
│   ├── api/                  # FastAPI – API Gateway
│   ├── web/                  # Next.js + RTL (بازار + چت)
│   ├── telegram-bot/         # @taxiran1395_bot
│   └── admin/
├── services/
│   ├── crawler/
│   ├── google-drive-sync/
│   └── source-bridge/
├── domains/
│   └── iran-tax/             # دانش، پرامپت‌ها، config دامنه مالیات
├── knowledge/                # مخزن اسناد خام (اختیاری)
├── docs/                     # Vision, Architecture, ADRs, Roadmap
├── infra/                    # Docker Compose
└── scripts/
```

---

## اهداف یکپارچه‌شده

### از MKA-Core
- هسته ماژولار دانش‌محور
- RAG + Citation
- Google Drive Sync، Document Parser، Embedding، Retrieval
- API Gateway، Telegram Bot، Admin Panel
- Domain-Agnostic برای گسترش به حوزه‌های دیگر

### از MousaviTax
- مشاوره هیبریدی (انسان + AI)
- خدمات عملیاتی: اظهارنامه، لایحه دفاعیه، سامانه مودیان
- بازار مشاوران (الهام از namatsp)
- انطباق با قوانین و رویه‌های مالیاتی ایران
- Temporal Validity روی دانش رسمی

---

## راه‌اندازی سریع

```bash
cp .env.example .env
# TELEGRAM_BOT_TOKEN، کلید LLM را پر کنید

# API
cd apps/api && pip install -r requirements.txt && uvicorn app.main:app --reload --port 8000

# ربات (ترمینال جدا)
cd apps/telegram-bot && pip install -r requirements.txt && python -m app.bot
```

یا با Docker:

```bash
docker compose -f infra/docker-compose.yml up --build
```

---

## وضعیت

- [x] یکپارچه‌سازی چشم‌انداز هلدینگ + ADRها
- [x] packages: shared, document-parser, embedding, retrieval, ai-gateway
- [x] apps/api (FastAPI Gateway) + apps/telegram-bot
- [x] domains/iran-tax (پرامپت و config اولیه)
- [ ] ایندکس دانش رسمی + pgvector production
- [ ] apps/web (Next.js RTL MVP)
- [ ] taxlaw-engine کامل + پنل مشاوران

جزئیات: [`docs/03_ROADMAP.md`](docs/03_ROADMAP.md)

---

## پیش‌نیازها

1. توکن ربات `@taxiran1395_bot`
2. کلید LLM (Ollama / Gemini / OpenAI-compatible)
3. (اختیاری) Google Service Account برای Drive Sync

---

**نگهدارنده:** ziya1346 · **ایمیل:** ziya.mka2026@gmail.com  
این پلتفرم جایگزین مشاور رسمی یا وکیل نیست.
