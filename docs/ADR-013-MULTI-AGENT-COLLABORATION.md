# ADR-013: معماری همکاری عامل‌های MousaviTax

## تصمیم
معماری عامل‌ها به صورت Tool-Based و Policy-Driven پیاده‌سازی می‌شود.

## عامل‌های اولیه
- Platform Agent
- Office Agent
- Case Agent
- Deadline Agent
- Quality Agent

## اصل ایمنی
Agent → Authorized Tool/API → Permission & Ownership Gate → Service Layer → Data Store

عامل‌ها به صورت مستقیم SQL یا دسترسی مستقیم به پایگاه داده ندارند.

## سطح اتوماسیون نسخه اول
**Read + Suggest**

ایجاد یا تغییر داده‌های عملیاتی نیازمند Policy و تأیید مناسب خواهد بود.

## نام‌گذاری سازمانی
در نقش‌ها و مستندات داخلی از «کارمند پلتفرم» و «کارمند دفتر مشاوره موسوی جراحی» استفاده می‌شود و عبارت «کارمند اداره مالیات» برای نقش داخلی پروژه استفاده نمی‌شود.
