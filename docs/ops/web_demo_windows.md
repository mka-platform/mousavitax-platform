# راهنمای دمو وب روی ویندوز

## آیا نسخه آزمایشی در GitHub هست؟
بله — پوشه `apps/web` در مخزن:
https://github.com/mka-platform/mousavitax-platform/tree/main/apps/web

شامل:
- `/` لندینگ فارسی RTL
- `/chat` اتصال به API
- `/advisors` اسکلت بازار مشاوران
- `/services` اسکلت خدمات

## اجرا (PowerShell فقط — نه CMD با دستور Linux)

```powershell
cd <مسیر-پروژه>\mousavitax-platform\apps\web
npm install
npm run dev
```

سپس: http://localhost:3000

## اشتباهات رایج
| اشتباه | درست |
|--------|------|
| `export VAR=...` | `$env:VAR = "..."` |
| `set VAR=...` داخل PowerShell | همان `$env:VAR` |
| مسیر `C:\Users\ziya\mousavitax-platform` وقتی پروژه جای دیگر است | `cd` به مسیری که `apps\web` دارد |
| چسباندن دو دستور در یک خط | هر دستور جدا Enter |
