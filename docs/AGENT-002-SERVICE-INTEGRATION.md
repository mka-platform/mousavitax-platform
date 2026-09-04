# AGENT-002: اتصال عامل به سرویس‌های پلتفرم

## پیاده‌سازی
- Permission Gate
- Agent Actor Context
- Audit Logger
- Service Tool Layer
- HTTP API Adapter
- Office Daily Summary
- API Boundary اولیه برای Agent
- تست‌های امنیتی پایه

## قرارداد امنیتی
عامل فقط از طریق API/Service Client با داده تعامل می‌کند. API مقصد باید Authentication، Authorization و Ownership را اعمال کند.

## نقش‌های داخلی
- platform_staff: کارمند پلتفرم
- office_staff: کارمند دفتر مشاوره موسوی جراحی
- office_manager: مدیر دفتر مشاوره موسوی جراحی
- tax_advisor: مشاور مالیاتی
- platform_admin: مدیر پلتفرم

## وضعیت
عملیات نسخه فعلی Read + Suggest است. Write Automation به مرحله بعد و Confirmation Policy منتقل شده است.
