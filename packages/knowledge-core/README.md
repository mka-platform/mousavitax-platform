# knowledge-core

هسته مدیریت دانش، RAG و Citation پلتفرم (برگرفته از MKA).

## مسئولیت‌ها
- همگام‌سازی منابع دانش (Google Drive، PDF، Markdown و ...)
- استخراج متن و ایندکس‌گذاری معنایی
- جستجوی معنایی با Citation اجباری
- مدیریت چرخه عمر دانش و Temporal Validity

## وابستگی‌ها (پس از migration)
- `packages/shared` — مدل‌های ADR-002
- `packages/document-parser` — استخراج متن
- `packages/retrieval-engine` — (در حال انتقال)

## وضعیت
اسکلت اولیه — `shared` و `document-parser` منتقل شدند؛ retrieval و embedding در مرحله بعد.
