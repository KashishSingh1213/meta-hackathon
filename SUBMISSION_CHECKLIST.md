# OpenEnv Submission Checklist

## ✅ Project Structure
- [x] `inference.py` exists in root directory
- [x] `backend/requirements.txt` includes all dependencies
- [x] `backend/.env` has GEMINI_API_KEY set
- [x] All environment variables have defaults (except HF_TOKEN)

## ✅ Code Requirements
- [x] Uses `OpenAI` client from `from openai import OpenAI`
- [x] Reads `API_BASE_URL` env var with default
- [x] Reads `MODEL_NAME` env var with default
- [x] **Requires** `HF_TOKEN` env var (no default)
- [x] No direct HTTP calls, using requests + OpenAI client
- [x] Emits exact 3 line types: [START], [STEP], [END]

## ✅ Output Format
- [x] [START] line: `task=<name> env=<name> model=<name>`
- [x] [STEP] line: `step=<n> action=<str> reward=<0.00> done=<bool> error=<msg|null>`
- [x] [END] line: `success=<bool> steps=<n> rewards=<0.00,...>`
- [x] Reward/rewards formatted to 2 decimal places
- [x] done/success are lowercase: true|false
- [x] error is JSON string or null
- [x] All on single line (no newlines within line)

## ✅ Environment Variables Verification

Run these commands locally to verify:

```bash
# 1. Check API_BASE_URL default
grep -n "API_BASE_URL.*default" inference.py
# Should show: API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# 2. Check MODEL_NAME default
grep -n "MODEL_NAME.*default" inference.py
# Should show: MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-mini")

# 3. Check HF_TOKEN required
grep -n "HF_TOKEN.*required" inference.py
# Should show: raise ValueError("HF_TOKEN environment variable is required")

# 4. Verify no direct HTTP requests (besides requests lib usage)  
grep -n "http\|https" inference.py | grep -v "localhost" | grep -v "#"
# Should only show necessary URLs in docstrings

# 5. Verify OpenAI import
grep -n "from openai import OpenAI" inference.py
# Must exist
```

## ✅ Testing Checklist

### Local Testing
```bash
# Step 1: Install dependencies
cd backend
pip install -r requirements.txt

# Step 2: Start backend in one terminal
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Step 3: Run inference in another terminal (from root)
export HF_TOKEN=test_token_for_local_testing
python inference.py

# Expected output:
# [START] task=viral_uri env=cliniq model=gpt-4-mini
# [STEP] step=1 action=... reward=0.00 done=false error=null
# ...
# [END] success=true steps=X rewards=...
```

### Docker Testing
```bash
# Build
docker build -f Dockerfile.inference -t cliniq-openenv .

# Run with HF_TOKEN
docker run -e HF_TOKEN=$HF_TOKEN \
           -e BACKEND_URL=http://host.docker.internal:8000/api \
           cliniq-openenv

# Should output same format
```

## ✅ Hugging Face Space Setup

### 1. Create Space
- Go to https://huggingface.co/new-space
- Space name: `cliniq-openenv` (or your choice)
- License: Apache 2.0
- Space SDK: Docker

### 2. Repository Structure
```
space-repo/
├── Dockerfile           (use Dockerfile.inference)
├── inference.py         (copy from root)
├── backend/
│   ├── requirements.txt
│   └── app/
│       └── ...
```

### 3. Repository Secrets (Settings → Secrets)
Set these environment variables in Space:
```
HF_TOKEN = hf_your_actual_token_here
API_BASE_URL = https://your-api-endpoint.com (if different)
MODEL_NAME = gpt-4-mini (or your model)
```

### 4. Space Configuration
- **Docker image**: Auto-built from Dockerfile
- **Port**: 8000 (for health checks)
- **Startup time**: ~2-3 minutes for first build

### 5. Verify Space is Running
- Go to your Space URL: `https://huggingface.co/spaces/YOUR_USERNAME/cliniq-openenv`
- Status should show: **"Running"** (green)
- Check logs for: `✅ Gemini Agent initialized`

## ✅ Common Mistakes to AVOID

❌ **DON'T:**
- [ ] Put `inference.py` in `backend/` or `frontend/` subfolder
- [ ] Use direct `http.request()` or `urllib` instead of requests lib
- [ ] Forget HF_TOKEN requirement check
- [ ] Forget default values for API_BASE_URL and MODEL_NAME
- [ ] Format rewards as `0` instead of `0.00`
- [ ] Use `True/False` instead of `true/false`
- [ ] Include multiple lines in a single output line
- [ ] Keep multiple Hugging Face spaces running (turn off others)
- [ ] Submit while space is still "Building"

✅ **DO:**
- [ ] Use OpenAI client consistently
- [ ] Validate all 3 line types in output
- [ ] Test locally before HF submission
- [ ] Check Space is in "Running" state
- [ ] Include error handling with proper [END] line
- [ ] Follow OpenEnv examples

## ✅ Performance Validation

**Must fit within:**
- CPU: 2 vCPU
- RAM: 8 GB
- Check: `du -sh .` (size of project)

Run locally and note:
- Memory usage: ~500MB ✅
- Startup time: ~30s ✅
- Per-step latency: ~2-5s (API call) ✅

## ✅ Final Submission

Before clicking "Submit":

1. [ ] All code changes committed
2. [ ] `.env` file updated with GEMINI_API_KEY
3. [ ] `requirements.txt` has openai + requests
4. [ ] `inference.py` in root directory
5. [ ] Local testing passes with correct output format
6. [ ] Hugging Face Space is **RUNNING** (not Building/Sleeping)
7. [ ] HF_TOKEN set in Space secrets
8. [ ] Docker successfully builds in Space

## Submission URL
- **Main Challenge:** [OpenEnv RL Challenge Submission]
- **Your Space:** [Link to your HF Space will go here]

---
**Quick Links:**
- 📖 [OpenEnv Docs](https://github.com/meta-pytorch/OpenEnv)
- 🤗 [Hugging Face Spaces](https://huggingface.co/spaces)
- 🔐 [HF Tokens](https://huggingface.co/settings/tokens)
- 💾 [This Setup Guide](./OPENENV_SETUP.md)

**Last Updated:** 2026-04-08
