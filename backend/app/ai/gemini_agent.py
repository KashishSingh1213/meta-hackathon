"""Gemini API integration for AI agent decision-making."""

import os
import json
from typing import Optional
import google.generativeai as genai
from app.models.schemas import Observation, Action, AgentDecisionResponse


class GeminiAgent:
    """AI agent using Google Gemini API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini agent."""
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
        
        self.api_key = api_key
        self.model = None
        self.fallback_mode = False
        
        print(f"🔍 API Key Check: {api_key[:10] if api_key else 'NONE'}...")
        print(f"🔍 API Key length: {len(api_key) if api_key else 0}")
        
        if not api_key:
            print("⚠️  GEMINI_API_KEY not set - using fallback mode")
            self.fallback_mode = True
            return
        
        try:
            print(f"🤖 Configuring genai with API key...")
            genai.configure(api_key=api_key)
            # Use gemini-1.5-flash (reliable and fast)
            print(f"🤖 Initializing Gemini model...")
            self.model = genai.GenerativeModel("gemini-1.5-flash")
            print(f"✅ Successfully initialized: gemini-1.5-flash")
            print(f"✅ Model object: {self.model}")
        except Exception as e:
            print(f"⚠️  Gemini API configuration failed: {type(e).__name__}: {e}")
            print(f"⚠️  Using fallback mode")
            self.fallback_mode = True
    
    def decide_action(self, observation: Observation, context: Optional[str] = None) -> AgentDecisionResponse:
        """Get AI agent decision for next action."""
        
        # If in fallback mode, return intelligent default based on patient state
        if self.fallback_mode:
            print("⚠️  IN FALLBACK MODE - API key or model not initialized")
            return self._get_intelligent_fallback(observation)
        
        # Build context for the model
        prompt = self._build_prompt(observation, context)
        
        try:
            print(f"🔄 Calling Gemini API with model: {self.model}")
            response = self.model.generate_content(prompt)
            print(f"✅ Got response from Gemini")
            
            # Parse response
            response_text = response.text
            
            # Extract JSON from response
            action_data = self._parse_response(response_text)
            
            action = Action(
                action_type=action_data.get("action_type", "request_history"),
                details=action_data.get("details", {}),
                reasoning=action_data.get("reasoning", ""),
            )
            
            print(f"✅ Successfully returned real AI decision: {action.action_type}")
            return AgentDecisionResponse(
                action=action,
                reasoning=action_data.get("reasoning", response_text),
                confidence=action_data.get("confidence", 0.7),
            )
        except Exception as e:
            # Fallback to safe action
            print(f"❌ GEMINI API CALL FAILED: {type(e).__name__}: {e}")
            print(f"❌ Switching to fallback mode")
            print(f"❌ Check: API key valid? Model initialized? {self.model}")
            return self._get_intelligent_fallback(observation)
    
    def _build_prompt(self, observation: Observation, context: Optional[str]) -> str:
        """Build prompt for Gemini."""
        prompt = f"""You are an expert clinical decision-making AI assistant. Analyze the following patient case and decide on the next clinical action.

PATIENT INFORMATION:
- Name: {observation.patient_info.name}
- Age: {observation.patient_info.age}
- Gender: {observation.patient_info.gender}
- Presenting Complaint: {observation.patient_info.presenting_complaint}
- Medical History: {', '.join(observation.patient_info.medical_history)}
- Current Medications: {', '.join(observation.patient_info.current_medications)}
- Allergies: {', '.join(observation.patient_info.allergies)}

CURRENT VITALS:
- Heart Rate: {observation.vitals.heart_rate} bpm
- Blood Pressure: {observation.vitals.blood_pressure}
- Temperature: {observation.vitals.temperature}°C
- Respiratory Rate: {observation.vitals.respiratory_rate}
- O2 Saturation: {observation.vitals.oxygen_saturation}%

SYMPTOMS:
{', '.join(observation.symptoms)}

PHYSICAL EXAMINATION:
{chr(10).join(f"- {k}: {v}" for k, v in observation.physical_exam_findings.items())}

LAB RESULTS:
{json.dumps(observation.lab_results, indent=2) if observation.lab_results else "None yet"}

IMAGING:
{json.dumps(observation.imaging_results, indent=2) if observation.imaging_results else "None yet"}

{"ADDITIONAL CONTEXT: " + context if context else ""}

TASK: Decide on the next clinical action. Respond ONLY with valid JSON (no markdown, no extra text) with this exact structure:

{{
  "action_type": "request_history|order_labs|diagnose|recommend_treatment",
  "details": {{
    "labs": ["lab1", "lab2"] (for order_labs),
    "diagnosis": "diagnosis text" (for diagnose),
    "treatment": "treatment plan" (for recommend_treatment)
  }},
  "reasoning": "brief explanation",
  "confidence": 0.0-1.0
}}

Prioritize life-threatening conditions. Be thorough but efficient."""
        
        return prompt
    
    def _parse_response(self, response_text: str) -> dict:
        """Parse JSON response from model."""
        try:
            # Try direct JSON parsing
            data = json.loads(response_text)
            return data
        except json.JSONDecodeError:
            # Try to extract JSON from text
            import re
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response_text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(0))
                except:
                    pass
            
            # Fallback
            return {
                "action_type": "request_history",
                "details": {},
                "reasoning": response_text,
                "confidence": 0.5,
            }
    
    def _get_intelligent_fallback(self, observation: Observation) -> AgentDecisionResponse:
        """Get intelligent fallback action based on patient state (no API call)."""
        # Safe clinical reasoning without API
        hr = observation.vitals.heart_rate
        bp = observation.vitals.blood_pressure
        temp = observation.vitals.temperature
        o2 = observation.vitals.oxygen_saturation
        
        # Check for concerning vital signs
        is_critical = (hr > 120 or hr < 60 or temp > 39 or o2 < 90)
        
        reasoning = ""
        if is_critical:
            reasoning = "Vital signs concerning - ordering urgent labs to rule out serious conditions"
            labs = ["Blood culture", "CBC", "CMP", "Lactate", "Troponin"]
            action_type = "order_labs"
            details = {"labs": labs}
        else:
            reasoning = "Stable vitals - gathering more clinical information"
            action_type = "request_history"
            details = {}
        
        return AgentDecisionResponse(
            action=Action(
                action_type=action_type,
                details=details,
                reasoning=reasoning,
            ),
            reasoning=f"[Fallback AI] {reasoning}",
            confidence=0.6,
        )
    
    def _get_fallback_action(self, error: str) -> AgentDecisionResponse:
        """Get fallback action on error."""
        return AgentDecisionResponse(
            action=Action(
                action_type="request_history",
                details={},
                reasoning=f"Error in AI model: {error}. Using default safe action.",
            ),
            reasoning=f"Fallback action due to: {error}",
            confidence=0.3,
        )
