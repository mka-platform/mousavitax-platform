# استاندارد اختصاصی APCS v1.0
## ARYA Prompt Command Standard

> منبع مادر کنترل پرامپت در اکوسیستم ARYA / MKA Holding / MousaviTax

### 1. هدف

APCS یک استاندارد داخلی برای تعریف، کنترل و اجرای دستورات هوش مصنوعی است.

یک دستور واحد باید مشخص کند:

- نقش مدل (`/ROLE`)
- مأموریت (`/TASK`)
- زمینه و ورودی (`/CONTEXT`, `/INPUT`)
- شواهد و اولویت منابع (`/EVIDENCE`, `/SOURCE-PRIORITY`)
- قواعد و محدودیت‌ها (`/RULES`, `/CONSTRAINTS`, `/GUARDRAIL`)
- روش تحلیل (`/METHOD`, `/ANALYZE`, ...)
- ریسک و خطا (`/RISK`, `/PITFALLS`)
- راستی‌آزمایی (`/VERIFY`, `/SELF-CHECK`)
- قالب خروجی و تصمیم (`/FORMAT`, `/DECISION`)

**اصول:** Model-Agnostic · Evidence-Based · Traceable Decision · No Unsupported Claims

---

### 2. ساختار دستورات

```
/ROLE /TASK /CONTEXT /INPUT /EVIDENCE /RULES /CONSTRAINTS
/METHOD /ANALYZE /PERSPECTIVES /COMPARE /RISK /PITFALLS
/METRICS /VERIFY /SCORE /DECISION /FORMAT /AUDIENCE /TONE
/EXEC /SELF-CHECK
```

همه اجباری نیستند؛ موتور فقط دستورات لازم برای مسئله را اجرا می‌کند.

---

### 3. لایه‌های طلایی (نباید جابه‌جا شوند)

| لایه | معنی |
|------|------|
| DATA | چه اطلاعاتی داریم؟ |
| EVIDENCE | چه چیزی اثبات شده؟ |
| ANALYSIS | چه برداشتی داریم؟ |
| DECISION | چه تصمیمی می‌گیریم؟ |
| ACTION | قدم بعدی چیست؟ |

---

### 4. ضد توهم

- اطلاعات ناکافی → `INSUFFICIENT_DATA`
- منابع متناقض → `CONFLICTING_EVIDENCE`
- فقط استنباط → `INFERENCE`
- نیاز به انسان → `HUMAN_REVIEW_REQUIRED`

وضعیت شواهد: `FACT | SUPPORTED | INFERRED | ASSUMED | UNCERTAIN | CONFLICTING | UNKNOWN`

---

### 5. معماری نرم‌افزاری

```
USER → APCS COMMAND → PARSER → VALIDATOR → CONTEXT ENGINE
     → EVIDENCE ENGINE → PROMPT BUILDER → MODEL ADAPTER
     → RESPONSE VALIDATOR → QUALITY GATE → DECISION/OUTPUT → USER
```

دستورات APCS مستقیماً به مدل خام فرستاده نمی‌شوند.

---

### 6. فازهای پیاده‌سازی

| فاز | دستورات |
|-----|----------|
| **Phase 1 — Core** | `/ROLE` `/TASK` `/CONTEXT` `/INPUT` `/RULES` `/FORMAT` |
| **Phase 2 — Intelligence** | `/METHOD` `/ANALYZE` `/PERSPECTIVES` `/COMPARE` `/RISK` `/PITFALLS` |
| **Phase 3 — Verification** | `/EVIDENCE` `/VERIFY` `/CROSS-CHECK` `/SELF-CHECK` `/QUALITY-GATE` |
| **Phase 4 — Decision** | `/METRICS` `/SCORE` `/WEIGHT` `/DECISION` `/ACTION` |
| **Phase 5 — Enterprise** | `/PM-MODE` `/DEV-MODE` `/CONTEXT-STACK` `/AUDIT-LOG` `/VERSIONING` |

---

### 7. پروفایل‌های دامنه (Holding)

```
APCS Core  +  Tax Profile  +  Trader Profile  +  Knowledge Profile  +  ...
```

- هسته یک بار پیاده می‌شود (`packages/prompt-engine`)
- هر Vertical فقط Profile تخصصی اعمال می‌کند (`domains/*/apcs_profile.yaml`)

جزئیات کامل دستورات، نمونه‌ها و Validator در همین سند نسخه کامل نگهداری می‌شود؛ نسخه اجرایی در repo با همین فایل و ADR-006 قفل شده است.

**نسخه:** 1.0  
**وضعیت:** Accepted as mother prompt standard  
**کاربرد:** ARYA Tax Advisor · Knowledge Studio · (آینده) Trader و سایر verticals
