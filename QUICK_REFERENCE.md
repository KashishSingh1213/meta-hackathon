# ⚡ ClinIQ Quick Reference Card

Print this out or bookmark it!

---

## 🚀 Quick Start (2 minutes)

### Windows
```bash
# Terminal 1: Backend
setup.bat
cd backend && venv\Scripts\activate
python -m uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend && npm run dev
```

### Mac/Linux
```bash
# Terminal 1: Backend
./setup.sh
cd backend && source venv/bin/activate
python -m uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend && npm run dev
```

### Docker
```bash
docker-compose up
```

---

## 🎮 Game URLs

| Service | URL | Notes |
|---------|-----|-------|
| Frontend | http://localhost:5173 | Main game interface |
| API Docs | http://localhost:8000/docs | Swagger documentation |
| Health | http://localhost:8000/api/health | API status |

---

## 🔑 Important First Step

**Add your Gemini API key!**

Edit `backend/.env`:
```
GEMINI_API_KEY=your_key_here
```

Get free key: https://makersuite.google.com/app/apikey

---

## 📂 Project Structure

```
backend/          → Python + FastAPI
frontend/         → React + Vite
docker-compose    → Container setup
setup.sh/bat      → Automated setup
```

---

## 🎯 Core API Endpoints

```
POST   /api/reset              - Start game
GET    /api/state              - Current state
POST   /api/step               - Take action
POST   /api/agent/decide       - AI suggestion
GET    /api/episode/summary    - Results
GET    /api/tasks              - Available cases
GET    /api/health             - Health check
```

---

## 🧠 Medical Cases

1. **Viral URI** (🟢 Easy) - 5-7 min
2. **Type 2 Diabetes** (🟡 Medium) - 8-10 min
3. **Sepsis** (🔴 Hard) - 10-12 min
4. **Drug Interaction** (🔴 Hard) - 8-10 min
5. **Rare Disease** (🟣 Expert) - 12-15 min

---

## 🎮 How to Play

1. Pick a medical case
2. Review patient info
3. Request history / Order labs
4. Make diagnosis
5. Recommend treatment
6. Collect XP & achievements
7. See your grade (A-F)

---

## 🤖 Use AI Agent

Click "Let AI Decide" for:
- Case analysis
- Clinical reasoning
- Action suggestion
- Confidence score

---

## 📊 Scoring

| Component | Weight | Notes |
|-----------|--------|-------|
| Accuracy | 40% | Correct diagnosis |
| Safety | 40% | No harmful actions |
| Efficiency | 20% | Few steps needed |

**Grade**: 4.5+ = A, 3.5+ = B, 2.5+ = C, 1.5+ = D, <1.5 = F

---

## 🏆 Achievements

- **Perfect Diagnosis** - Score A
- **Safe Doctor** - 95%+ safety
- **Fast Thinker** - 80%+ efficiency
- **Quick Solver** - 3 steps or less
- **Life Saver** - A/B on Sepsis
- **Medical Sleuth** - A/B on Rare Disease

---

## ⚙️ Backend Files

| File | Purpose |
|------|---------|
| `app/main.py` | FastAPI app |
| `app/routes.py` | API endpoints |
| `app/environment/clinic_env.py` | Game engine |
| `app/environment/case_generator.py` | Patient data |
| `app/graders/task_graders.py` | Scoring |
| `app/ai/gemini_agent.py` | AI integration |
| `app/models/schemas.py` | Data models |

---

## 🎨 Frontend Files

| File | Purpose |
|------|---------|
| `App.jsx` | Main component |
| `TaskSelector.jsx` | Case selection |
| `PatientCard.jsx` | Patient info |
| `ActionPanel.jsx` | Actions UI |
| `RewardChart.jsx` | Score display |
| `EpisodeSummary.jsx` | Results screen |
| `hooks/useEnvironment.js` | Game logic |
| `api/client.js` | API client |

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 8000 in use | `setup.sh` or use port 8001 |
| No API connection | Check CORS_ORIGINS in .env |
| AI not working | Add GEMINI_API_KEY to .env |
| Blank screen | Check browser console (F12) |
| Dependencies fail | Delete node_modules/venv, re-run setup |

---

## 🔧 Key Commands

```bash
# Backend
cd backend && venv\Scripts\activate             # Windows
cd backend && source venv/bin/activate        # Mac/Linux
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
python run.py                                  # Production

# Frontend
cd frontend
npm install
npm run dev                                    # Development
npm run build                                  # Production build
npm run preview                                # Test build locally

# Docker
docker-compose up                              # Start
docker-compose down                            # Stop
docker-compose up --build                      # Rebuild
docker-compose logs -f                         # View logs
```

---

## 📝 Environment Variables

### Backend (.env)
```env
HOST=0.0.0.0
PORT=8000
GEMINI_API_KEY=your_key_here
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
ENVIRONMENT=development
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

---

## 💡 Tips & Tricks

- 🤖 Let AI play first to learn strategies
- 📊 Check performance breakdown after each game
- 🎖️ Try to unlock all achievements
- ⏱️ Challenge yourself to beat your time
- 📈 Level up by earning XP
- 🔄 Retry cases to improve score
- 🎯 Try hard cases for more XP
- 👁️ Check API docs during gameplay

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Full documentation |
| `SETUP_GUIDE.md` | Detailed setup |
| `DEVELOPER_GUIDE.md` | Extension guide |
| `PROJECT_SUMMARY.md` | Project overview |
| This file | Quick reference |

---

## 🌐 Deployment

Ready for:
- Heroku
- Railway
- Render
- AWS
- Google Cloud
- Azure
- DigitalOcean
- Vercel + Backend combo

See DEVELOPER_GUIDE for details.

---

## ❓ FAQ

**Q: Lost my API key?**
A: Get new one at makersuite.google.com

**Q: Can I play offline?**
A: Backend needs Gemini API for AI features

**Q: How many cases?**
A: 5 medical cases, easy to expert

**Q: Is data saved?**
A: XP/achievements saved locally

**Q: Can I add cases?**
A: Yes! See DEVELOPER_GUIDE.md

---

## 📞 Support

1. Check README.md
2. See TROUBLESHOOTING section
3. Review error in browser console
4. Check backend terminal output
5. Verify API at /docs

---

## 🎉 You're Ready!

Run setup → Add API key → Start playing!

```bash
./setup.sh          # or setup.bat on Windows
# Add GEMINI_API_KEY
npm run dev         # Terminal 1: Frontend
python -m uvicorn app.main:app --reload  # Terminal 2: Backend
# Open http://localhost:5173
```

---

**ClinIQ - Clinical Intelligence Query Environment**

*Making medical learning fun and interactive* ⚕️🤖

Enjoy the simulation! 🚀
