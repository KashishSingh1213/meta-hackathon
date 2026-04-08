# Hugging Face Space Deployment Guide

Complete step-by-step guide to deploy ClinIQ to Hugging Face Spaces for the OpenEnv RL Challenge.

## Prerequisites

- ✅ Hugging Face account ([signup here](https://huggingface.co/join))
- ✅ Hugging Face API token ([create here](https://huggingface.co/settings/tokens))
- ✅ Project tested locally with `test-openenv.bat` or `test-openenv.sh`
- ✅ All code committed and working

## Step 1: Create Hugging Face Space

1. Go to https://huggingface.co/new-space
2. Fill in details:
   - **Owner:** Your username
   - **Space name:** `cliniq-openenv` (can be anything)
   - **License:** Apache 2.0 (recommended)
   - **SDK:** Docker ← **IMPORTANT**
   - **Space type:** Private (if submitting to challenge)

3. Click **"Create Space"**

You now have a blank Space repository.

## Step 2: Initialize Git Repository (Local)

From your metahackathon folder:

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: ClinIQ OpenEnv setup"

# Add Hugging Face remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/cliniq-openenv
git branch -M main
git push -u hf main
```

Replace `YOUR_USERNAME` with your actual HF username.

## Step 3: Create/Configure Files for Space

### File 1: Dockerfile (root level)

The Space needs `Dockerfile` in root (lowercase):

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code
COPY . .

# Expose port for health checks
EXPOSE 8000

# Entrypoint
CMD ["python", "inference.py"]
```

### File 2: .env for Space

Create `backend/.env` with Gemini key:

```env
GEMINI_API_KEY=AIzaSyDSBRsIgeVBfTDcMoE9tKh54F2ubTsCIfE
ENVIRONMENT=production
```

### File 3: requirements.txt

Ensure it has:
```
fastapi==0.104.1
uvicorn==0.24.0
google-generativeai==0.3.0
openai==1.3.0
requests==2.31.0
python-dotenv==1.0.0
...
```

## Step 4: Add to Git and Push

```bash
# Add all files
git add Dockerfile backend/.env requirements.txt inference.py

# Commit
git commit -m "Add OpenEnv deployment files"

# Push to Hugging Face
git push hf main
```

## Step 5: Set Space Secrets

Go to your Space on HF: https://huggingface.co/spaces/YOUR_USERNAME/cliniq-openenv

1. Click **Settings** (gear icon, top right)
2. Scroll to **Repository secrets**
3. Add these secrets:

| Secret Name | Value | Notes |
|-------------|-------|-------|
| `HF_TOKEN` | `hf_xxxxxxxxxxxxx` | Your HF API token |
| `API_BASE_URL` | `http://localhost:8000` | Or your custom endpoint |
| `MODEL_NAME` | `gpt-4-mini` | Or your preferred model |

Save secrets.

## Step 6: Monitor Build

1. Go back to Space homepage
2. Scroll down to **Build logs**
3. Watch for:

```
✅ Step 1 : FROM python:3.11-slim
✅ Step 2 : WORKDIR /app
...
✅ Successfully built cliniq-openenv:latest
```

**Build time:** 2-5 minutes first time (may be faster on rebuilds)

### Common Build Issues

**Issue:** "pip install failed"
- **Fix:** Check requirements.txt syntax, all packages exist

**Issue:** "GEMINI_API_KEY not found"
- **Fix:** Ensure `.env` file has valid key in repo

**Issue:** "Build timed out"
- **Fix:** Space has 15min limit; simplify dependencies if needed

## Step 7: Verify Space is Running

Once build completes:

1. **Status badge:** Should show green "**Running**"
2. **Health check:** Space logs should show:
   ```
   ✅ Gemini Agent initialized
   ```
3. **Test endpoint:** (if space exposes port)
   ```bash
   curl https://YOUR_USERNAME-cliniq-openenv.hf.space/api/health
   ```

## Step 8: Generate Submission Output

Your Space now runs `inference.py` automatically. To test it:

### Option A: Via Space UI
1. Go to Space homepage
2. Check logs for output (if interactive)
3. Capture the [START], [STEP], [END] lines

### Option B: Docker Container (local mock)
```bash
docker build -f Dockerfile -t cliniq-space .
docker run -e HF_TOKEN=$HF_TOKEN cliniq-space
```

Should output:
```
[START] task=viral_uri env=cliniq model=gpt-4-mini
[STEP] step=1 action=request_history({}) reward=0.00 done=false error=null
[STEP] step=2 action=order_labs({...}) reward=0.50 done=false error=null
[STEP] step=3 action=diagnose({...}) reward=1.00 done=true error=null
[END] success=true steps=3 rewards=0.00,0.50,1.00
```

## Step 9: Submit to Challenge

1. Go to OpenEnv challenge submission page
2. Paste Space URL: `https://huggingface.co/spaces/YOUR_USERNAME/cliniq-openenv`
3. System validates:
   - ✅ Space is in Running state
   - ✅ inference.py exists in root
   - ✅ Output format is correct
   - ✅ Within resource limits

4. Click **Submit**

## Troubleshooting Deployment

### Space Status: "Building"
- **Duration:** Can take 2-5 minutes
- **Wait:** Don't submit while building
- **Check logs:** Build → View logs

### Space Status: "Error"
- Click **Restart** button
- Check logs for error messages
- Fix issues locally, then `git push hf main`

### Space Status: "Sleeping"
- Reason: Multiple spaces running (HF throttles)
- **Fix:** Stop/delete other unused spaces
- Restart with **Restart** button

### HF_TOKEN Error at Runtime
- Go to Space → Settings → Secrets
- Verify `HF_TOKEN` is set correctly
- Click **Restart** after updating

### Backend Not Responding
- Check `backend/.env` has `GEMINI_API_KEY`
- Check requirements.txt has all packages
- Check docker logs in Space UI
- Local test first: `python inference.py`

### Wrong Output Format
- Review [STEP] line format in `inference.py`
- Test locally first: `python inference.py`
- Compare with expected format in OPENENV_SETUP.md

## Testing Workflow

1. **Local testing** (before pushing)
   ```bash
   bash test-openenv.sh    # Linux/Mac
   # or
   test-openenv.bat        # Windows
   ```

2. **Git push to Space**
   ```bash
   git push hf main
   ```

3. **Monitor build in Space UI**
   - Check Status: Running
   - Check Logs: ✅ Gemini initialized

4. **Verify output format**
   - Capture example run
   - Compare with OpenEnv spec

5. **Submit to Challenge**
   - Paste Space URL
   - Wait for validation
   - Receive score

## Space Maintenance

### After Successful Submission

- Space can remain running (no penalty)
- Or pause to save compute (Settings → Pause)
- Keep git repo clean for future fixes

### Resubmission Workflow

If submission fails:

1. **Fix locally**
   ```bash
   # Edit code
   git add .
   git commit -m "Fix issue XYZ"
   git push hf main
   ```

2. **Wait for rebuild** (2-5 min)

3. **Verify Space status** (Running)

4. **Resubmit**
   - Same Space URL works
   - System re-validates
   - Score recalculated

## Space URL Reference

Your Space will be publicly accessible at:

```
https://huggingface.co/spaces/YOUR_USERNAME/cliniq-openenv
```

Use this URL for:
- ✅ Challenge submission
- ✅ Sharing with others
- ✅ Monitoring/debugging
- ✅ Resubmissions

## Support & Resources

- 📖 [HF Spaces Docs](https://huggingface.co/docs/hub/spaces)
- 🐛 [HF Spaces Issues](https://github.com/huggingface/hub-docs/issues)
- 💬 [HF Community](https://discuss.huggingface.co)
- 📧 [OpenEnv Support](https://github.com/meta-pytorch/OpenEnv/issues)

---

## Submission Verification Checklist

Before final submission, verify:

- [ ] Space URL works: https://hf.co/spaces/USERNAME/cliniq-openenv
- [ ] Space shows "Running" status (green)
- [ ] `inference.py` in root directory
- [ ] Output includes [START], [STEP], [END]
- [ ] Rewards formatted to 2 decimals (0.00)
- [ ] Success/done are lowercase (true/false)
- [ ] No HF_TOKEN errors in logs
- [ ] Backend health check passes
- [ ] Gemini Agent initialized successfully
- [ ] Resource usage within limits

✅ **Ready to submit!**

---
**Last Updated:** 2026-04-08  
**Version:** 1.0.0
