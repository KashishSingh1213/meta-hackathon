"""Graders for evaluating actions in each task."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
from app.models.schemas import Action, Observation, RewardBreakdown


class TaskGrader(ABC):
    """Base class for task graders."""
    
    @abstractmethod
    def grade_action(self, observation: Observation, action: Action, step_number: int) -> RewardBreakdown:
        """Grade an action and return reward breakdown."""
        pass
    
    @abstractmethod
    def get_correct_diagnosis(self) -> str:
        """Get the correct diagnosis for this case."""
        pass


class ViralURIGrader(TaskGrader):
    """Grader for viral URI task."""
    
    CORRECT_DIAGNOSIS = "Viral Upper Respiratory Infection"
    
    def grade_action(self, observation: Observation, action: Action, step_number: int) -> RewardBreakdown:
        accuracy = 0.0
        safety = 1.0
        efficiency = 1.0 - (min(step_number, 5) / 5) * 0.2
        penalty = 0.0
        
        if action.action_type == "request_history":
            accuracy += 0.1
        elif action.action_type == "order_labs":
            # Unnecessary labs for URI
            accuracy += 0.05
        elif action.action_type == "diagnose":
            diagnosis = action.details.get("diagnosis", "")
            if self.CORRECT_DIAGNOSIS.lower() in diagnosis.lower():
                accuracy = 0.9
        elif action.action_type == "recommend_treatment":
            treatment = action.details.get("treatment", "")
            # Good if recommending supportive care
            if any(x in treatment.lower() for x in ["rest", "fluids", "zinc", "supportive"]):
                accuracy += 0.1
            # Penalty if recommending antibiotics
            if "antibiotic" in treatment.lower():
                penalty += 0.15
        
        return RewardBreakdown(
            accuracy=min(accuracy, 1.0),
            safety=safety,
            efficiency=efficiency,
            penalty=penalty,
        )
    
    def get_correct_diagnosis(self) -> str:
        return self.CORRECT_DIAGNOSIS


class Diabetes2Grader(TaskGrader):
    """Grader for type 2 diabetes management task."""
    
    CORRECT_DIAGNOSIS = "Type 2 Diabetes Mellitus (uncontrolled)"
    
    def grade_action(self, observation: Observation, action: Action, step_number: int) -> RewardBreakdown:
        accuracy = 0.0
        safety = 1.0
        efficiency = 1.0 - (min(step_number, 6) / 6) * 0.25
        penalty = 0.0
        
        if action.action_type == "request_history":
            accuracy += 0.15
        elif action.action_type == "order_labs":
            labs_ordered = action.details.get("labs", [])
            good_labs = [x.lower() in ["hemoglobin a1c", "fasting glucose", "lipid panel", "urinalysis"] 
                        for x in labs_ordered]
            if any(good_labs):
                accuracy += 0.2
        elif action.action_type == "diagnose":
            diagnosis = action.details.get("diagnosis", "")
            if "diabetes" in diagnosis.lower():
                accuracy = 0.8
        elif action.action_type == "recommend_treatment":
            treatment = action.details.get("treatment", "")
            # Good if adjusting medications appropriately
            if "metformin" in treatment.lower() or "glp-1" in treatment.lower():
                accuracy += 0.2
            # Reward for mentioning lifestyle
            if "exercise" in treatment.lower() or "diet" in treatment.lower():
                accuracy += 0.15
            # Penalty for inappropriate treatment
            if "insulin" in treatment.lower() and "initiate" in treatment.lower():
                penalty += 0.1
        
        return RewardBreakdown(
            accuracy=min(accuracy, 1.0),
            safety=max(safety - penalty, 0.7),
            efficiency=efficiency,
            penalty=penalty,
        )
    
    def get_correct_diagnosis(self) -> str:
        return self.CORRECT_DIAGNOSIS


class SepsisTriageGrader(TaskGrader):
    """Grader for sepsis triage task."""
    
    CORRECT_DIAGNOSIS = "Sepsis (Presumed bacterial pneumonia)"
    
    def grade_action(self, observation: Observation, action: Action, step_number: int) -> RewardBreakdown:
        accuracy = 0.0
        safety = 1.0
        efficiency = 1.0 - (min(step_number, 4) / 4) * 0.3
        penalty = 0.0
        
        if action.action_type == "request_history":
            accuracy += 0.1
        elif action.action_type == "order_labs":
            labs_ordered = action.details.get("labs", [])
            # Must order blood cultures, lactate, CBC
            critical_labs = 0
            for lab in labs_ordered:
                if any(x in lab.lower() for x in ["blood culture", "lactate", "cbc", "procalcitonin"]):
                    critical_labs += 1
            accuracy += (critical_labs / 4) * 0.25
        elif action.action_type == "diagnose":
            diagnosis = action.details.get("diagnosis", "")
            if "sepsis" in diagnosis.lower() and "pneumonia" in diagnosis.lower():
                accuracy = 0.95
        elif action.action_type == "recommend_treatment":
            treatment = action.details.get("treatment", "")
            # Critical: early antibiotics
            if "antibiotic" in treatment.lower() and "broad" in treatment.lower():
                accuracy += 0.3
            # Good: IV fluids
            if "iv fluid" in treatment.lower() or "lactate" in treatment.lower():
                accuracy += 0.15
            # Penalty for delay
            if step_number > 3:
                penalty += 0.2
        
        return RewardBreakdown(
            accuracy=min(accuracy, 1.0),
            safety=max(safety - penalty, 0.5),
            efficiency=efficiency,
            penalty=penalty,
        )
    
    def get_correct_diagnosis(self) -> str:
        return self.CORRECT_DIAGNOSIS


class DrugInteractionGrader(TaskGrader):
    """Grader for drug interaction task."""
    
    CORRECT_DIAGNOSIS = "Drug Interaction (Warfarin + NSAID + Metronidazole)"
    
    def grade_action(self, observation: Observation, action: Action, step_number: int) -> RewardBreakdown:
        accuracy = 0.0
        safety = 1.0
        efficiency = 1.0 - (min(step_number, 5) / 5) * 0.25
        penalty = 0.0
        
        if action.action_type == "request_history":
            accuracy += 0.15
        elif action.action_type == "order_labs":
            labs = action.details.get("labs", [])
            if any("inr" in lab.lower() for lab in labs):
                accuracy += 0.2
        elif action.action_type == "diagnose":
            diagnosis = action.details.get("diagnosis", "")
            if "drug interaction" in diagnosis.lower() or "warfarin" in diagnosis.lower():
                accuracy = 0.92
        elif action.action_type == "recommend_treatment":
            treatment = action.details.get("treatment", "")
            # Critical: stop NSAID
            if "stop" in treatment.lower() and "ibuprofen" in treatment.lower():
                accuracy += 0.25
            # Good: adjust warfarin
            if "warfarin" in treatment.lower() and ("reduce" in treatment.lower() or "adjust" in treatment.lower()):
                accuracy += 0.2
            # Penalty if not addressing root cause
            if "continue warfarin" in treatment.lower() and "continue ibuprofen" in treatment.lower():
                penalty += 0.3
        
        return RewardBreakdown(
            accuracy=min(accuracy, 1.0),
            safety=max(safety - penalty, 0.6),
            efficiency=efficiency,
            penalty=penalty,
        )
    
    def get_correct_diagnosis(self) -> str:
        return self.CORRECT_DIAGNOSIS


class RareDiseaseGrader(TaskGrader):
    """Grader for rare disease case."""
    
    CORRECT_DIAGNOSIS = "Rhabdomyolysis (exercise-induced or statin-related)"
    
    def grade_action(self, observation: Observation, action: Action, step_number: int) -> RewardBreakdown:
        accuracy = 0.0
        safety = 1.0
        efficiency = 1.0 - (min(step_number, 6) / 6) * 0.3
        penalty = 0.0
        
        if action.action_type == "request_history":
            accuracy += 0.1
        elif action.action_type == "order_labs":
            labs = action.details.get("labs", [])
            important_labs = 0
            for lab in labs:
                if any(x in lab.lower() for x in ["ck", "myoglobin", "urine", "creatinine", "potassium"]):
                    important_labs += 1
            accuracy += (important_labs / 5) * 0.3
        elif action.action_type == "diagnose":
            diagnosis = action.details.get("diagnosis", "")
            if "rhabdomyolysis" in diagnosis.lower():
                accuracy = 0.95
            elif "myositis" in diagnosis.lower() or "muscle" in diagnosis.lower():
                accuracy = 0.7
        elif action.action_type == "recommend_treatment":
            treatment = action.details.get("treatment", "")
            # Critical: aggressive IV hydration
            if "iv" in treatment.lower() and ("hydration" in treatment.lower() or "fluids" in treatment.lower()):
                accuracy += 0.25
            # Good: urine alkalinization
            if "alkalin" in treatment.lower():
                accuracy += 0.15
            # Penalty for missing critical treatment
            if "stop statin" in treatment.lower():
                accuracy += 0.1
        
        return RewardBreakdown(
            accuracy=min(accuracy, 1.0),
            safety=max(safety - penalty, 0.6),
            efficiency=efficiency,
            penalty=penalty,
        )
    
    def get_correct_diagnosis(self) -> str:
        return self.CORRECT_DIAGNOSIS


class GraderFactory:
    """Factory for creating task graders."""
    
    GRADERS = {
        "viral_uri": ViralURIGrader(),
        "type2_diabetes": Diabetes2Grader(),
        "sepsis_triage": SepsisTriageGrader(),
        "drug_interaction": DrugInteractionGrader(),
        "rare_disease_hunt": RareDiseaseGrader(),
    }
    
    @staticmethod
    def get_grader(task: str) -> TaskGrader:
        """Get grader for task."""
        if task not in GraderFactory.GRADERS:
            raise ValueError(f"Unknown task: {task}")
        return GraderFactory.GRADERS[task]
