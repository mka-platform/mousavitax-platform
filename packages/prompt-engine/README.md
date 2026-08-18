# prompt-engine

موتور مرکزی **APCS v1.0** (ARYA Prompt Command Standard).

تمام دستیارهای هلدینگ (Tax، Knowledge Studio، ...) از این پکیج استفاده می‌کنند و منطق پرامپت را تکرار نمی‌کنند.

## معماری

```
APCS Command → Parser → Validator → Context → Evidence
            → PromptBuilder → (ai-gateway) → ResponseValidator → QualityGate
```

## فاز فعلی: Phase 1 — Core

پشتیبانی اولیه:

- `/ROLE` `/TASK` `/CONTEXT` `/INPUT` `/RULES` `/FORMAT`
- ساخت system/user prompt از Domain Profile + دستورات

## استفاده

```python
from prompt_engine import APCSParser, PromptBuilder

cmd = APCSParser().parse(raw_apcs_text)
prompt = PromptBuilder(domain="iran-tax").build(cmd, retrieved_context=[...])
```

## اسناد

- استاندارد کامل: `docs/standards/APCS-v1.0.md`
- ADR: `docs/adr/ADR-006-APCS-Prompt-Engine.md`
