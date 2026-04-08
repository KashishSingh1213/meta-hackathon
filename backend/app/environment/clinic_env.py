"""ClinIQ simulation environment."""

import datetime
import random
from typing import Dict, List, Any, Optional
from app.models.schemas import (
    Observation,
    Action,
    StepResult,
    RewardBreakdown,
    EpisodeSummary,
)
from app.environment.case_generator import CaseGenerator
from app.graders.task_graders import GraderFactory


class ClinIQEnvironment:
    """OpenAI Gym-style environment for clinical simulation."""
    
    def __init__(self):
        self.current_observation: Optional[Observation] = None
        self.current_task: str = "viral_uri"
        self.case_id: str = ""
        self.step_count: int = 0
        self.total_reward: float = 0.0
        self.reward_history: List[RewardBreakdown] = []
        self.action_history: List[Action] = []
        self.start_time: datetime.datetime = datetime.datetime.now()
        self.episode_done: bool = False
        self.grader = None
        self.max_steps = 10
        
    def reset(self, task: str = "viral_uri", seed: Optional[int] = None) -> Observation:
        """Reset environment and generate new case."""
        if seed is not None:
            random.seed(seed)
        
        self.current_task = task
        self.step_count = 0
        self.total_reward = 0.0
        self.reward_history = []
        self.action_history = []
        self.start_time = datetime.datetime.now()
        self.episode_done = False
        
        # Generate case
        self.current_observation = CaseGenerator.generate_case(task)
        self.case_id = self.current_observation.case_id
        
        # Get grader
        self.grader = GraderFactory.get_grader(task)
        
        return self.current_observation
    
    def step(self, action: Action) -> StepResult:
        """Take a step in the environment."""
        if self.current_observation is None:
            raise RuntimeError("Environment not reset. Call reset() first.")
        
        if self.episode_done:
            raise RuntimeError("Episode is done. Call reset() to start new episode.")
        
        self.step_count += 1
        self.action_history.append(action)
        
        # Grade action
        reward_breakdown = self.grader.grade_action(
            self.current_observation,
            action,
            self.step_count
        )
        
        self.reward_history.append(reward_breakdown)
        
        # Calculate reward
        accuracy_weight = 0.4
        safety_weight = 0.4
        efficiency_weight = 0.2
        
        reward = (
            accuracy_weight * reward_breakdown.accuracy +
            safety_weight * reward_breakdown.safety +
            efficiency_weight * reward_breakdown.efficiency -
            reward_breakdown.penalty
        )
        
        self.total_reward += reward
        
        # Determine if done
        done = self.step_count >= self.max_steps or self._is_case_solved(action)
        if done:
            self.episode_done = True
        
        info = {
            "step": self.step_count,
            "action_type": action.action_type,
            "diagnostic_hint": self._get_diagnostic_hint(),
        }
        
        # Create new observation with updated context
        updated_observation = self._update_observation(action)
        
        return StepResult(
            observation=updated_observation,
            reward=reward,
            done=done,
            info=info,
            reward_breakdown=reward_breakdown,
        )
    
    def _update_observation(self, action: Action) -> Observation:
        """Update observation based on action."""
        # Create a copy to avoid mutating the original
        obs = self.current_observation.copy(deep=True)
        
        if action.action_type == "order_labs":
            # Simulate lab results
            if obs.lab_results is None:
                obs.lab_results = {}
            obs.lab_results.update(self._generate_lab_results(action))
        
        elif action.action_type == "request_history":
            # Expand medical history
            obs.patient_info.medical_history.extend(
                self._generate_additional_history()
            )
        
        return obs
    
    def _is_case_solved(self, action: Action) -> bool:
        """Check if case is correctly diagnosed and treated."""
        if action.action_type != "recommend_treatment":
            return False
        
        diagnosis = action.details.get("diagnosis", "")
        correct_diagnosis = self.grader.get_correct_diagnosis()
        
        # Allow for some variation in wording
        return correct_diagnosis.lower() in diagnosis.lower() or \
               diagnosis.lower() in correct_diagnosis.lower()
    
    def _get_diagnostic_hint(self) -> str:
        """Provide subtle diagnostic hints."""
        hints = {
            "viral_uri": "Consider the patient's symptom pattern and vital signs.",
            "type2_diabetes": "Review the lab values, especially glucose and HbA1c.",
            "sepsis_triage": "Act quickly - these vital signs are concerning.",
            "drug_interaction": "Check for medication interactions carefully.",
            "rare_disease_hunt": "Look at the muscle enzyme levels.",
        }
        return hints.get(self.current_task, "")
    
    def _generate_lab_results(self, action: Action) -> Dict[str, Any]:
        """Generate lab results based on action."""
        labs_requested = action.details.get("labs", [])
        results = {}
        
        # Map common lab requests to results
        for lab in labs_requested:
            lab_lower = lab.lower()
            if "blood culture" in lab_lower:
                results["blood_culture"] = "Pending"
            elif "cbc" in lab_lower or "white blood cell" in lab_lower:
                results["wbc"] = f"{12 + random.randint(-2, 8)}"
            elif "lactate" in lab_lower:
                results["lactate"] = f"{2.5 + random.uniform(0, 1.0):.1f}"
            elif "glucose" in lab_lower:
                results["glucose"] = f"{180 + random.randint(-30, 30)}"
            elif "ck" in lab_lower:
                results["ck"] = f"{2000 + random.randint(-500, 2000)}"
        
        return results
    
    def _generate_additional_history(self) -> List[str]:
        """Generate additional history details."""
        return ["Detailed exposure history provided", "Family history reviewed"]
    
    def get_state(self) -> Dict[str, Any]:
        """Get current state."""
        if self.current_observation is None:
            return {}
        
        return {
            "observation": self.current_observation.dict(),
            "step": self.step_count,
            "total_reward": self.total_reward,
            "episode_done": self.episode_done,
        }
    
    def get_summary(self) -> EpisodeSummary:
        """Get episode summary."""
        if not self.episode_done:
            raise RuntimeError("Episode not done yet.")
        
        # Calculate grade based on total reward
        if self.total_reward >= 4.5:
            grade = "A"
        elif self.total_reward >= 3.5:
            grade = "B"
        elif self.total_reward >= 2.5:
            grade = "C"
        elif self.total_reward >= 1.5:
            grade = "D"
        else:
            grade = "F"
        
        # Calculate average breakdown
        avg_accuracy = sum(r.accuracy for r in self.reward_history) / len(self.reward_history) if self.reward_history else 0
        avg_safety = sum(r.safety for r in self.reward_history) / len(self.reward_history) if self.reward_history else 0
        avg_efficiency = sum(r.efficiency for r in self.reward_history) / len(self.reward_history) if self.reward_history else 0
        avg_penalty = sum(r.penalty for r in self.reward_history) / len(self.reward_history) if self.reward_history else 0
        
        overall_breakdown = RewardBreakdown(
            accuracy=avg_accuracy,
            safety=avg_safety,
            efficiency=avg_efficiency,
            penalty=avg_penalty,
        )
        
        # Calculate XP
        xp_earned = int((self.total_reward / 5.0) * 100)
        xp_earned = max(0, min(xp_earned, 500))
        
        # Determine achievements
        achievements = self._get_achievements(grade, overall_breakdown)
        
        duration = (datetime.datetime.now() - self.start_time).total_seconds()
        
        return EpisodeSummary(
            case_id=self.case_id,
            task_name=self.current_task,
            total_reward=self.total_reward,
            reward_breakdown=overall_breakdown,
            grade=grade,
            actions_taken=self.action_history,
            step_count=self.step_count,
            duration_seconds=duration,
            xp_earned=xp_earned,
            achievements_unlocked=achievements,
        )
    
    def _get_achievements(self, grade: str, breakdown: RewardBreakdown) -> List[str]:
        """Determine achievements unlocked."""
        achievements = []
        
        if grade == "A":
            achievements.append("Perfect Diagnosis")
        
        if breakdown.safety > 0.95:
            achievements.append("Safe Doctor")
        
        if breakdown.efficiency > 0.8:
            achievements.append("Fast Thinker")
        
        if self.step_count <= 3:
            achievements.append("Quick Solver")
        
        if self.current_task == "sepsis_triage" and grade in ["A", "B"]:
            achievements.append("Life Saver")
        
        if self.current_task == "rare_disease_hunt" and grade in ["A", "B"]:
            achievements.append("Medical Sleuth")
        
        return achievements
