# data/

مسیر پیش‌فرض vector store: `iran_tax_vectors.json`

فایل ایندکس معمولاً محلی ساخته می‌شود (حجم embedding). برای تولید از ریشه مخزن:

```bash
export EMBEDDING_PROVIDER=fallback   # یا ollama
export VECTOR_DB_PATH=$PWD/data/iran_tax_vectors.json
python scripts/seed_knowledge.py
```

سپس API:

```bash
export VECTOR_DB_PATH=$PWD/data/iran_tax_vectors.json
export EMBEDDING_PROVIDER=fallback
cd apps/api && uvicorn app.main:app --reload --port 8000
```

وضعیت دانش: `GET /v1/knowledge/status`

اسناد منبع: `domains/iran-tax/knowledge/*.md` (نمونه آموزشی — قبل از production با متن رسمی جایگزین شود).
