@echo off
REM ClinIQ Quick Setup Script for Windows

echo.
echo Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Please install Python 3.11+
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python %PYTHON_VERSION% found

echo.
echo Checking Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Node.js not found. Please install Node.js 18+
    exit /b 1
)
for /f %%i in ('node --version') do set NODE_VERSION=%%i
echo Node.js %NODE_VERSION% found

REM Setup Backend
echo.
echo Setting up backend...
cd backend

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing Python dependencies...
pip install -r requirements.txt -q

if not exist ".env" (
    echo Creating .env from template...
    copy .env.example .env
    echo Please edit backend\.env with your GEMINI_API_KEY
) else (
    echo .env already exists
)

cd ..

REM Setup Frontend
echo.
echo Setting up frontend...
cd frontend

echo Installing npm dependencies...
call npm install -q

if not exist ".env" (
    echo Creating .env from template...
    copy .env.example .env
    echo Frontend .env created
) else (
    echo .env already exists
)

cd ..

echo.
echo ======================================================
echo Setup complete!
echo ======================================================
echo.
echo Next steps:
echo.
echo 1. Update your Gemini API key:
echo    Edit: backend\.env
echo    Get free key: https://makersuite.google.com/app/apikey
echo.
echo 2. Start the backend:
echo    cd backend
echo    venv\Scripts\activate
echo    python -m uvicorn app.main:app --reload
echo.
echo 3. In another terminal, start the frontend:
echo    cd frontend
echo    npm run dev
echo.
echo 4. Open http://localhost:5173 in your browser
echo.
