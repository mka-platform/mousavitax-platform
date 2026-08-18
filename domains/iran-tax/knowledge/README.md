# دانش نمونه — iran-tax

اسناد **نمونه آموزشی** برای تست RAG و Citation.

> این متون جایگزین متن رسمی کامل قانون نیستند و فقط برای راه‌اندازی pipeline ایندکس استفاده می‌شوند.
> قبل از استفاده تولیدی، متن قوانین و بخشنامه‌های رسمی را جایگزین کنید.

ایندکس:

```bash
# از ریشه مخزن
export VECTOR_DB_PATH=data/iran_tax_vectors.json
export EMBEDDING_PROVIDER=fallback   # یا ollama اگر در دسترس است
python scripts/seed_knowledge.py
```
