# ADR-014: یک مغز، دو دست

## تصمیم
MKA-Core مغز دانشی پروژه است و تنها مرجع Evidence و Citation محسوب می‌شود.

MousaviTax Platform لایه عملیات دفتر، پرونده، خدمات و کانال‌ها است.

MKA Panel فقط رابط کاربری و مصرف‌کننده API است.

## قرارداد مشترک

`POST /v1/orchestrate`

پاسخ استاندارد:

`{ status, answer, citations, actions, trace_id }`

## قواعد
- پرسش مالیاتی به MKA-Core ارجاع می‌شود.
- پاسخ MKA-Core بدون بازنویسی عبور داده می‌شود.
- INSUFFICIENT_DATA بدون تغییر بازگردانده می‌شود.
- ابهام در Intent منجر به CLARIFICATION_REQUIRED می‌شود.
- هیچ Agent دیگری Citation تولید نمی‌کند.
