# 🏥 ClinIQ - Clinical Intelligence Query Environment

A production-ready, full-stack AI-powered medical simulation platform that combines clinical decision-making challenges with gamified elements. Perfect for medical training, AI research, and clinical skill development.

## 🎯 Overview

**ClinIQ** is a complete clinical decision-making simulator where users and AI agents navigate realistic medical cases through a gamified environment. The platform features:

- ✅ **5 Progressive Medical Cases** (easy to expert difficulty)
- ✅ **AI-Powered Agent** (Gemini API integration)
- ✅ **Real-time Scoring System** (accuracy, safety, efficiency)
- ✅ **Gamification** (XP, levels, achievements)
- ✅ **Modern Glassmorphism UI** (dark theme, smooth animations)
- ✅ **OpenAI Gym-style Backend** (reset, step, state API)
- ✅ **Production-Ready Code** (FastAPI + React + Vite)

## 🏗️ Project Structure

```
/metahackathon
├── /backend
│   ├── /app
│   │   ├── /models              # Pydantic schemas
│   │   ├── /environment         # ClinIQEnvironment class
│   │   ├── /graders            # Task graders
│   │   ├── /ai                 # Gemini AI integration
│   │   ├── routes.py           # FastAPI routes
│   │   └── main.py             # FastAPI app
│   ├── requirements.txt
│   ├── .env.example
│   └── .gitignore
├── /frontend
│   ├── /src
│   │   ├── /components         # React components
│   │   ├── /hooks              # Custom hooks
│   │   ├── /api                # API client
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── .env.example
│   └── .gitignore
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn
- Docker & Docker Compose (optional)
- Gemini API Key (free from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Option 1: Local Development

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Or (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Run backend
python -m uvicorn app.main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/api/health`

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Run development server
npm run dev
```

Frontend will be available at `http://localhost:5173`

### Option 2: Docker Compose (Recommended)

```bash
# Create .env file at root
cp backend/.env.example .env

# Edit .env and add GEMINI_API_KEY

# Start all services
docker-compose up

# Build from scratch
docker-compose up --build
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000` or `http://localhost:5173`

## 📚 API Endpoints

### Health & Tasks
```
GET  /api/health              - Health check
GET  /api/tasks               - List available tasks
```

### Environment Control
```
POST /api/reset               - Reset environment & generate case
GET  /api/state               - Get current state
POST /api/step                - Take action
```

### AI Agent
```
POST /api/agent/decide        - Get AI agent decision
```

### Episodes
```
GET  /api/episode/summary     - Get episode summary & score
```

## 🎮 Game Flow

1. **Task Selection** → Choose difficulty level (easy to expert)
2. **Patient Presentation** → View vitals, symptoms, history
3. **Clinical Actions** → Request history, order labs, diagnose, recommend treatment
4. **Real-Time Scoring** → Get feedback on accuracy, safety, efficiency
5. **AI Agent** → Optional: Let AI agent decide the next step
6. **Episode Summary** → Final score, XP, achievements, grade (A-F)

## 📋 Medical Cases

### 1. Viral Upper Respiratory Infection (Easy)
- **Difficulty**: Easy
- **Time**: 5-7 minutes
- **Focus**: Basic symptom recognition, appropriate treatment

### 2. Type 2 Diabetes Management (Medium)
- **Difficulty**: Medium
- **Time**: 8-10 minutes
- **Focus**: Chronic disease management, lab interpretation

### 3. Sepsis Triage & Treatment (Hard)
- **Difficulty**: Hard
- **Time**: 10-12 minutes
- **Focus**: Time-critical diagnosis, rapid intervention
- **Challenge**: Patient deteriorates if not treated quickly

### 4. Drug Interaction Management (Hard)
- **Difficulty**: Hard
- **Time**: 8-10 minutes
- **Focus**: Medication safety, interaction recognition

### 5. Rare Disease Diagnosis (Expert)
- **Difficulty**: Expert
- **Time**: 12-15 minutes
- **Focus**: Differential diagnosis, pattern recognition
- **Challenge**: Uncommon presentation of rhabdomyolysis

## 🤖 AI Agent Integration

The AI agent uses **Google Gemini 1.5 Flash** to provide intelligent clinical decisions:

```python
from app.ai.gemini_agent import GeminiAgent

# Initialize
agent = GeminiAgent(api_key="your_api_key")

# Get decision
decision = agent.decide_action(observation, context)
```

### Agent Features
- Analyzes patient data (vitals, history, labs)
- Provides clinical reasoning
- Suggests next diagnostic or treatment actions
- Confidence scoring

## 🏆 Scoring System

### Reward Calculation
```
Total Reward = (0.4 × Accuracy) + (0.4 × Safety) + (0.2 × Efficiency) - Penalty

Accuracy (0-1)     : Correctness of diagnosis/treatment
Safety (0-1)       : Appropriate clinical decisions
Efficiency (0-1)   : Number of steps taken
Penalty (0-1)      : Wrong or harmful actions
```

### Grades
| Grade | Reward Range | Result |
|-------|--------------|--------|
| A     | 4.5-5.0      | Perfect diagnosis |
| B     | 3.5-4.4      | Good work |
| C     | 2.5-3.4      | Satisfactory |
| D     | 1.5-2.4      | Needs improvement |
| F     | 0-1.4        | Critical errors |

## 🎖️ Achievements

Unlock achievements based on performance:
- 🏆 **Perfect Diagnosis** - Grade A case
- 🛡️ **Safe Doctor** - Safety score > 95%
- ⚡ **Fast Thinker** - Efficiency score > 80%
- 🚀 **Quick Solver** - Complete in ≤ 3 steps
- 💔 **Life Saver** - Grade A/B on sepsis case
- 🔍 **Medical Sleuth** - Grade A/B on rare disease case

## 🛠️ Configuration

### Environment Variables

#### Backend (.env)
```env
# Server
HOST=0.0.0.0
PORT=8000

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Gemini API
GEMINI_API_KEY=your_api_key_here

# Environment
ENVIRONMENT=development
```

#### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

## 📦 Dependencies

### Backend
```
fastapi==0.104.1          # Web framework
uvicorn==0.24.0           # ASGI server
pydantic==2.5.0           # Data validation
google-generativeai==0.3.0 # Gemini API
```

### Frontend
```
react==18.2.0             # UI library
recharts==2.10.3          # Charts
axios==1.6.2              # HTTP client
tailwindcss==3.4.1        # CSS framework
vite==5.0.8               # Build tool
```

## 🧪 Testing

### Backend Health Check
```bash
curl http://localhost:8000/api/health
```

### Frontend Development
```bash
cd frontend
npm run dev
```

## 🔐 Security

- CORS properly configured
- API rate limiting ready (add with RedisBackend)
- Input validation via Pydantic
- Environment variables for secrets

## 🚀 Deployment

### Docker Production Build
```bash
docker-compose -f docker-compose.yml up -d
```

### Manual Deployment
1. Backend: Deploy to cloud (Heroku, Render, AWS)
2. Frontend: Deploy to Vercel, Netlify, or CDN
3. Set environment variables on hosting platform

## 🎨 UI Components

### TaskSelector
Displays available medical cases with difficulty badges

### PatientCard
Shows patient info, vitals, symptoms, exam findings

### ActionPanel
Interface for selecting and executing clinical actions

### RewardChart
Real-time visualization of score and performance metrics

### EpisodeSummary
Final results with grade, breakdown, and achievements

## 📊 Backend Architecture

### ClinIQEnvironment Class
Implements OpenAI Gym-style interface:
```python
env = ClinIQEnvironment()
obs = env.reset(task="viral_uri")
result = env.step(action)
summary = env.get_summary()
```

### Grader System
Task-specific grading:
- ViralURIGrader
- Diabetes2Grader
- SepsisTriageGrader
- DrugInteractionGrader
- RareDiseaseGrader

### Case Generator
Randomized medical case generation with realistic data

## 🔄 Development Workflow

1. **Backend Development**
   ```bash
   cd backend
   source venv/bin/activate
   python -m uvicorn app.main:app --reload
   ```

2. **Frontend Development**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Test Integration**
   - Open http://localhost:5173
   - Select a case and interact

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.11+

# Check port 8000 is available
lsof -i :8000
```

### Frontend build fails
```bash
# Clear node modules
rm -rf node_modules
npm install

# Check Node version
node --version  # Should be 18+
```

### Gemini API errors
- Verify GEMINI_API_KEY is set
- Check API key is valid
- Ensure API is enabled in Google Cloud Console

## 📖 Documentation

### API Docs
Access Swagger UI at `http://localhost:8000/docs` when backend is running

### Model Schema
All Pydantic models in `backend/app/models/schemas.py`

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Gemini API Guide](https://ai.google.dev/)
- [OpenAI Gym Interface](https://gymnasium.farama.org/)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Medical case inspiration from clinical training programs
- UI/UX inspiration from modern medical dashboards
- AI integration via Google Gemini API

## 📞 Support

For issues, questions, or suggestions:
1. Check existing GitHub issues
2. Create a new issue with detailed information
3. Include steps to reproduce
4. Share your environment details

---

**Made with ❤️ for healthcare professionals and AI enthusiasts**

Happy learning! 🎓⚕️
#   m e t a - h a c k a t h o n  
 