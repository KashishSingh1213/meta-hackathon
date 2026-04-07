# 🚀 ClinIQ Setup Guide

Complete step-by-step guide to get ClinIQ running on your system.

## ⚡ Prerequisites

Before you start, ensure you have:

- ✅ Python 3.11 or higher
- ✅ Node.js 18+ and npm
- ✅ Git (optional, for cloning)
- ✅ Google Gemini API Key (free at [makersuite.google.com](https://makersuite.google.com/app/apikey))

### Get Your Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy your key (starts with `AI...`)
4. Keep it safe!

## 🖥️ Windows Setup

### Step 1: Extract Project

```bash
# Navigate to where you want the project
cd Documents
# Unzip or clone the project
# cd metahackathon
```

### Step 2: Run Setup Script

```bash
cd metahackathon
setup.bat
```

This will:
- ✓ Check Python and Node.js
- ✓ Create virtual environment
- ✓ Install dependencies
- ✓ Create .env files

### Step 3: Add Gemini API Key

Edit `backend\.env`:
```
GEMINI_API_KEY=your_actual_key_here
```

### Step 4: Start Backend

```bash
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 5: Start Frontend (in new terminal)

```bash
cd frontend
npm run dev
```

Expected output:
```
  ➜  Local:   http://localhost:5173/
```

### Step 6: Open in Browser

- Open: http://localhost:5173
- Enjoy! 🎮

---

## 🍎 Mac/Linux Setup

### Step 1: Extract Project

```bash
cd Documents
# Extract or clone
cd metahackathon
```

### Step 2: Run Setup Script

```bash
chmod +x setup.sh
./setup.sh
```

### Step 3: Add Gemini API Key

Edit `backend/.env`:
```bash
nano backend/.env
# or
vim backend/.env
```

Add:
```
GEMINI_API_KEY=your_actual_key_here
```

### Step 4: Start Backend

```bash
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload
```

### Step 5: Start Frontend (new terminal)

```bash
cd frontend
npm run dev
```

### Step 6: Open in Browser

http://localhost:5173

---

## 🐳 Docker Setup (All Platforms)

If you have Docker installed:

### Step 1: Create .env File

```bash
cp backend/.env.example .env
```

Edit `.env`:
```
GEMINI_API_KEY=your_actual_key_here
```

### Step 2: Start Services

```bash
docker-compose up
```

Wait for output:
```
cliniq-backend    | INFO:     Uvicorn running on http://0.0.0.0:8000
cliniq-frontend   | Accepting connections at http://localhost:3000
```

### Step 3: Open Browser

http://localhost:3000 (or http://localhost:5173)

---

## ✅ Verification Checklist

After starting, verify everything works:

### Backend Check

```bash
# Terminal 1
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "ClinIQ",
  "version": "1.0.0"
}
```

### API Documentation

Visit: http://localhost:8000/docs

### Frontend Check

Visit: http://localhost:5173

You should see:
- ✓ ClinIQ header
- ✓ 5 medical cases
- ✓ Game dashboard

---

## 🎮 First Game

1. Click any case (start with "Viral URI" for easy intro)
2. Read patient information
3. Click "Request History" to understand the case
4. Click "Order Labs" to get diagnostic data
5. Click "Make Diagnosis" to enter your diagnosis
6. Click "Recommend Treatment"
7. See your score!

---

## 🤖 Using AI Agent

Once the game is running:

1. Click "Let AI Decide" button
2. Watch AI analyze the case
3. AI will suggest the next clinical action
4. Review AI reasoning
5. Approve and continue

---

## 🔧 Troubleshooting

### Backend won't start

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
cd backend
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Port 8000 already in use

**Problem**: `Address already in use`

**Solution**:
```bash
# Kill process using port 8000
# Mac/Linux:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Or use different port**:
```bash
python -m uvicorn app.main:app --port 8001
# Update frontend VITE_API_URL to http://localhost:8001
```

### Frontend won't load

**Problem**: Blank page or errors

**Solution**:
```bash
cd frontend
npm cache clean --force
rm -rf node_modules
npm install
npm run dev
```

### Gemini API errors

**Problem**: `APIConnectionError` or `APIAuthError`

**Solution**:
- Check API key is correct
- Visit https://makersuite.google.com/app/apikey
- Generate new key if needed
- Restart backend after updating

### CORS errors

**Problem**: Browser console shows CORS error

**Solution**:
- Check `CORS_ORIGINS` in `backend/.env`
- Should include: `http://localhost:5173` and `http://localhost:3000`
- Restart backend

```env
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

---

## 📊 Project Structure

```
metahackathon/
├── backend/
│   ├── app/
│   │   ├── models/          # Data models
│   │   ├── environment/     # Game environment
│   │   ├── graders/         # Scoring logic
│   │   ├── ai/              # Gemini integration
│   │   ├── main.py          # FastAPI app
│   │   └── routes.py        # API endpoints
│   ├── requirements.txt
│   ├── .env                 # Your config
│   └── run.py              # Production runner
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── hooks/           # Custom hooks
│   │   ├── api/             # API client
│   │   ├── App.jsx          # Main app
│   │   └── index.css        # Tailwind
│   ├── package.json
│   ├── vite.config.js
│   └── .env                 # Your config
├── docker-compose.yml       # Docker setup
├── README.md               # Full documentation
├── setup.sh                # Mac/Linux setup
└── setup.bat               # Windows setup
```

---

## 🚀 Next Steps

### After Setup Works:

1. **Explore Cases**: Try all 5 medical cases
2. **Use AI Agent**: Let Gemini help you solve cases
3. **Check Achievements**: Unlock badges for good performance
4. **Compare Scores**: Challenge yourself on harder cases
5. **Customize**: Add your own medical cases

### Customization Options:

**Add New Case**:
```python
# In backend/app/environment/case_generator.py
@staticmethod
def generate_your_case() -> Observation:
    # Create case...
    return observation
```

**Add New Achievement**:
```python
# In backend/app/environment/clinic_env.py
def _get_achievements(self, grade, breakdown):
    achievements = []
    # Add logic...
    return achievements
```

---

## ❓ FAQ

**Q: What if I don't have a Gemini API key?**
A: The game still works without AI! Just won't suggest actions. Get a free key at makersuite.google.com

**Q: Can I run just the frontend without backend?**
A: No, the frontend needs the backend API. Both are required.

**Q: Can I deploy this online?**
A: Yes! Use Railway, Render, or Heroku for free hosting.

**Q: Is my Gemini API key safe?**
A: Keep it in `.env` file (not git). Never commit .env files.

**Q: How do I reset everything?**
A: Delete `backend/venv` and `frontend/node_modules`, then re-run setup.

---

## 📞 Need Help?

1. Check README.md for full documentation
2. Review error messages carefully
3. Check API docs at http://localhost:8000/docs
4. Verify Python/Node versions
5. Try running setup script again

---

## 🎉 You're All Set!

Now enjoy your ClinIQ experience!

**Quick Reminders:**
- Keep terminals open while playing
- Don't forget to add Gemini API key
- Enjoy the medical cases
- Share your scores! 📊

Happy learning! ⚕️🤖
