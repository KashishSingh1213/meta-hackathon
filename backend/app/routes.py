"""FastAPI routes for ClinIQ backend."""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, List, Any, Optional
from app.models.schemas import (
    ResetRequest,
    ActionRequest,
    Observation,
    StepResult,
    TaskInfo,
    AgentDecisionRequest,
    AgentDecisionResponse,
    EpisodeSummary,
)
from app.environment.clinic_env import ClinIQEnvironment
from app.environment.case_generator import CaseGenerator
from app.ai.gemini_agent import GeminiAgent

router = APIRouter(prefix="/api", tags=["clinic"])

# Global environment instance
env = ClinIQEnvironment()

# Gemini agent - always initialize, uses smart fallback if API unavailable
try:
    print("\n" + "="*60)
    print("🚀 INITIALIZING GEMINI AGENT AT STARTUP")
    print("="*60)
    agent = GeminiAgent()
    print(f"✅ Gemini Agent initialized")
    print(f"   - Fallback mode: {agent.fallback_mode}")
    print(f"   - Model: {agent.model}")
    print(f"   - API Key loaded: {bool(agent.api_key)}")
    print("="*60 + "\n")
except Exception as e:
    agent = None
    print(f"❌ CRITICAL: Gemini agent failed to initialize: {e}")
    import traceback
    traceback.print_exc()


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "ClinIQ",
        "version": "1.0.0",
    }


@router.get("/tasks")
async def get_tasks() -> List[TaskInfo]:
    """Get available tasks."""
    tasks = []
    for task_name, task_info in CaseGenerator.TASKS.items():
        tasks.append(TaskInfo(
            name=task_name,
            title=task_info["title"],
            description=task_info["description"],
            difficulty=task_info["difficulty"],
            estimated_time="5-10 minutes",
            learning_objectives=[
                "Clinical decision-making",
                "Diagnostic reasoning",
                "Patient safety",
            ],
        ))
    return tasks


@router.post("/reset")
async def reset_environment(request: ResetRequest) -> Observation:
    """Reset environment and generate new patient case."""
    try:
        observation = env.reset(task=request.task, seed=request.seed)
        return observation
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/state")
async def get_state() -> Dict[str, Any]:
    """Get current environment state."""
    try:
        return env.get_state()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/step")
async def step_environment(request: ActionRequest) -> StepResult:
    """Take a step in the environment."""
    print("\n" + "="*60)
    print("📝 STEP ENDPOINT CALLED")
    print("="*60)
    
    try:
        # Log the incoming request
        print(f"📥 Request type: {type(request)}")
        print(f"📥 Action type: {request.action.action_type}")
        print(f"📥 Action details: {request.action.details}")
        
        # Check environment state
        if env is None:
            raise RuntimeError("Environment not initialized")
        
        # AUTO-INITIALIZE: If environment not reset, reset with default task
        if env.current_observation is None:
            print("⚠️  Environment not reset. Auto-initializing with default task...")
            env.reset(task="viral_uri")
            print("✅ Environment auto-initialized")
        
        # AUTO-RESET: If episode is done, reset for new episode
        if env.episode_done:
            print("⚠️  Episode already done. Auto-resetting for new episode...")
            env.reset(task="viral_uri")
            print("✅ Episode reset for new game")
        
        print(f"✅ Environment state: obs={env.current_observation is not None}, done={env.episode_done}, step={env.step_count}")
        
        # Call step
        print(f"🔄 Calling env.step()...")
        result = env.step(request.action)
        
        print(f"✅ Step completed successfully!")
        print(f"✅ Reward: {result.reward}, Done: {result.done}, New step count: {env.step_count}")
        print("="*60 + "\n")
        
        return result
        
    except RuntimeError as e:
        print(f"⚠️  Runtime error in step: {e}")
        print("="*60 + "\n")
        raise HTTPException(status_code=400, detail=str(e))
        
    except ValueError as e:
        print(f"⚠️  Value error in step: {e}")
        print("="*60 + "\n")
        raise HTTPException(status_code=400, detail=str(e))
        
    except Exception as e:
        print(f"❌ Unexpected error in step: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        print("="*60 + "\n")
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {str(e)}")


@router.post("/agent/decide")
async def get_agent_decision(request: AgentDecisionRequest) -> AgentDecisionResponse:
    """Get AI agent decision for current state."""
    if agent is None:
        raise HTTPException(
            status_code=503,
            detail="AI Agent not available. Set GEMINI_API_KEY environment variable.",
        )
    
    try:
        decision = agent.decide_action(request.observation, request.context)
        return decision
    except Exception as e:
        print(f"❌ Agent decision error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")


@router.get("/episode/summary")
async def get_episode_summary() -> EpisodeSummary:
    """Get summary of completed episode."""
    try:
        if not env.episode_done:
            raise HTTPException(status_code=400, detail="Episode not completed yet.")
        return env.get_summary()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset/{task}")
async def reset_with_task(task: str) -> Observation:
    """Reset environment with specific task."""
    try:
        request = ResetRequest(task=task)
        return await reset_environment(request)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
