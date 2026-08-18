# ADR-003: Core Migration Strategy (MKA-Core → packages/)

**Status:** Accepted  
**Date:** 2026-08-18  
**Deciders:** Project Owner + Architecture (on behalf of mka-platform)

---

## Context

مخزن `mousavitax-platform` اسکلت monorepo است. کد واقعی هسته در:

- **MKA-Core** (`mka-platform/MKA-Core`): document-parser، retrieval-engine، embedding-service، shared، ai-gateway، backend-api، telegram-bot، google-drive-sync، ...
- **TAXLAW-GROK / ALTIP** (عمدتاً روی Drive و پروتوتایپ‌ها): منطق لایحه‌نویسی و پژوهش حقوقی

نیاز است هسته واقعی به `packages/` منتقل شود بدون:
- شکستن تاریخچه مفید
- ایجاد دو منبع حقیقت دائمی
- قفل شدن به ساختار نامناسب برای دامنه مالیات ایران

گزینه‌ها:
1. Git submodule / subtree
2. کپی یک‌باره + تطبیق (copy & adapt)
3. ادغام کامل تاریخچه (monorepo merge)
4. نگه داشتن MKA-Core به‌عنوان upstream و فقط wrapper

## Decision

**استراتژی: Copy & Adapt با مرز مشخص**

1. **کپی انتخابی** بسته‌های پایدار از MKA-Core به مسیرهای معادل در `mousavitax-platform/packages/`:
   - `document-parser` → `packages/document-parser`
   - `retrieval-engine` → `packages/retrieval-engine` (یا ادغام تدریجی در knowledge-core)
   - `shared` → `packages/shared` (با namespace/مدل‌های مالیاتی گسترش‌یافته)
   - منطق embedding → بخشی از knowledge-core یا سرویس جدا
2. **تطبیق**:
   - نام‌گذاری و importها با ساختار monorepo جدید
   - اعمال مدل داده ADR-002 (Temporal، official_ref، ...)
   - حذف یا ایزوله کردن بخش‌های domain-agnostic که برای مالیات لازم نیست در لایه tax
3. **taxlaw-engine** از صفر/اسکلت فعلی با پورت منطق TAXLAW-GROK و ALTIP ساخته می‌شود (نه کپی کور).
4. **MKA-Core** تا اطلاع ثانوی به‌عنوان مرجع و منبع الهام باقی می‌ماند؛ پس از تثبیت migration، وابستگی runtime به آن قطع می‌شود.
5. **تاریخچه git**: commitهای اولیه migration با پیام واضح (`migrate: ... from MKA-Core`) ثبت می‌شوند؛ نیازی به حفظ کامل history submodule نیست.

ترتیب پیشنهادی انتقال:
1. `shared` + مدل‌ها  
2. `document-parser`  
3. retrieval + embedding → knowledge-core  
4. اسکلت taxlaw-engine + پورت تدریجی  
5. سرویس‌های جانبی (crawler، source-bridge، telegram) بر اساس نیاز

## Consequences

### Positive
- کنترل کامل روی کد داخل پلتفرم مالیاتی
- امکان سفارشی‌سازی بدون محدودیت upstream
- سادگی CI و ownership داخل یک repo
- جلوگیری از پیچیدگی submodule در مرحله اولیه

### Negative / Trade-offs
- همگام‌سازی دستی با بهبودهای بعدی MKA-Core (در صورت ادامه توسعه موازی)
- احتمال divergence؛ باید با discipline و در صورت نیاز cherry-pick مدیریت شود

### Neutral
- این تصمیم با ADR-001 و ADR-002 MKA-Core (Domain-Agnostic، Modular Monorepo) سازگار است: هسته دانش generic می‌ماند و دامنه مالیات در packages/apps لایه‌بندی می‌شود.

## Compliance

- انتقال بدون تست حداقل smoke (import + یک مسیر parse/index/query) پذیرفته نیست.
- پس از هر بسته منتقل‌شده، README همان package و `docs/03_ROADMAP.md` به‌روز شود.
- ایجاد وابستگی runtime از mousavitax-platform به کلون MKA-Core ممنوع است مگر با ADR جدید.
