#!/bin/bash

# ClinIQ Quick Setup Script
set -e

echo "🏥 ClinIQ - Clinical Intelligence Query Environment"
echo "=================================================="
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check Python
echo "${BLUE}Checking Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo "${YELLOW}Python 3 not found. Please install Python 3.11+${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
echo "${GREEN}✓ Python $PYTHON_VERSION found${NC}"
echo ""

# Check Node
echo "${BLUE}Checking Node.js...${NC}"
if ! command -v node &> /dev/null; then
    echo "${YELLOW}Node.js not found. Please install Node.js 18+${NC}"
    exit 1
fi
NODE_VERSION=$(node --version)
echo "${GREEN}✓ Node.js $NODE_VERSION found${NC}"
echo ""

# Setup Backend
echo "${BLUE}Setting up backend...${NC}"
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists"
fi

# Activate
echo "Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt -q

# Check .env
if [ ! -f ".env" ]; then
    echo "Creating .env from template..."
    cp .env.example .env
    echo "${YELLOW}⚠ Please edit backend/.env with your GEMINI_API_KEY${NC}"
else
    echo "${GREEN}✓ .env already exists${NC}"
fi
echo ""

cd ..

# Setup Frontend
echo "${BLUE}Setting up frontend...${NC}"
cd frontend

# Install dependencies
echo "Installing npm dependencies..."
npm install -q

# Check .env
if [ ! -f ".env" ]; then
    echo "Creating .env from template..."
    cp .env.example .env
    echo "${GREEN}✓ Frontend .env created${NC}"
else
    echo "${GREEN}✓ .env already exists${NC}"
fi
echo ""

cd ..

echo "${GREEN}=================================================="
echo "✅ Setup complete!"
echo "=================================================="
echo ""
echo "${BLUE}Next steps:${NC}"
echo ""
echo "1. Update your Gemini API key:"
echo "   Edit: backend/.env"
echo "   Get free key: https://makersuite.google.com/app/apikey"
echo ""
echo "2. Start the backend:"
echo "   cd backend"
echo "   source venv/bin/activate  (or: venv\\Scripts\\activate on Windows)"
echo "   python -m uvicorn app.main:app --reload"
echo ""
echo "3. In another terminal, start the frontend:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "4. Open http://localhost:5173 in your browser"
echo ""
