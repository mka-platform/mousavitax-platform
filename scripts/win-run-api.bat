@echo off
chcp 65001 >nul
cd /d "%~dp0\.."
if not exist ".venv\Scripts\activate.bat" (
  echo Run scripts\win-setup.bat first.
  pause
  exit /b 1
)
call .venv\Scripts\activate.bat

REM Do NOT put packages\document-parser or *\embedding-service\app on PYTHONPATH —
REM they also expose a top-level package named "app" and break "app.main".
set PYTHONPATH=%CD%\packages\shared;%CD%\packages\ai-gateway\app;%CD%\packages\taxlaw-engine;%CD%\packages\prompt-engine;%CD%\packages\knowledge-core
set EMBEDDING_PROVIDER=fallback
set VECTOR_DB_PATH=%CD%\data\iran_tax_vectors.json
set LLM_PROVIDER=ollama
set OPENAI_BASE_URL=http://localhost:11434/v1
set OPENAI_API_KEY=ollama

echo ROOT=%CD%
echo API  -> http://localhost:8000/health
echo Docs -> http://localhost:8000/docs
echo.

cd /d "%CD%\apps\api"
python -c "import app.main; print('import ok', app.main.app.title)"
if errorlevel 1 (
  echo [ERROR] import app.main failed
  pause
  exit /b 1
)

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
