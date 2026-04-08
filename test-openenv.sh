#!/bin/bash
# Quick test script for ClinIQ OpenEnv setup (Linux/Mac)
# Usage: bash test-openenv.sh

set -e

echo ""
echo "========================================"
echo " ClinIQ OpenEnv - Quick Test"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 not found. Install Python 3.11+"
    exit 1
fi
python3 --version
echo "[OK] Python found"

# Check inference.py exists
if [ ! -f "inference.py" ]; then
    echo "ERROR: inference.py not found in current directory"
    exit 1
fi
echo "[OK] inference.py found"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip3 install -q -r backend/requirements.txt || exit 1
echo "[OK] Dependencies installed"

# Check .env
if [ ! -f "backend/.env" ]; then
    echo "WARNING: backend/.env not found"
else
    if grep -q "GEMINI_API_KEY" backend/.env; then
        echo "[OK] backend/.env configured"
    else
        echo "WARNING: GEMINI_API_KEY not set in backend/.env"
    fi
fi

# Check backend is running
echo ""
echo "Checking if backend is running..."
if ! curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo ""
    echo "[NOTICE] Backend not running. Starting it..."
    cd backend
    python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    cd ..
    echo "[INFO] Backend started (PID: $BACKEND_PID)"
    sleep 5
    echo "[INFO] Backend should be ready"
else
    echo "[OK] Backend is running at http://localhost:8000"
fi

# Check HF_TOKEN
if [ -z "$HF_TOKEN" ]; then
    echo ""
    echo "WARNING: HF_TOKEN not set"
    echo "Set it before running: export HF_TOKEN=your_token_here"
    echo ""
    export HF_TOKEN="test_token"
fi

# Run inference
echo ""
echo "========================================"
echo " Running inference..."
echo "========================================"
echo ""

python3 inference.py

echo ""
echo "========================================"
echo " Test Complete"
echo "========================================"
echo ""
echo "Output should show:"
echo "  [START] task=viral_uri env=cliniq model=gpt-4-mini"
echo "  [STEP] step=1 action=... reward=0.00 done=false error=null"
echo "  ..."
echo "  [END] success=true steps=X rewards=..."
echo ""

# Cleanup
if [ ! -z "$BACKEND_PID" ]; then
    echo "Stopping backend (PID: $BACKEND_PID)..."
    kill $BACKEND_PID 2>/dev/null || true
fi
