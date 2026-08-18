# ADR-004: API Layer and Gateway

**Status:** Accepted  
**Date:** 2026-08-18  
**Deciders:** Project Owner + Architecture (on behalf of mka-platform)

---

## Context

طبق معماری کلی و الگوی API Gateway در MKA:

- کلاینت‌ها (Web، Telegram Bot، Admin) نباید مستقیماً به سرویس‌های داخلی (retrieval، taxlaw، parser) وصل شوند.
- نیاز به احراز هویت، rate limit، orchestration جریان RAG/لایحه، و بسته‌بندی Citation وجود دارد.
- در MKA-Core بخش `backend-api` با FastAPI پیاده‌سازی اولیه شده است.

گزینه‌ها برای `apps/api` یا معادل:
- **FastAPI** (Python) — هم‌زبان با knowledge/RAG packages
- **NestJS** (TypeScript) — هم‌زبان با Next.js
- BFF داخل Next.js Route Handlers فقط

## Decision

1. **الگوی Gateway حفظ می‌شود**: تمام ترافیک خارجی از یک Backend API عبور می‌کند (هم‌راستا با ADR-003 MKA-Core).
2. **پیاده‌سازی اولیه API Gateway با FastAPI (Python)** در `apps/api` (یا `packages/backend-api` منتقل‌شده):
   - هم‌زبانی با document-parser، retrieval، embedding، taxlaw-engine
   - استفاده مجدد از کد و مدل‌های Pydantic موجود در MKA
   - مناسب برای orchestration سنگین RAG و پردازش سند
3. **وب (Next.js)** فقط BFF نازک دارد (Route Handlers / Server Actions) برای session، cookie و proxy به FastAPI؛ منطق دامنه در Next.js انباشته نمی‌شود.
4. قراردادهای عمومی (OpenAPI) از FastAPI تولید و در صورت نیاز برای کلاینت TypeScript مصرف می‌شوند.

در صورت نیاز آینده به API کاملاً TypeScript-first، می‌توان BFF را گسترش داد یا سرویس جدا اضافه کرد؛ این ADR مسیر پیش‌فرض فاز ۱–۲ را قفل می‌کند.

## Consequences

### Positive
- یک زبان برای هسته دانش و API → سرعت انتقال از MKA-Core
- مرز امنیتی و orchestration متمرکز
- کلاینت‌های متعدد (وب، ربات، ادمین) قرارداد یکسان دارند

### Negative / Trade-offs
- دو runtime (Node برای وب، Python برای API) در استقرار
- تیم باید با هر دو اکوسیستم راحت باشد
- تأخیر یک hop اضافه (قابل قبول برای workload تعاملی)

### Neutral
- ربات تلگرام و admin نیز فقط از طریق همین API صحبت می‌کنند.
- جزئیات auth (JWT، session، Supabase و غیره) در پیاده‌سازی/ADR بعدی مشخص می‌شود.

## Compliance

- هیچ endpoint عمومی جدید نباید مستقیماً روی retrieval-engine یا taxlaw-engine expose شود.
- تغییرات breaking در API عمومی باید versioned و در changelog/ADR منعکس شوند.
