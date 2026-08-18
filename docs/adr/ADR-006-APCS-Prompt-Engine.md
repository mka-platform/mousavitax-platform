# ADR-006: APCS as Central Prompt Engine

**Status:** Accepted  
**Date:** 2026-08-18  
**Deciders:** Project Owner + Architecture (mka-platform / ARYA)

---

## Context

پلتفرم هلدینگ (MKA Core + verticals) به چند دستیار نیاز دارد:

- مشاور مالیاتی (MousaviTax / ARYA Tax)
- Knowledge Studio
- در آینده: Trader، حقوقی، حسابداری، ...

بدون استاندارد واحد پرامپت:

- منطق نقش/قواعد/Citation در چند جا تکرار می‌شود
- تعویض LLM پرهزینه می‌شود
- کنترل ضدتوهم و Quality Gate یکدست نیست
- ردیابی تصمیم (Traceable Decision) ضعیف می‌ماند

استاندارد **APCS v1.0 (ARYA Prompt Command Standard)** این شکاف را پر می‌کند.

## Decision

1. **APCS v1.0** استاندارد مادر Prompt در تمام پروژه‌های ARYA / MousaviTax / MKA Holding است.
2. یک **APCS Engine مرکزی** در `packages/prompt-engine` پیاده می‌شود؛ دستیارها منطق APCS را کپی نمی‌کنند.
3. هر Domain Pack فقط **Profile** دارد (`domains/<id>/apcs_profile.yaml` + prompts).
4. معماری pipeline اجباری است:

   `Parse → Validate → Context → Evidence → Prompt Build → Model Adapter → Response Validate → Quality Gate → Output`

5. پیاده‌سازی طبق فازهای APCS (ابتدا Phase 1 Core).
6. Model Adapter از `packages/ai-gateway` استفاده می‌کند (هم‌راستا با ADR-004).
7. خروجی‌های حقوقی-مالیاتی بدون Citation معتبر / با شواهد ناکافی نباید از Quality Gate عبور کنند (هم‌راستا با ADR-002 و اصل Zero Fabrication).

## Consequences

### Positive
- یک هسته پرامپت برای همه verticals
- تعویض مدل بدون بازنویسی منطق دامنه
- تصمیم‌ها قابل ردیابی و ممیزی
- ضدتوهم ساختاریافته (`INSUFFICIENT_DATA`, ...)

### Negative / Trade-offs
- هزینه اولیه ساخت Parser/Validator
- تیم باید دستورات APCS را بیاموزد

### Neutral
- سازگار با Domain-Agnostic Core (MKA ADR-001) و Holding Vision

## Compliance

- افزودن system prompt دامنه خارج از APCS Engine / Domain Profile ممنوع است مگر استثنای موقت مستند.
- تغییر ناسازگار در دستورات APCS فقط با نسخه Major و ADR جدید.
