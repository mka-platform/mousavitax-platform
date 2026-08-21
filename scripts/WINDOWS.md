# راه‌اندازی روی Windows

## پیش‌نیاز
- Python 3.12+ در PATH (`python --version`)
- Node.js 18+ (`node -v`)
- Git

## یک‌بار
1. کلون یا `git pull` مخزن
2. دوبارکلیک یا در CMD:

```bat
cd /d D:\AI\GitHub\mousavitax-platform
scripts\win-setup.bat
```

## هر بار اجرا (دو پنجره CMD)

پنجره ۱ — API:
```bat
scripts\win-run-api.bat
```

پنجره ۲ — وب:
```bat
scripts\win-run-web.bat
```

- API: http://localhost:8000/health  
- وب: http://localhost:3000  
- بخشودگی: http://localhost:3000/waiver  

## اگر `pip` / `uvicorn` خطای Python313 داد
همیشه:
```bat
python -m pip install ...
python -m uvicorn ...
```

## دانش رسمی
PDFها را در `knowledge\official\` بگذارید، سپس:
```bat
call .venv\Scripts\activate.bat
set EMBEDDING_PROVIDER=fallback
set VECTOR_DB_PATH=%CD%\data\iran_tax_vectors.json
python scripts\seed_knowledge.py
```
