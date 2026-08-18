# ADR-002: Knowledge Data Model

**Status:** Accepted  
**Date:** 2026-08-18  
**Deciders:** Project Owner + Architecture (on behalf of mka-platform)

---

## Context

پلتفرم باید دانش رسمی مالیاتی ایران (قوانین، بخشنامه‌ها، آراء، دستورالعمل‌ها) را با این الزامات مدیریت کند:

- **Citation اجباری** برای هر ادعای مهم
- **Temporal Validity** (تاریخ لازم‌الاجرا شدن، نسخه‌های قبلی، تاریخ انقضا)
- جداسازی دانش رسمی از دانش پرونده کاربر
- قابلیت ردیابی منبع (source_id، نوع منبع، صفحه، بخش)
- سازگاری با مدل‌های موجود در MKA-Core (`DocumentChunk`, `Citation`, `RetrievedChunk`)

بدون مدل داده یکسان، انتقال از MKA و TAXLAW-GROK و کیفیت RAG/Citation دچار پراکندگی می‌شود.

## Decision

مدل داده دانش حول این موجودیت‌های اصلی تعریف می‌شود:

### 1. SourceDocument
سند مبدأ (قانون، بخشنامه، رأی، ...)

| فیلد | توضیح |
|------|--------|
| `source_id` | شناسه یکتا |
| `source_type` | `law` \| `circular` \| `ruling` \| `directive` \| `pdf` \| `markdown` \| ... |
| `title` | عنوان رسمی |
| `official_ref` | شماره/مرجع رسمی (مثلاً شماره بخشنامه) |
| `effective_from` | تاریخ شروع اعتبار (Temporal) |
| `effective_to` | تاریخ پایان اعتبار (nullable) |
| `supersedes` / `superseded_by` | روابط نسخه‌ای |
| `url` / `storage_path` | محل دسترسی |
| `metadata` | فیلدهای اضافی |

### 2. DocumentChunk
قطعه ایندکس‌شده برای بازیابی

| فیلد | توضیح |
|------|--------|
| `chunk_id` | شناسه یکتا |
| `source_id` | ارجاع به SourceDocument |
| `text` | متن chunk |
| `page` / `section` | موقعیت در سند |
| `effective_from` / `effective_to` | کپی یا override اعتبار زمانی |
| `embedding` | بردار (در لایه store) |
| `metadata` | برچسب‌ها، نوع ماده، و غیره |

### 3. Citation
اطلاعات provenance برای پاسخ نهایی

| فیلد | توضیح |
|------|--------|
| `source_id`, `chunk_id` | ارجاع |
| `title`, `official_ref` | نمایش به کاربر |
| `page`, `section`, `url` | موقعیت |
| `score` | امتیاز بازیابی |
| `effective_from` (اختیاری) | برای شفافیت زمانی |

### 4. Collection / Namespace
- دانش رسمی در collection جدا (مثلاً `iran_tax_official`)
- دانش پرونده کاربر هرگز با دانش رسمی مخلوط نمی‌شود

قراردادهای Pydantic/TypeScript معادل این مدل در `packages/shared` نگهداری می‌شوند و از مدل‌های MKA-Core به‌عنوان پایه استفاده/تطبیق می‌گردند.

## Consequences

### Positive
- Citation و Temporal Validity از سطح داده پشتیبانی می‌شوند
- انتقال از MKA-Core با حداقل اصطکاک
- امکان فیلتر زمانی در retrieval (فقط قوانین معتبر در تاریخ X)
- جداسازی امن دانش رسمی و پرونده

### Negative / Trade-offs
- پیچیدگی بیشتر نسبت به chunk ساده بدون metadata زمانی
- نیاز به پر کردن `effective_from`/`effective_to` در ingestion (گاهی دستی یا نیمه‌خودکار)

### Neutral
- جزئیات schema دیتابیس رابطه‌ای (PostgreSQL) در پیاده‌سازی مشخص می‌شود؛ این ADR قرارداد منطقی است.
- taxlaw-engine می‌تواند فیلدهای اضافی پرونده (timeline، ادعاها) را روی همین پایه بسازد.

## Compliance

- هر پاسخ RAG که ادعای حقوقی-مالیاتی دارد باید حداقل یک `Citation` معتبر داشته باشد.
- Chunkهای بدون `source_id` قابل ایندکس در collection رسمی نیستند.
- تغییرات شکستن‌ساز مدل باید با ADR جدید یا نسخه جدید این ADR مستند شوند.
