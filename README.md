# MousaviTax Platform (MKA / ARYA Holding)

پلتفرم مشاوره مالیاتی هوشمند ایران — هسته MKA + APCS + کانال‌های وب/تلگرام/بله + بازار مشاوران + **موتور بخشودگی جرائم**.

**هشدار:** جایگزین مشاور رسمی مالیاتی یا وکیل نیست.

## ساختار

```text
apps/api          FastAPI — RAG + APCS + /v1/tax/waiver/*
apps/web          Next.js RTL — چت، مشاوران، خدمات، /waiver
apps/telegram-bot · apps/bale-bot · apps/admin
packages/taxlaw-engine   محاسبه بخشودگی (۲۰۰/۱۴۰۴/۵۰۴)
packages/knowledge-core · prompt-engine · retrieval-engine · …
domains/iran-tax/
templates/contracts/
docs/ops/
```

## اجرای سریع API

```bash
cd apps/api
pip install -r requirements.txt
# از ریشه مخزن:
PYTHONPATH=../../packages/shared:../../packages/ai-gateway/app:../../packages/taxlaw-engine \
  uvicorn app.main:app --reload --port 8000
```

- Health: `GET /health`
- بخشودگی: `POST /v1/tax/waiver/calculate`
- Meta: `GET /v1/tax/waiver/meta`
- Smoke: `GET /v1/tax/waiver/smoke`

## وب

```bash
cd apps/web
npm install
# اختیاری: NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
```

صفحات: `/` · `/chat` · `/waiver` · `/advisors` · `/services`

## مشاور انسانی

ضیاءالدین موسوی جراحی — ۰۹۱۵۳۰۶۸۳۲۲

ایمیل مدیر: ziya.mka2026@gmail.com


## دانش و ایندکس

```bash
# 1) اختیاری — همگام Drive (Service Account)
export GOOGLE_SERVICE_ACCOUNT_JSON=/path/to/sa.json
python scripts/sync_drive_knowledge.py

# 2) یا کپی دستی PDF رسمی در knowledge/official/

# 3) ایندکس
export EMBEDDING_PROVIDER=fallback   # یا ollama
export VECTOR_DB_PATH=$PWD/data/iran_tax_vectors.json
python scripts/seed_knowledge.py
```
