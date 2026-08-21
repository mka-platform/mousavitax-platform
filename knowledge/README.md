# knowledge

مخزن دانش رسمی پلتفرم (قوانین، بخشنامه‌ها، آراء، دستورالعمل‌ها).

## مسیرها

| مسیر | نقش |
|------|-----|
| `domains/iran-tax/knowledge/` | نمونه‌های Markdown اولیه |
| `knowledge/official/` | **ورود دستی** PDF/DOCX رسمی |
| `knowledge/drive_mirror/` | خروجی `sync_drive_knowledge.py` از Google Drive |
| `knowledge/drive_manifest.json` | شناسه پوشه‌ها / فایل‌های Drive |

## Drive مالک

- PRIMARY: `1Jx0cipUqQyGnJk4hFCURzWIg1Abo1Del`
- FALLBACK: `1NcBkZOTemmVfnNKY7FgxuqbIXj6f4Dtl`

## ایندکس

```bash
python scripts/sync_drive_knowledge.py   # اختیاری — نیاز به Service Account
python scripts/seed_knowledge.py
```

## نکات
- فقط منابع تأییدشده؛ Citation اجباری
- دانش پرونده خصوصی مودی اینجا نیاید
