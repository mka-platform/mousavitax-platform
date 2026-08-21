# apps/web — نسخه آزمایشی وب (Next.js + RTL)

اسکلت دمو از قبل داخل مخزن است: لندینگ، `/chat`، `/advisors`، `/services`.

## پیش‌نیاز
- Node.js 18+ از https://nodejs.org
- (اختیاری) API روی `http://127.0.0.1:8000` برای چت واقعی

## اجرا روی ویندوز (PowerShell)

```powershell
# ۱) برو داخل پوشه واقعی پروژه (مسیر خودتان را جایگزین کنید)
cd D:\AI\GitHub\MKA-platformmousavitax-platform\mousavitax-platform

# اگر مخزن را ندارید:
# git clone https://github.com/mka-platform/mousavitax-platform.git
# cd mousavitax-platform

# ۲) وب
cd apps\web
npm install

# ۳) آدرس API (اگر بک‌اند روشن است)
$env:NEXT_PUBLIC_API_URL = "http://127.0.0.1:8000"

# ۴) اجرای دمو
npm run dev
```

مرورگر: http://localhost:3000

### بدون API
صفحات لندینگ / مشاوران / خدمات کار می‌کنند. صفحه `/chat` بدون API خطا می‌دهد تا بک‌اند را روشن کنید.

## فقط یک‌بار clone از GitHub

```powershell
cd D:\AI\GitHub
git clone https://github.com/mka-platform/mousavitax-platform.git
cd mousavitax-platform\apps\web
npm install
npm run dev
```

## انتشار دمو آنلاین (پیشنهادی: Vercel)

GitHub Pages برای Next.js App Router مناسب نیست مگر static export.
ساده‌ترین راه دمو عمومی:

1. حساب [vercel.com](https://vercel.com) با GitHub
2. Import مخزن `mka-platform/mousavitax-platform`
3. Root Directory را بگذارید: `apps/web`
4. Deploy

متغیر محیطی (اختیاری):
`NEXT_PUBLIC_API_URL` = آدرس API عمومی شما

## ساخت production محلی

```powershell
cd apps\web
npm run build
npm run start
```
