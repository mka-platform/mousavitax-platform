# Holding Vision — MKA / ARYA / MousaviTax

## مدل هلدینگ

1. **Core (MKA)** — RAG، Citation، Parser، Embedding، AI Gateway، **APCS Prompt Engine**
2. **Vertical / Domain Pack** — هر حوزه یک pack:
   - knowledge collection
   - `apcs_profile.yaml` + prompts
   - اختیاری: Domain Adapter
3. **محصولات** — Web، Telegram، API، Admin

## APCS

استاندارد مادر پرامپت: **APCS v1.0** (`docs/standards/APCS-v1.0.md`, ADR-006).

```
APCS Core + Tax Profile + Knowledge Profile + (آینده) Trader / Legal / ...
```

## دامنه فعلی: Iran Tax

- مسیر: `domains/iran-tax/`
- Collection: `iran_tax_official`
- محصولات: مشاوره AI، بازار مشاوران، لایحه، اظهارنامه، سامانه مودیان

## دامنه‌های آینده

افزودن دامنه = دانش + APCS Profile + پرامپت؛ بدون بازنویسی Core.
