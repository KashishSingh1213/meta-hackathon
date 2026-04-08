# OpenEnv RL Challenge - ClinIQ Submission Setup

## Overview
This document explains how to set up and run the ClinIQ project for the OpenEnv RL Challenge.

## Project Structure
```
metahackathon/
├── inference.py                 # ✅ Main entry point (OpenEnv compliant)
├── backend/                     # ClinIQ environment server
│   ├── requirements.txt         # Python dependencies
│   ├── .env                    # Environment variables
│   └── app/
│       ├── environment/        # Clinic simulation environment
│       ├── ai/                # Gemini AI agent
│       └── routes.py          # FastAPI endpoints
├── frontend/                    # React UI (optional for inference)
├── docker-compose.yml          # Docker setup
└── README.md
```

## Quick Start

### 1. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 2. Set Environment Variables

**For Local Testing:**
```bash
# Backend server
export API_BASE_URL=http://localhost:8000
export MODEL_NAME=gpt-4-mini
export HF_TOKEN=<your-hugging-face-token>

# Optional: Override backend URL for inference
export BACKEND_URL=http://localhost:8000/api
```

**For Hugging Face Space Submission:**
The system will automatically set these variables. Just ensure:
- `HF_TOKEN` is set in Hugging Face Space secrets
- `API_BASE_URL` and `MODEL_NAME` have defaults in `inference.py`

### 3. Start Backend Server
```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Backend will show:
```
🚀 INITIALIZING GEMINI AGENT AT STARTUP
✅ Gemini Agent initialized
   - Fallback mode: False
   - Model: gemini-1.5-flash
   - API Key loaded: True
```

### 4. Run Inference

**Local Testing:**
```bash
python inference.py
```

**With Specific Task:**
```bash
TASK=viral_uri MAX_STEPS=10 python inference.py
```

## Expected Output Format

The script emits three types of lines to stdout:

```
[START] task=viral_uri env=cliniq model=gpt-4-mini
[STEP] step=1 action=request_history({}) reward=0.00 done=false error=null
[STEP] step=2 action=order_labs({...}) reward=0.50 done=false error=null
[STEP] step=3 action=diagnose({...}) reward=1.00 done=true error=null
[END] success=true steps=3 rewards=0.00,0.50,1.00
```

## Environment Variables Reference

| Variable | Default | Required | Notes |
|----------|---------|----------|-------|
| `API_BASE_URL` | `http://localhost:8000` | Yes* | LLM API endpoint |
| `MODEL_NAME` | `gpt-4-mini` | Yes* | Model identifier |
| `HF_TOKEN` | - | **Yes** | Hugging Face API token |
| `BACKEND_URL` | `http://localhost:8000/api` | No | ClinIQ backend API |
| `TASK` | `viral_uri` | No | Clinical task name |
| `MAX_STEPS` | `10` | No | Max steps per episode |

*Must have defaults in code per OpenEnv requirements

## Available Tasks

These clinical cases are available:

1. **viral_uri** - Viral Upper Respiratory Infection (default)
2. **gastroenteritis** - Acute Gastroenteritis
3. **pneumonia** - Community-Acquired Pneumonia
4. **acute_coronary** - Acute Coronary Syndrome
5. **stroke** - Ischemic Stroke

### Run Specific Task:
```bash
TASK=pneumonia python inference.py
```

## Backend Endpoints Used by inference.py

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/reset` | POST | Initialize new patient case |
| `/api/step` | POST | Execute clinical action |
| `/api/agent/decide` | POST | Get AI agent decision |

## Troubleshooting

### Issue: "[Fallback AI]" in responses
**Solution:** Ensure `GEMINI_API_KEY` is set in `backend/.env`:
```bash
# backend/.env
GEMINI_API_KEY=AIzaSyDSBRsIgeVBfTDcMoE9tKh54F2ubTsCIfE
```

### Issue: Backend not responding
**Check:**
```bash
# Verify backend is running
curl http://localhost:8000/api/health

# Check logs in backend console
# Should see: ✅ Gemini Agent initialized
```

### Issue: HF_TOKEN error
**Solution:** Set the environment variable:
```bash
export HF_TOKEN=hf_your_actual_token_here
```

## Docker Deployment

### For Hugging Face Space:

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

# Copy app
COPY . .

# Set entrypoint
ENTRYPOINT ["python", "inference.py"]
```

**Building:**
```bash
docker build -t cliniq-inference .
docker run -e HF_TOKEN=$HF_TOKEN cliniq-inference
```

## Output Validation

Your output must follow this exact format:

✅ **Valid:**
```
[START] task=viral_uri env=cliniq model=gpt-4-mini
[STEP] step=1 action=request_history({}) reward=0.00 done=false error=null
[END] success=true steps=1 rewards=0.00
```

❌ **Invalid:**
```
[START] task=viral_uri env=cliniq model=gpt-4-mini
Episode starting...
[STEP] action=request_history
Done!
```

## Performance Notes

- **Memory:** ~500MB for backend + model
- **CPU:** Single core sufficient for inference
- **Latency:** ~2-5s per step (network + Gemini API)

Fits within OpenEnv constraints (2 vCPU, 8GB RAM) ✅

## Hugging Face Space Submission Checklist

- [ ] `inference.py` in root directory
- [ ] `API_BASE_URL` has default value
- [ ] `MODEL_NAME` has default value
- [ ] `HF_TOKEN` marked as required/secret in Space
- [ ] Space is in "Running" state
- [ ] Backend Docker container configured
- [ ] Output format validated
- [ ] `requirements.txt` includes `openai` and `requests`

## Support

- Reference implementations: https://github.com/meta-pytorch/OpenEnv/tree/main/envs
- Check console output for detailed error messages
- Verify backend health: `curl http://localhost:8000/api/health`

---
**Last Updated:** 2026-04-08  
**Version:** 1.0.0
