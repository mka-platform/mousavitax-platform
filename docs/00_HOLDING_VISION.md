# Holding Vision — MKA / MousaviTax

## مدل هلدینگ

MousaviTax Platform به‌عنوان **هلدینگ فناوری دانش‌محور** طراحی می‌شود:

1. **Core (MKA)** — یک بار ساخته می‌شود، برای همه دامنه‌ها مشترک است.
2. **Vertical / Domain Pack** — هر حوزه کسب‌وکار (مالیات، حقوقی، پزشکی، ...) یک pack مستقل است:
   - knowledge collection جدا
   - prompt templates جدا
   - قوانین ایمنی و disclaimer جدا
   - در صورت نیاز Domain Adapter نازک (بدون آلوده کردن Core)

3. **محصولات سطحی** — وب، ربات، API، پنل — روی همان Core و Domain Packها سوار می‌شوند.

## دامنه فعلی: Iran Tax

- مسیر: `domains/iran-tax/`
- Collection پیش‌فرض: `iran_tax_official`
- محصولات: مشاوره AI، بازار مشاوران، لایحه، اظهارنامه، سامانه مودیان

## دامنه‌های آینده (نمونه)

| Domain ID | مثال محصول |
|-----------|------------|
| `iran-legal` | دستیار حقوقی |
| `iran-accounting` | دستیار حسابداری |
| `education` | دستیار آموزشی |

افزودن دامنه جدید = محتوای دانش + پرامپت + (اختیاری) adapter؛ **بدون بازنویسی Core**.

## هم‌راستایی با MKA-Core ADR-001

هسته Domain-Agnostic می‌ماند. منطق دامنه فقط در:
- Prompt Engine / `domains/*/prompts`
- Knowledge collections
- Domain Adapters (آینده)
