@echo off
chcp 65001 >nul
cd /d "%~dp0\.."
call .venv\Scripts\activate.bat
set PYTHONPATH=%CD%\packages\shared;%CD%\packages\ai-gateway\app;%CD%\packages\taxlaw-engine;%CD%\packages\prompt-engine;%CD%\packages\knowledge-core
set EMBEDDING_PROVIDER=fallback
set VECTOR_DB_PATH=%CD%\data\iran_tax_vectors.json
cd /d "%CD%\apps\api"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
