# ADR-005: Vector Store and Embedding

**Status:** Accepted  
**Date:** 2026-08-18  
**Deciders:** Project Owner + Architecture (on behalf of mka-platform)

---

## Context

RAG و Citation به ذخیره و جستجوی برداری chunkها وابسته‌اند. در MKA-Core یک `InMemoryVectorStore` با persistence JSON و numpy برای مرحله اول وجود دارد. برای پلتفرم تولیدی مالیاتی نیاز به:

- پایداری و پشتیبان‌گیری
- فیلتر metadata (از جمله Temporal Validity)
- مقیاس متوسط دانش رسمی ایران
- هزینه و پیچیدگی عملیاتی قابل مدیریت در فاز ۱

گزینه‌ها:
- ادامه In-Memory / JSON (فقط dev)
- **pgvector** روی PostgreSQL
- Qdrant / Chroma / Weaviate به‌صورت سرویس جدا
- سرویس مدیریت‌شده ابری

برای Embedding: مدل‌های OpenAI-compatible، مدل‌های محلی (sentence-transformers)، یا APIهای سازگار.

## Decision

### Vector Store
- **فاز ۱ (Foundation / MVP):**  
  - Development: In-Memory یا فایل (سازگار با MKA) برای سرعت iteration  
  - Target production path: **PostgreSQL + pgvector**  
  - یک interface مشترک (`VectorStore`) در knowledge-core/retrieval تا تعویض store بدون تغییر orchestration ممکن باشد

- **فاز بعد:** در صورت نیاز به مقیاس یا ویژگی‌های پیشرفته، Qdrant (یا معادل) پشت همان interface اضافه می‌شود؛ pgvector به‌عنوان پیش‌فرض باقی می‌ماند مگر ADR جدید.

### Embedding
- Embedder پشت یک abstraction (مشابه MKA) قرار می‌گیرد.
- پیش‌فرض قابل پیکربندی: مدل OpenAI-compatible (یا Gemini و غیره) از طریق env.
- امکان تعویض به مدل محلی در صورت نیاز هزینه/حریم خصوصی.
- ابعاد بردار و نام مدل در metadata ایندکس ذخیره می‌شود تا از mismatch جلوگیری شود.

### Collection
- حداقل یک collection رسمی: `iran_tax_official`
- فیلترهای query از ADR-002 (از جمله بازه اعتبار زمانی) پشتیبانی شوند.

## Consequences

### Positive
- PostgreSQL یک스택 familiar برای داده رابطه‌ای + بردار است (کاهش تعداد سیستم‌ها)
- Interface واحد مسیر مهاجرت از MVP به production را ساده می‌کند
- سازگاری با کد فعلی MKA در لایه abstract

### Negative / Trade-offs
- pgvector برای مقیاس بسیار بزرگ ممکن است محدودیت داشته باشد (در افق فعلی قابل قبول)
- نیاز به مدیریت migrationهای SQL و نسخه extension

### Neutral
- انتخاب دقیق مدل embedding (نام و version) در زمان پیاده‌سازی با بنچمارک فارسی/حقوقی قابل تنظیم است و نیاز به ADR جدا ندارد مگر تغییر معماری.

## Compliance

- هیچ مسیر production نباید فقط به In-Memory بدون persistence وابسته باشد.
- تغییر store پیش‌فرض production بدون به‌روزرسانی این ADR مجاز نیست.
- تمام chunkهای ایندکس‌شده باید با مدل داده ADR-002 سازگار باشند.
