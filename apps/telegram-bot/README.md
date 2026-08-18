# apps/telegram-bot

آداپتر نازک برای تلگرام (`@taxiran1395_bot` یا ربات جایگزین).

- فقط پروتکل تلگرام را ترجمه می‌کند
- منطق دانش/APCS در `apps/api` است
- هم‌تراز با `apps/bale-bot` (همان Backend)

```bash
export TELEGRAM_BOT_TOKEN=...
export BACKEND_URL=http://localhost:8000
python -m app.bot
```
