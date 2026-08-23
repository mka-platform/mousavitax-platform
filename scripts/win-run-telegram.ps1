# PowerShell runner for Telegram bot (if .bat path issues)
Set-Location $PSScriptRoot\..
if (-not (Test-Path .\.venv\Scripts\Activate.ps1)) {
  Write-Host "Run scripts\win-setup.bat first"
  exit 1
}
& .\.venv\Scripts\Activate.ps1
if (-not $env:TELEGRAM_BOT_TOKEN) {
  Write-Host "Set TELEGRAM_BOT_TOKEN first:"
  Write-Host '  $env:TELEGRAM_BOT_TOKEN = "YOUR_TOKEN"'
  exit 1
}
if (-not $env:BACKEND_URL) { $env:BACKEND_URL = "http://127.0.0.1:8000" }
if (-not $env:WEB_PUBLIC_URL) { $env:WEB_PUBLIC_URL = "http://localhost:3001" }
python -m pip install -q -r apps\telegram-bot\requirements.txt
Set-Location apps\telegram-bot
python app\bot.py
