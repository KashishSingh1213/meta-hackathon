"""Pydantic models for ClinIQ platform."""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class Vitals(BaseModel):
    """Patient vital signs."""
    heart_rate: int = Field(..., description="Heart rate in bpm")
    blood_pressure: str = Field(..., description="Blood pressure (e.g., '120/80')")
    temperature: float = Field(..., description="Temperature in Celsius")
    respiratory_rate: int = Field(..., description="Respiratory rate in breaths/min")
    oxygen_saturation: float = Field(..., description="O2 saturation percentage")


class PatientInfo(BaseModel):
    """Patient demographic and clinical information."""
    name: str
    age: int
    gender: str
    presenting_complaint: str
    medical_history: List[str]
    current_medications: List[str]
    allergies: List[str]


class Observation(BaseModel):
    """Observation returned from environment."""
    patient_info: PatientInfo
    vitals: Vitals
    symptoms: List[str]
    physical_exam_findings: Dict[str, str]
    lab_results: Optional[Dict[str, Any]] = None
    imaging_results: Optional[Dict[str, str]] = None
    case_id: str
    episode_number: int
    task_name: str


class Action(BaseModel):
    """Action taken by user/agent."""
    action_type: str = Field(..., description="Type: request_history, order_labs, diagnose, recommend_treatment")
    details: Dict[str, Any] = Field(default_factory=dict)
    reasoning: Optional[str] = None


class RewardBreakdown(BaseModel):
    """Detailed reward breakdown."""
    accuracy: float = Field(..., ge=0, le=1)
    safety: float = Field(..., ge=0, le=1)
    efficiency: float = Field(..., ge=0, le=1)
    penalty: float = Field(default=0, ge=0)


class StepResult(BaseModel):
    """Result of a step in the environment."""
    observation: Observation
    reward: float
    done: bool
    info: Dict[str, Any]
    reward_breakdown: RewardBreakdown


class ResetRequest(BaseModel):
    """Request to reset the environment."""
    task: str = Field(default="viral_uri", description="Task type")
    seed: Optional[int] = None


class ActionRequest(BaseModel):
    """Request to take an action in the environment."""
    action: Action


class TaskInfo(BaseModel):
    """Information about a task."""
    name: str
    title: str
    description: str
    difficulty: str
    estimated_time: str
    learning_objectives: List[str]


class AgentDecisionRequest(BaseModel):
    """Request to get AI agent decision."""
    observation: Observation
    context: Optional[str] = None


class AgentDecisionResponse(BaseModel):
    """Response from AI agent decision."""
    action: Action
    reasoning: str
    confidence: float


class EpisodeSummary(BaseModel):
    """Summary of a completed episode."""
    case_id: str
    task_name: str
    total_reward: float
    reward_breakdown: RewardBreakdown
    grade: str  # A, B, C, D, F
    actions_taken: List[Action]
    step_count: int
    duration_seconds: float
    xp_earned: int
    achievements_unlocked: List[str]
