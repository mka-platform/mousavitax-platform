# دانش رسمی (ورود محلی)

فایل‌های PDF / DOCX / MD تأییدشده را اینجا قرار دهید؛ سپس:

```bash
python scripts/seed_knowledge.py
```

## پوشه‌های Drive مرجع (مالک پروژه)

| نقش | Folder ID |
|-----|-----------|
| PRIMARY (آفلاین اصلی) | `1Jx0cipUqQyGnJk4hFCURzWIg1Abo1Del` |
| FALLBACK / ساختار قوانین | `1NcBkZOTemmVfnNKY7FgxuqbIXj6f4Dtl` |
| Registry folder | `1LmVU0WnD_-qlzs8Upv2HkpI-dYrUfkqg` |

همگام‌سازی خودکار: `python scripts/sync_drive_knowledge.py`  
(نیاز به `GOOGLE_SERVICE_ACCOUNT_JSON` یا دانلود دستی)
