@echo off
REM AI App Config Compiler - Windows startup script

echo ========================================
echo AI App Config Compiler
echo ========================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Node.js not found. Please install Node.js.
    exit /b 1
)

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python not found. Please install Python 3.8+
    exit /b 1
)

echo Starting AI App Config Compiler...
echo.

REM Start backend
echo [1/2] Starting backend server...
cd backend
start "Backend - AI App Config Compiler" python app.py
cd ..
timeout /t 3 /nobreak

REM Start frontend
echo [2/2] Starting frontend server...
cd frontend
if not exist node_modules (
    echo Installing frontend dependencies...
    call npm install
)
call npm run dev
cd ..

echo.
echo ========================================
echo Frontend: http://localhost:5173
echo Backend:  http://localhost:8000
echo ========================================
