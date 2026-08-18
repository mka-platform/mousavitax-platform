# Architecture Decision Records (ADR)

این پوشه تصمیم‌های معماری مهم پلتفرم MousaviTax را ثبت می‌کند.

فرمت هر ADR:
- **Status:** Proposed | Accepted | Deprecated | Superseded
- **Date**
- **Context / Decision / Consequences**

## فهرست ADRها

| شماره | عنوان | وضعیت |
|-------|--------|--------|
| [ADR-001](ADR-001-Web-Frontend-Stack.md) | انتخاب Stack فرانت‌اند وب (Next.js + RTL) | Accepted |
| [ADR-002](ADR-002-Knowledge-Data-Model.md) | مدل داده دانش (Document / Chunk / Citation / Temporal) | Accepted |
| [ADR-003](ADR-003-Core-Migration-Strategy.md) | استراتژی انتقال هسته از MKA-Core و TAXLAW-GROK | Accepted |
| [ADR-004](ADR-004-API-Layer.md) | لایه API و Gateway | Accepted |
| [ADR-005](ADR-005-Vector-Store-and-Embedding.md) | Vector Store و Embedding | Accepted |

## قوانین

- هر تغییر معماری مهم باید با یک ADR مستند شود.
- ADRهای Accepted تا زمان supersede شدن الزام‌آور هستند.
- شماره ADRها متوالی و بدون پرش هستند.
