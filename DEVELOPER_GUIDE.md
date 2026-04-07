# 🔧 Developer Guide

For extending and customizing ClinIQ.

## Architecture Overview

```
┌─────────────────────────┐
│    React Frontend       │
│  (Vite + Tailwind)      │
└──────────┬──────────────┘
           │ HTTP/REST
           ↓
┌─────────────────────────┐
│   FastAPI Backend       │
│  (Python + Pydantic)    │
└──────────┬──────────────┘
           │
      ┌────┴─────┐
      ↓          ↓
   Cases      Gemini AI
  Generator    (API)
```

## Backend Architecture

### Core Files

**`app/main.py`**
- FastAPI application setup
- CORS middleware
- Route registration

**`app/routes.py`**
- API endpoints
- Request/response handling
- Global environment instance

**`app/models/schemas.py`**
- Pydantic data models
- Type validation
- API contracts

### Game Environment

**`app/environment/clinic_env.py`**
```python
class ClinIQEnvironment:
    def reset(task: str) -> Observation      # Start episode
    def step(action: Action) -> StepResult   # Take action
    def get_state() -> dict                  # Current state
    def get_summary() -> EpisodeSummary      # Episode results
```

Implements OpenAI Gym interface for compatibility with RL libraries.

### Case Generation

**`app/environment/case_generator.py`**
```python
class CaseGenerator:
    @staticmethod
    def generate_viral_uri() -> Observation
    @staticmethod
    def generate_type2_diabetes() -> Observation
    # ... more cases ...
    @staticmethod
    def generate_case(task: str) -> Observation
```

Each case returns:
- Patient info (demographics, history)
- Vitals (HR, BP, temp, RR, O2)
- Symptoms & physical exam
- Initial lab results

### Scoring System

**`app/graders/task_graders.py`**
```python
class TaskGrader(ABC):
    def grade_action(observation, action, step_number) -> RewardBreakdown
    def get_correct_diagnosis() -> str

class ViralURIGrader(TaskGrader):
    # Scores diagnosis & treatment for URI

class Diabetes2Grader(TaskGrader):
    # Scores diabetes management
```

### AI Integration

**`app/ai/gemini_agent.py`**
```python
class GeminiAgent:
    def decide_action(observation, context) -> AgentDecisionResponse
```

Uses Google Gemini 1.5 Flash to:
1. Analyze patient data
2. Generate clinical reasoning
3. Suggest next action
4. Provide confidence score

---

## Frontend Architecture

### State Management

Components use React hooks:
- `useEnvironment()` - Game state & API
- `useAgent()` - AI agent decisions
- `useLocalStorage()` - Persist XP/achievements

### Component Structure

```
App
├── TaskSelector
├── GamePlay
│   ├── PatientCard
│   ├── ActionPanel
│   └── RewardChart
└── EpisodeSummary
```

### API Client

**`src/api/client.js`**
```javascript
const api = axios.create({
  baseURL: 'http://localhost:8000'
})

cliniqAPI.reset(task)
cliniqAPI.getState()
cliniqAPI.step(action)
cliniqAPI.getAgentDecision(observation)
cliniqAPI.getSummary()
```

### Styling

- **Framework**: Tailwind CSS
- **Theme**: Dark mode with medical blue accents
- **Components**: Glassmorphism effects
- **Animations**: Smooth transitions

---

## Extending ClinIQ

### Add a New Medical Case

1. **Create case generator in `case_generator.py`**:

```python
@staticmethod
def generate_my_case() -> Observation:
    patient = PatientInfo(
        name="Patient Name",
        age=45,
        gender="M",
        presenting_complaint="...",
        medical_history=[],
        current_medications=[],
        allergies=[]
    )
    
    vitals = Vitals(
        heart_rate=75,
        blood_pressure="120/80",
        temperature=37.0,
        respiratory_rate=16,
        oxygen_saturation=98.0
    )
    
    return Observation(
        patient_info=patient,
        vitals=vitals,
        symptoms=[],
        physical_exam_findings={},
        lab_results=None,
        case_id="my_case_001",
        episode_number=1,
        task_name="my_task"
    )

# Add to TASKS dict
TASKS["my_task"] = {
    "title": "My Medical Case",
    "description": "...",
    "difficulty": "medium",
}

# Register generator
generators["my_task"] = CaseGenerator.generate_my_case
```

2. **Create grader in `graders/task_graders.py`**:

```python
class MyTaskGrader(TaskGrader):
    CORRECT_DIAGNOSIS = "Correct diagnosis text"
    
    def grade_action(self, observation, action, step_number):
        accuracy = 0.0
        safety = 1.0
        efficiency = 1.0 - (step_number / 5) * 0.2
        penalty = 0.0
        
        # Score based on action
        if action.action_type == "diagnose":
            if self.CORRECT_DIAGNOSIS in action.details.get("diagnosis", ""):
                accuracy = 1.0
        
        return RewardBreakdown(
            accuracy=accuracy,
            safety=safety,
            efficiency=efficiency,
            penalty=penalty
        )
    
    def get_correct_diagnosis(self):
        return self.CORRECT_DIAGNOSIS

# Register in GraderFactory
GraderFactory.GRADERS["my_task"] = MyTaskGrader()
```

3. **Update case generator to include new case**:

```python
generators = {
    # ... existing cases ...
    "my_task": CaseGenerator.generate_my_case,
}
```

### Add Custom Action Types

1. **Add to action handler in `clinic_env.py`**:

```python
def _update_observation(self, action):
    obs = self.current_observation
    
    if action.action_type == "my_custom_action":
        # Handle custom action
        obs.custom_field = "value"
    
    return obs
```

2. **Add UI component for action in `ActionPanel.jsx`**:

```javascript
const ACTION_TEMPLATES = {
  my_custom_action: {
    label: 'My Custom Action',
    icon: '🎯',
    details: {},
  },
  // ...
}
```

### Add New Achievements

In `clinic_env.py`:

```python
def _get_achievements(self, grade, breakdown):
    achievements = []
    
    # ... existing achievements ...
    
    if your_condition:
        achievements.append("Your New Achievement")
    
    return achievements
```

Display in `EpisodeSummary.jsx`:

```javascript
{summary.achievements_unlocked.map(achievement => (
  <div key={achievement} className="badge">
    {achievement}
  </div>
))}
```

---

## API Endpoints Reference

### Health

```
GET /api/health
Response: { status, service, version }
```

### Tasks

```
GET /api/tasks
Response: [ { name, title, description, difficulty, ... } ]
```

### Environment

```
POST /api/reset
Body: { task, seed }
Response: Observation

GET /api/state
Response: { observation, step, total_reward, episode_done }

POST /api/step
Body: { action }
Response: StepResult

GET /api/episode/summary
Response: EpisodeSummary
```

### AI Agent

```
POST /api/agent/decide
Body: { observation, context }
Response: AgentDecisionResponse
```

---

## Testing Tips

### Test Backend Locally

```bash
# Run tests (create tests/ folder)
pytest tests/

# Check API docs
http://localhost:8000/docs

# Manual API test
curl -X POST http://localhost:8000/api/reset \
  -H "Content-Type: application/json" \
  -d '{"task": "viral_uri"}'
```

### Test Frontend

```bash
# Debug React components
# Install React DevTools browser extension
# Use browser dev tools (F12)

# Check console for errors
# Check Network tab for API calls
```

---

## Performance Optimization

### Backend
- Add caching for case generation
- Use AsyncIO for AI calls
- Implement batch processing
- Add database for persistence

### Frontend
- Lazy load components
- Memoize expensive operations
- Optimize images
- Implement virtual scrolling

---

## Deployment Checklist

- [ ] Environment configured
- [ ] Gemini API key set
- [ ] CORS properly configured
- [ ] Database setup (if adding)
- [ ] Error handling tested
- [ ] Performance baseline
- [ ] Security audit
- [ ] Documentation updated

---

## Useful Commands

```bash
# Backend
python -m uvicorn app.main:app --reload
python -m uvicorn app.main:app --port 8001
python run.py

# Frontend
npm run dev
npm run build
npm run preview

# Docker
docker-compose up
docker-compose down
docker-compose logs -f

# Python
pip list
pip install package_name
python -m pip install --upgrade pip
```

---

## Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [React Docs](https://react.dev/)
- [Tailwind Docs](https://tailwindcss.com/)
- [Gemini API Docs](https://ai.google.dev/docs)

---

## Need Help?

Check:
1. Backend logs in terminal
2. Browser console (F12)
3. Network requests in DevTools
4. API docs at `/docs`

Good luck! 🚀
