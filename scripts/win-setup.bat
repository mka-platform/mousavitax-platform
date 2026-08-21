@echo off
chcp 65001 >nul
setlocal EnableExtensions
cd /d "%~dp0\.."
echo === MousaviTax setup (Windows) ===
echo ROOT: %CD%

where python >nul 2>&1
if errorlevel 1 (
  echo [ERROR] python not in PATH. Install Python 3.12+ and check "Add to PATH".
  pause
  exit /b 1
)

python --version
if not exist ".venv\Scripts\python.exe" (
  echo Creating .venv ...
  python -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
echo Installing API requirements...
python -m pip install -r apps\api\requirements.txt
python -m pip install -r packages\document-parser\requirements.txt 2>nul
python -m pip install -r packages\embedding-service\requirements.txt 2>nul
python -m pip install -r packages\retrieval-engine\requirements.txt 2>nul
python -m pip install -r packages\knowledge-core\requirements.txt 2>nul

if not exist "data" mkdir data
set EMBEDDING_PROVIDER=fallback
set VECTOR_DB_PATH=%CD%\data\iran_tax_vectors.json
echo Seeding sample knowledge...
python scripts\seed_knowledge.py
echo.
echo Setup done. Next: scripts\win-run-api.bat   then   scripts\win-run-web.bat
pause
