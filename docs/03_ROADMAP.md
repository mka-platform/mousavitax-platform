# Roadmap — MousaviTax / MKA Holding

## فاز ۰ — Foundation

- [x] مخزن یکپارچه تحت mka-platform
- [x] Vision هلدینگ + Domain-Agnostic Core
- [x] ADRهای کلیدی
- [x] انتقال shared, document-parser, embedding, retrieval, ai-gateway
- [x] API Gateway + Telegram Bot
- [x] Domain pack اولیه iran-tax
- [ ] CI پایه

## فاز ۱ — Knowledge

- [ ] اتصال retrieval واقعی به RAG endpoint
- [ ] بارگذاری دانش رسمی (قوانین / بخشنامه‌ها)
- [ ] pgvector production path
- [ ] Google Drive Sync

## فاز ۲ — Web MVP

- [ ] apps/web Next.js 15 + RTL
- [ ] چت با Citation + لیست مشاوران

## فاز ۳ — خدمات عملیاتی

- [ ] taxlaw-engine (لایحه)
- [ ] راهنمای اظهارنامه و سامانه مودیان
- [ ] پنل مشاور / مودی

## فاز ۴ — گسترش هلدینگ

- [ ] دومین Domain Pack نمونه
- [ ] Multi-tenant collections
- [ ] Audit trail و مقیاس

**اولویت فعلی:** ایندکس دانش + اتصال retrieval به `/v1/rag/query`
