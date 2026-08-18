# MousaviTax Platform (MKA / ARYA Holding)

**هلدینگ پلتفرم دانش‌محور — دامنه اول: مشاوره و خدمات مالیاتی هوشمند ایران**

> هسته Domain-Agnostic (MKA) + **APCS Prompt Engine** + Vertical مالیاتی + گسترش به حوزه‌های دیگر

سازمان: [mka-platform](https://github.com/mka-platform)

---

## چشم‌انداز هلدینگ

| لایه | نقش |
|------|------|
| **Core** | RAG، Citation، Parser، Embedding، AI Gateway، **APCS Engine** |
| **Vertical: Iran Tax** | دانش رسمی، taxlaw، بازار مشاوران، اظهارنامه، لایحه |
| **Future Verticals** | حقوقی، حسابداری، Trader، آموزش — فقط Domain Pack جدید |

اصول: Knowledge First · Citation · Human-in-the-loop · Temporal Validity · Zero Fabrication · **APCS Traceable Decision**

استاندارد پرامپت: [`docs/standards/APCS-v1.0.md`](docs/standards/APCS-v1.0.md) · [ADR-006](docs/adr/ADR-006-APCS-Prompt-Engine.md)

---

## ساختار

```text
packages/
  shared/ document-parser/ embedding-service/ retrieval-engine/
  ai-gateway/ prompt-engine/   # APCS Parser + Builder
  knowledge-core/ taxlaw-engine/
apps/
  api/            # FastAPI — /v1/rag/query + /v1/apcs/query
  telegram-bot/
  web/ admin/
domains/
  iran-tax/       # apcs_profile.yaml + prompts
docs/standards/   # APCS-v1.0.md
```

---

## راه‌اندازی سریع

```bash
cp .env.example .env
cd apps/api && pip install -r requirements.txt \
  && pip install -r ../../packages/prompt-engine/requirements.txt \
  && uvicorn app.main:app --reload --port 8000
```

Endpoints:
- `GET /health`
- `POST /v1/rag/query` — پرسش ساده
- `POST /v1/apcs/query` — دستور APCS کامل

---

## وضعیت

- [x] Holding vision + ADR-001…006 (شامل APCS)
- [x] Core packages + prompt-engine Phase 1
- [x] API Gateway + Telegram bot + iran-tax profile
- [ ] Retrieval واقعی روی RAG/APCS
- [ ] apps/web Next.js RTL
- [ ] APCS Phase 2–3 (Risk, Verify, Quality Gate)

**ایمیل:** ziya.mka2026@gmail.com  
جایگزین مشاور رسمی نیست.
