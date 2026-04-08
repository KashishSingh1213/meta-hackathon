#!/usr/bin/env python3
"""
OpenEnv RL Challenge Inference Script
ClinIQ - Clinical Intelligence Query Environment
"""

import os
import sys
import json
import requests
from typing import Optional
from openai import OpenAI

# Read environment variables with defaults where required
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

# Initialize OpenAI client
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

# Backend API base for ClinIQ environment
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api")


class ClinIQInference:
    """Inference runner for ClinIQ environment."""
    
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.task_name = None
        self.env_name = "cliniq"
        self.model_name = MODEL_NAME
        self.steps = []
        self.rewards = []
        self.success = False
        self.current_observation = None
        self.episode_done = False
        
    def start_episode(self, task: str = "viral_uri") -> bool:
        """Initialize a new episode."""
        try:
            self.task_name = task
            response = requests.post(
                f"{self.backend_url}/reset",
                json={"task": task, "seed": None},
                timeout=10
            )
            response.raise_for_status()
            self.current_observation = response.json()
            self.steps = []
            self.rewards = []
            self.episode_done = False
            
            # Print START line
            print(f"[START] task={task} env={self.env_name} model={self.model_name}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to start episode: {e}", file=sys.stderr)
            return False
    
    def get_ai_decision(self, context: Optional[str] = None) -> Optional[dict]:
        """Get AI agent decision using LLM."""
        try:
            # Send observation to backend AI agent
            request_data = {
                "observation": self.current_observation,
                "context": context or "Determine next clinical action based on patient state."
            }
            
            response = requests.post(
                f"{self.backend_url}/agent/decide",
                json=request_data,
                timeout=30
            )
            response.raise_for_status()
            decision = response.json()
            return decision
        except Exception as e:
            print(f"[ERROR] Failed to get AI decision: {e}", file=sys.stderr)
            return None
    
    def format_step_log(self, step_num: int, action_str: str, reward: float, 
                       done: bool, error: Optional[str] = None) -> str:
        """Format step output according to specification."""
        error_str = f'"{error}"' if error else "null"
        return (
            f"[STEP] step={step_num} action={action_str} "
            f"reward={reward:.2f} done={'true' if done else 'false'} error={error_str}"
        )
    
    def run_step(self, action: dict) -> bool:
        """Execute one step in the environment."""
        try:
            # Execute action in environment
            response = requests.post(
                f"{self.backend_url}/step",
                json={"action": action},
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            
            # Extract step information
            reward = result.get("reward", 0.0)
            done = result.get("done", False)
            error = result.get("error", None)
            
            # Update state
            self.current_observation = result.get("observation")
            self.episode_done = done
            self.rewards.append(reward)
            
            # Format action string for logging
            action_type = action.get("action_type", "unknown")
            details = action.get("details", {})
            action_str = f"{action_type}({json.dumps(details)})"
            
            # Print STEP line
            step_num = len(self.steps) + 1
            print(self.format_step_log(step_num, action_str, reward, done, error))
            
            self.steps.append({
                "action": action_str,
                "reward": reward,
                "done": done,
                "error": error
            })
            
            return not done
        except Exception as e:
            print(f"[ERROR] Step execution failed: {e}", file=sys.stderr)
            return False
    
    def run_episode(self, task: str = "viral_uri", max_steps: int = 10) -> bool:
        """Run a complete episode."""
        try:
            # Start episode
            if not self.start_episode(task):
                return False
            
            # Run steps until done or max_steps reached
            step_count = 0
            while step_count < max_steps and not self.episode_done:
                # Get AI decision
                decision = self.get_ai_decision()
                if not decision:
                    print(f"[ERROR] Failed to get AI decision at step {step_count + 1}", 
                          file=sys.stderr)
                    break
                
                # Execute action
                action = decision.get("action", {})
                if not self.run_step(action):
                    break
                
                step_count += 1
            
            self.success = self.episode_done
            
            # Print END line
            rewards_str = ",".join(f"{r:.2f}" for r in self.rewards)
            print(f"[END] success={'true' if self.success else 'false'} "
                  f"steps={step_count} rewards={rewards_str}")
            
            return self.success
        except Exception as e:
            print(f"[ERROR] Episode execution failed: {e}", file=sys.stderr)
            # Still emit END line
            rewards_str = ",".join(f"{r:.2f}" for r in self.rewards)
            print(f"[END] success=false steps={len(self.steps)} rewards={rewards_str}")
            return False


def main():
    """Main entry point."""
    try:
        # Get task from environment or use default
        task = os.getenv("TASK", "viral_uri")
        max_steps = int(os.getenv("MAX_STEPS", "10"))
        
        # Run inference
        runner = ClinIQInference()
        success = runner.run_episode(task=task, max_steps=max_steps)
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"[FATAL] {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()
