@echo off
chcp 65001 >nul
cd /d "%~dp0\.."
cd apps\web
if not exist "node_modules" (
  echo npm install...
  call npm install
)
set NEXT_PUBLIC_API_URL=http://localhost:8000
echo Web → http://localhost:3000
echo Waiver → http://localhost:3000/waiver
call npm run dev
