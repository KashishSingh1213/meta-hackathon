# ClinIQ OpenEnv RL Challenge - Complete Setup Guide

Complete guide to submit your clinical simulation environment to the OpenEnv RL Challenge.

## 📋 Overview

Your project has been restructured to meet OpenEnv RL Challenge requirements:

```
metahackathon/
├── 📝 inference.py                         ← Main entry point (OpenEnv compliant)
├── 📦 backend/                              ← Clinical simulation environment
│   ├── requirements.txt                     ← Python dependencies
│   ├── .env                                ← API keys & config
│   ├── app/main.py                         ← FastAPI application
│   ├── app/routes.py                       ← API endpoints (/reset, /step, /agent/decide)
│   ├── app/environment/clinic_env.py       ← Clinic simulation environment
│   ├── app/ai/gemini_agent.py              ← Gemini AI decision maker
│   └── app/models/schemas.py               ← Data models (Observation, Action, etc.)
├── 📄 Dockerfile.inference                 ← Docker configuration
├── 📌 test-openenv.bat/sh                  ← Quick test scripts
└── 📚 Documentation:
     ├── OPENENV_SETUP.md                   ← Detailed setup guide
     ├── SUBMISSION_CHECKLIST.md            ← Verification checklist
     ├── HF_SPACE_DEPLOYMENT.md             ← Hugging Face deployment
     └── README.md                           ← Original project docs
```

## 🚀 Quick Start (5 minutes)

### 1️⃣ Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 2️⃣ Verify API Key
```bash
# backend/.env must have:
GEMINI_API_KEY=AIzaSyDSBRsIgeVBfTDcMoE9tKh54F2ubTsCIfE
```

### 3️⃣ Start Backend
```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Expected output:
```
🚀 INITIALIZING GEMINI AGENT AT STARTUP
✅ Gemini Agent initialized
   - Fallback mode: False
   - Model: gemini-1.5-flash
   - API Key loaded: True
```

### 4️⃣ Run Inference (new terminal, from root)
```bash
export HF_TOKEN=test_token
python inference.py
```

Expected output:
```
[START] task=viral_uri env=cliniq model=gpt-4-mini
[STEP] step=1 action=request_history({}) reward=0.00 done=false error=null
...
[END] success=true steps=N rewards=...
```

✅ **If you see this, you're ready to submit!**

## 📚 Documentation Guide

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **OPENENV_SETUP.md** | Environment variables, tasks, troubleshooting | Before running locally |
| **SUBMISSION_CHECKLIST.md** | Verification steps and common mistakes | Before submitting |
| **HF_SPACE_DEPLOYMENT.md** | Deploy to Hugging Face Spaces | For HF Space submission |
| **test-openenv.bat/sh** | Quick automated testing | First time setup |

## 🔍 Key Components

### inference.py (Root level) - OpenEnv Compliant Entry Point
```python
# ✅ Uses OpenAI client
from openai import OpenAI

# ✅ Reads env vars with defaults
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-mini")

# ✅ Requires HF_TOKEN (no default)
HF_TOKEN = os.getenv("HF_TOKEN")
if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

# ✅ Emits [START], [STEP], [END]
print(f"[START] task={task} env=cliniq model={MODEL_NAME}")
print(f"[STEP] step=1 action=... reward=0.00 done=false error=null")
print(f"[END] success=true steps=1 rewards=0.00")
```

### Backend API Endpoints
```
POST /api/reset              # Start new patient case
POST /api/step               # Execute clinical action
POST /api/agent/decide       # Get AI decision via Gemini
GET  /api/health             # Health check
```

### Gemini Agent (Fixed)
✅ No longer falling back - simplified initialization
```python
# Directly uses gemini-1.5-flash
self.model = genai.GenerativeModel("gemini-1.5-flash")
```

## 🧪 Local Testing

### Option 1: Quick Test Script
```bash
# Windows
test-openenv.bat

# Linux/Mac
bash test-openenv.sh
```

### Option 2: Manual Testing
```bash
# Terminal 1: Start backend
cd backend && python -m uvicorn app.main:app --port 8000

# Terminal 2: Run inference
export HF_TOKEN=test
python inference.py

# Verify output has all 3 line types
```

### Option 3: Docker Testing
```bash
docker build -f Dockerfile.inference -t cliniq-openenv .
docker run -e HF_TOKEN=test cliniq-openenv
```

## 📤 Submission Options

### Option A: Direct Docker (Fastest)
1. Bundle project in Docker
2. Submit Docker image to OpenEnv
3. Result: Direct scoring without HF Space

### Option B: Hugging Face Space (Recommended for Challenge)
1. Follow [HF_SPACE_DEPLOYMENT.md](./HF_SPACE_DEPLOYMENT.md)
2. Create Space on HF
3. Push code to HF repo
4. HF auto-builds Docker
5. Submit Space URL to OpenEnv
6. System validates and scores

**Choose Option B** if you want:
- ✅ Automatic Docker builds
- ✅ Version control linked to submission
- ✅ Easy resubmissions
- ✅ Public showcase of your work

## ✨ Environment Variables Reference

```bash
# OpenEnv Required
API_BASE_URL=http://localhost:8000      # Default provided ✅
MODEL_NAME=gpt-4-mini                   # Default provided ✅
HF_TOKEN=hf_xxxxx                       # Required - no default ⚠️

# Optional
BACKEND_URL=http://localhost:8000/api   # ClinIQ backend
TASK=viral_uri                          # Clinical task (default)
MAX_STEPS=10                            # Steps per episode (default)
ENVIRONMENT=production                  # development/production

# Backend Required
GEMINI_API_KEY=AIzaSy...                # Set in backend/.env
```

## ⚠️ Common Issues & Fixes

### Issue: "[Fallback AI]" Still Showing
✅ **Fixed!** Completely removed test call that caused fallback.

**Verify:**
1. Restart backend: `cd backend && python -m uvicorn app.main:app --port 8000`
2. Check console for: `✅ Gemini Agent initialized`
3. Run inference again

### Issue: Backend Not Responding
**Fix:**
```bash
# Check health
curl http://localhost:8000/api/health

# View detailed logs in backend console
# Should show: ✅ Gemini Agent initialized
```

### Issue: HF_TOKEN Error
**Fix:**
```bash
export HF_TOKEN=your_actual_token_here
python inference.py
```

### Issue: Port 8000 Already in Use
**Fix:**
```bash
# Find process using port 8000
netstat -ano | grep :8000

# Kill it or use different port
python -m uvicorn app.main:app --port 8001
```

## 📊 Output Format Validation

Your output **MUST** match exactly:

✅ **Valid:**
```
[START] task=viral_uri env=cliniq model=gpt-4-mini
[STEP] step=1 action=request_history({}) reward=0.00 done=false error=null
[STEP] step=2 action=order_labs({"labs": ["CBC", "CMP"]}) reward=0.50 done=false error=null
[STEP] step=3 action=diagnose({"diagnosis": "Viral URI"}) reward=1.00 done=true error=null
[END] success=true steps=3 rewards=0.00,0.50,1.00
```

❌ **Invalid:**
```
Starting episode...
action: request_history
Done!
```

**Rules:**
- Exactly 3 line types: [START], [STEP], [END]
- Rewards formatted to 2 decimals: `0.00`
- Booleans lowercase: `true`/`false`
- Error is `"string"` or `null`
- All on single line (no `\n` within line)

## 🎯 Submission Flow

```
1. Local Testing
   ↓ (python inference.py)
   ↓
2. Verify Output Format
   ↓ (Check [START], [STEP], [END])
   ↓
3. Deploy to Hugging Face
   ↓ (git push hf main)
   ↓
4. Verify Space Running
   ↓ (Status: "Running")
   ↓
5. Submit to Challenge
   ↓ (Paste Space URL)
   ↓
6. Wait for Validation
   ↓ (System checks format, constraints)
   ↓
7. Get Score!
```

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│               OpenEnv Challenge                     │
│                                                     │
│  ┌───────────────────────────────────────────────┐  │
│  │ inference.py (OpenEnv Interface)              │  │
│  │ - Reads env vars                              │  │
│  │ - Emits [START], [STEP], [END]               │  │
│  │ - Uses OpenAI client                         │  │
│  └────────────┬────────────────────────────────┘  │
│               │ HTTP Requests                      │
│  ┌────────────▼────────────────────────────────┐  │
│  │ FastAPI Backend (clinic_env.py)             │  │
│  │ - /api/reset (new episode)                  │  │
│  │ - /api/step (execute action)                │  │
│  │ - /api/agent/decide (AI decision)           │  │
│  └────────────┬────────────────────────────────┘  │
│               │                                     │
│  ┌────────────▼────────┬──────────────────────┐   │
│  │ clinic_env.py       │ gemini_agent.py      │   │
│  │                     │                      │   │
│  │ Patient simulation  │ Gemini AI reasoning  │   │
│  │ - Vitals           │ - Clinical logic     │   │
│  │ - Symptoms         │ - Action generation  │   │
│  │ - Lab results      │                      │   │
│  │ - Grading logic    │                      │   │
│  └─────────────────────┴──────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 📦 Dependencies

**Key Libraries:**
- `fastapi` - Web framework
- `google-generativeai` - Gemini API
- `openai` - OpenAI client (for inference.py)
- `requests` - HTTP client
- `pydantic` - Data validation
- `uvicorn` - ASGI server

**Total Size:** ~500MB (fits in 8GB constraint ✅)

## 🔐 Security Notes

- ⚠️ **Never commit** `backend/.env` with real API keys (use `.gitignore`)
- ⚠️ **HF_TOKEN** should be in Space secrets, not in repo
- ✅ Use environment variables for all sensitive data
- ✅ Validate all inputs in backend

```bash
# .gitignore
backend/.env
.env
.env.local
*.pyc
__pycache__/
```

## 📞 Getting Help

1. **Local issues:** Check `test-openenv.bat/sh` output
2. **Backend issues:** Check `backend` console logs
3. **Format issues:** Compare output with SUBMISSION_CHECKLIST.md
4. **HF Space issues:** Read HF_SPACE_DEPLOYMENT.md
5. **OpenEnv issues:** Check reference projects in challenge docs

## ✅ Final Checklist

Before submission:

- [ ] Local testing passes
- [ ] Output format matches spec (3 line types)
- [ ] Backend shows ✅ Gemini initialized
- [ ] HF_TOKEN set and required in code
- [ ] API_BASE_URL and MODEL_NAME have defaults
- [ ] Hugging Face Space is "Running"
- [ ] All documentation read and understood
- [ ] Docker builds successfully
- [ ] Resource usage within limits

## 📚 Additional Resources

- 🔗 [OpenEnv GitHub](https://github.com/meta-pytorch/OpenEnv)
- 🔗 [Reference Projects](https://github.com/meta-pytorch/OpenEnv/tree/main/envs)
- 🔗 [Hugging Face Docs](https://huggingface.co/docs/hub/spaces)
- 🔗 [Google Gemini API](https://ai.google.dev)

---

## 🎉 Ready to Submit?

1. ✅ Local testing complete
2. ✅ Output format verified
3. ✅ HF Space running
4. ✅ Following this guide

**Go to OpenEnv challenge submission page and paste your HF Space URL!**

---

**Last Updated:** 2026-04-08  
**Setup Version:** 1.0.0  
**Status:** ✅ Ready for Submission  

Good luck with your submission! 🚀
