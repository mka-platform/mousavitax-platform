# shared

انواع مشترک، قراردادها و utilities بین پکیج‌های MousaviTax Platform.

برگرفته از `MKA-Core/packages/shared` و گسترش‌یافته طبق **ADR-002** (مدل داده دانش).

## محتویات

| ماژول | نقش |
|--------|------|
| `mousavitax_shared.models` | SourceDocument، DocumentChunk، Citation، RAG request/response |

## نصب (توسعه)

```bash
cd packages/shared
pip install -e ".[dev]"   # یا اضافه کردن path به PYTHONPATH
```

## وابستگی‌ها

- pydantic >= 2

## وضعیت

منتقل‌شده از MKA-Core — آماده استفاده در knowledge-core و taxlaw-engine.
