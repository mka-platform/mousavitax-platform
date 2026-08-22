@echo off
chcp 65001 >nul
cd /d "%~dp0\.."
if not exist ".venv\Scripts\activate.bat" (
  echo Run scripts\win-setup.bat first.
  pause
  exit /b 1
)
call .venv\Scripts\activate.bat
if not defined TELEGRAM_BOT_TOKEN (
  echo Set TELEGRAM_BOT_TOKEN first, e.g.:
  echo   set TELEGRAM_BOT_TOKEN=123:ABC...
  pause
  exit /b 1
)
if not defined BACKEND_URL set BACKEND_URL=http://127.0.0.1:8000
if not defined WEB_PUBLIC_URL set WEB_PUBLIC_URL=http://localhost:3001
python -m pip install -q -r apps\telegram-bot\requirements.txt
cd apps\telegram-bot
python app\bot.py
