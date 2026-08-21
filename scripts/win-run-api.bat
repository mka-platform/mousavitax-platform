@echo off
chcp 65001 >nul
cd /d "%~dp0\.."
if not exist ".venv\Scripts\activate.bat" (
  echo Run scripts\win-setup.bat first.
  pause
  exit /b 1
)
call .venv\Scripts\activate.bat
set PYTHONPATH=%CD%\packages\shared;%CD%\packages\ai-gateway\app;%CD%\packages\taxlaw-engine;%CD%\packages\prompt-engine;%CD%\packages\knowledge-core;%CD%\packages\embedding-service\app;%CD%\packages\retrieval-engine\app;%CD%\packages\document-parser
set EMBEDDING_PROVIDER=fallback
set VECTOR_DB_PATH=%CD%\data\iran_tax_vectors.json
set LLM_PROVIDER=ollama
set OPENAI_BASE_URL=http://localhost:11434/v1
set OPENAI_API_KEY=ollama
echo API → http://localhost:8000/health
echo Docs → http://localhost:8000/docs
cd apps\api
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
