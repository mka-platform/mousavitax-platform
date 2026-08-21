# کاتالوگ خدمات (Service Catalog)

الهام‌گرفته از مدل Service-Based نما — پیاده‌سازی در MousaviTax با AI Triage.

| کد | خدمت | مسیر اولیه |
|----|------|------------|
| S01 | سؤال سریع مالیاتی | AI + RAG |
| S02 | تحلیل پرونده | Tax Case + Document AI |
| S03 | تحلیل برگ تشخیص / مطالبه | Case + Risk |
| S04 | تهیه لایحه | AI draft + Expert |
| S05 | اعتراض مالیاتی | Workflow + Expert |
| S06 | اظهارنامه | راهنما + نیمه‌خودکار |
| S07 | سامانه مودیان | دانش + راهنما |
| S08 | ارزش افزوده | RAG + Case |
| S09 | جرائم مالیاتی | RAG + Risk |
| S10 | بررسی قرارداد | Document AI |
| S11 | محاسبات مالیاتی | ابزار + Expert |
| S12 | ارزیابی ریسک مالیاتی | Risk Scoring (P1) |
| S13 | ارجاع به مشاور متخصص | Marketplace |

ثبت درخواست خدمت در فاز API: `POST /v1/services/requests` (برنامه).
