# ADR-001: Web Frontend Stack (Next.js + RTL)

**Status:** Accepted  
**Date:** 2026-08-18  
**Deciders:** Project Owner + Architecture (on behalf of mka-platform)

---

## Context

وب‌سایت اصلی پلتفرم (`apps/web`) باید:

- کاملاً فارسی و **RTL** باشد
- تجربه کاربری شبیه پلتفرم‌های مشاوره ایرانی (الهام از moshaver.namatsp.ir) ارائه دهد
- چت‌بات دانش‌محور با Citation، لیست مشاوران، پنل مودی و صفحات خدمات را پوشش دهد
- SEO-friendly و قابل استقرار روی Vercel / Node باشد
- با اکوسیستم TypeScript monorepo هماهنگ باشد

گزینه‌های بررسی‌شده:
- Next.js (App Router) + Tailwind + shadcn/ui
- Remix / SvelteKit
- Nuxt (Vue)
- SPA خالص (Vite + React)

## Decision

**Stack فرانت‌اند وب:**

| جزء | انتخاب |
|------|--------|
| Framework | **Next.js 15** (App Router) |
| Language | TypeScript |
| Styling | Tailwind CSS + CSS logical properties برای RTL |
| UI Components | **shadcn/ui** (با پشتیبانی RTL) |
| Font | فونت‌های فارسی استاندارد (مثلاً Vazirmatn یا IRANSans) |
| i18n / Direction | `dir="rtl"` و `lang="fa"` در root layout؛ در صورت نیاز `next-intl` برای آینده |
| Form / Validation | React Hook Form + Zod |
| Data fetching | Server Components + Route Handlers / API client به Backend |

- پروژه در `apps/web` قرار می‌گیرد.
- پشتیبانی کامل RTL از روز اول اجباری است (نه retrofit).
- پنل ادمین می‌تواند بعداً از همین stack یا از admin-panel موجود در MKA-Core الهام بگیرد؛ در این ADR فقط `apps/web` قفل می‌شود.

## Consequences

### Positive
- اکوسیستم غنی، SSR/SSG، SEO و عملکرد خوب
- shadcn/ui سرعت توسعه UI را بالا می‌برد و با Tailwind سازگار است
- هم‌راستا با روند فعلی جامعه React/Next و مهارت‌های رایج تیم
- امکان استفاده از Server Actions و Route Handlers برای لایه نازک وب

### Negative / Trade-offs
- Next.js App Router گاهی پیچیدگی بیشتری نسبت به Pages Router دارد
- وابستگی به React؛ در صورت تغییر شدید stack در آینده هزینه مهاجرت وجود دارد
- shadcn/ui نیاز به کپی کامپوننت‌ها دارد (نه npm package کلاسیک) — قابل مدیریت است

### Neutral
- این تصمیم فقط `apps/web` را پوشش می‌دهد؛ `apps/admin` و ربات تلگرام جداگانه تصمیم‌گیری می‌شوند.
- با ADRهای MKA-Core (Domain-Agnostic و API Gateway) سازگار است؛ وب فقط client است.

## Compliance

- هر PR مربوط به `apps/web` باید RTL و فارسی بودن را رعایت کند.
- افزودن dependency فرانت‌اند خارج از این stack نیاز به ADR جدید یا به‌روزرسانی این ADR دارد.
