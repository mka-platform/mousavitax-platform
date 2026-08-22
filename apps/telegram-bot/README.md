# Telegram Bot — @taxiran1395_bot

Adapter نازک روی API Gateway (RAG).

## اجرا (Windows)

1. API روی `127.0.0.1:8000` روشن باشد.
2. توکن را تنظیم کنید:

```bat
set TELEGRAM_BOT_TOKEN=...
set BACKEND_URL=http://127.0.0.1:8000
set WEB_PUBLIC_URL=http://localhost:3001
scripts\win-run-telegram.bat
```

## دستورات
/start /help /status /contact /jobs /web + پیام آزاد → `/v1/rag/query`

بخشودگی جرائم فقط روی وب `/waiver` است.
