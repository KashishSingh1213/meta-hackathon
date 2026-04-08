@echo off
REM Quick test script for ClinIQ OpenEnv setup (Windows)
REM Usage: test-openenv.bat

echo.
echo ========================================
echo  ClinIQ OpenEnv - Quick Test
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Install Python 3.11+
    exit /b 1
)
echo [OK] Python found

REM Check inference.py exists
if not exist "inference.py" (
    echo ERROR: inference.py not found in current directory
    exit /b 1
)
echo [OK] inference.py found

REM Install dependencies
echo.
echo Installing dependencies...
pip install -q -r backend/requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)
echo [OK] Dependencies installed

REM Check .env
if not exist "backend\.env" (
    echo WARNING: backend\.env not found
) else (
    findstr /M "GEMINI_API_KEY" backend\.env >nul
    if errorlevel 1 (
        echo WARNING: GEMINI_API_KEY not set in backend\.env
    ) else (
        echo [OK] backend\.env configured
    )
)

REM Check backend is running
echo.
echo Checking if backend is running...
curl -s http://localhost:8000/api/health >nul 2>&1
if errorlevel 1 (
    echo.
    echo [NOTICE] Backend not running. Starting it...
    start cmd /k "cd backend^&& python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
    echo [INFO] Backend started in new window
    timeout /t 3 /nobreak
    echo [INFO] Waiting for backend to initialize...
    timeout /t 3 /nobreak
) else (
    echo [OK] Backend is running at http://localhost:8000
)

REM Set HF_TOKEN if provided
if "%HF_TOKEN%"=="" (
    echo.
    echo WARNING: HF_TOKEN not set
    echo Set it before running: set HF_TOKEN=your_token_here
    echo.
    set HF_TOKEN=test_token
)

REM Run inference
echo.
echo ========================================
echo  Running inference...
echo ========================================
echo.

python inference.py

echo.
echo ========================================
echo  Test Complete
echo ========================================
echo.
echo Output should show:
echo   [START] task=viral_uri env=cliniq model=gpt-4-mini
echo   [STEP] step=1 action=... reward=0.00 done=false error=null
echo   ...
echo   [END] success=true steps=X rewards=...
echo.
