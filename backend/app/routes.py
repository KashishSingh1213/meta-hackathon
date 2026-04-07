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

# Gemini agent
try:
    agent = GeminiAgent()
except Exception as e:
    agent = None
    print(f"Warning: Gemini agent not initialized: {e}")


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
    try:
        result = env.step(request.action)
        return result
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agent/decide")
async def get_agent_decision(request: AgentDecisionRequest) -> AgentDecisionResponse:
    """Get AI agent decision for current state."""
    if agent is None:
        raise HTTPException(
            status_code=503,
            detail="Gemini API not configured. Set GEMINI_API_KEY environment variable.",
        )
    
    try:
        decision = agent.decide_action(request.observation, request.context)
        return decision
    except Exception as e:
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
