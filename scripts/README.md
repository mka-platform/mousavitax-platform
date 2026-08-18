# scripts

## seed_knowledge.py

ایندکس اسناد نمونه `domains/iran-tax/knowledge/*.md` در vector store.

```bash
cd /path/to/mousavitax-platform
export EMBEDDING_PROVIDER=fallback
export VECTOR_DB_PATH=$PWD/data/iran_tax_vectors.json
python scripts/seed_knowledge.py
```

سپس API را با همان `VECTOR_DB_PATH` اجرا کنید تا Citation واقعی برگردد.
