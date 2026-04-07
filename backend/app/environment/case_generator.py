"""Case generator for different clinical tasks."""

import random
from typing import Dict, Any
from app.models.schemas import PatientInfo, Vitals, Observation


class CaseGenerator:
    """Generates medical cases for simulation tasks."""
    
    TASKS = {
        "viral_uri": {
            "title": "Viral Upper Respiratory Infection",
            "description": "Diagnose and manage a common viral URI",
            "difficulty": "easy",
        },
        "type2_diabetes": {
            "title": "Type 2 Diabetes Management",
            "description": "Manage blood glucose and diabetes complications",
            "difficulty": "medium",
        },
        "sepsis_triage": {
            "title": "Sepsis Triage and Treatment",
            "description": "Quickly identify sepsis and initiate proper treatment",
            "difficulty": "hard",
        },
        "drug_interaction": {
            "title": "Drug Interaction Management",
            "description": "Identify harmful drug interactions and optimize therapy",
            "difficulty": "hard",
        },
        "rare_disease_hunt": {
            "title": "Rare Disease Diagnosis",
            "description": "Diagnose a rare but important disease from vague symptoms",
            "difficulty": "expert",
        },
    }

    @staticmethod
    def generate_viral_uri() -> Observation:
        """Generate viral URI case."""
        patient = PatientInfo(
            name="John Smith",
            age=random.randint(25, 45),
            gender=random.choice(["M", "F"]),
            presenting_complaint="Sore throat, runny nose, and cough",
            medical_history=["Seasonal allergies"],
            current_medications=["Loratadine"],
            allergies=["Penicillin"],
        )
        
        vitals = Vitals(
            heart_rate=random.randint(80, 95),
            blood_pressure="120/78",
            temperature=round(37.8 + random.uniform(0, 0.5), 1),
            respiratory_rate=random.randint(14, 18),
            oxygen_saturation=98.0,
        )
        
        symptoms = ["Sore throat", "Rhinorrhea", "Mild cough", "Fatigue"]
        physical_exam = {
            "oropharynx": "Mild erythema, no exudate",
            "neck_lymph_nodes": "Slightly enlarged but mobile",
            "lungs": "Clear to auscultation bilaterally",
        }
        
        return Observation(
            patient_info=patient,
            vitals=vitals,
            symptoms=symptoms,
            physical_exam_findings=physical_exam,
            lab_results=None,
            imaging_results=None,
            case_id="viral_uri_001",
            episode_number=1,
            task_name="viral_uri",
        )

    @staticmethod
    def generate_type2_diabetes() -> Observation:
        """Generate type 2 diabetes case."""
        patient = PatientInfo(
            name="Mary Johnson",
            age=random.randint(45, 65),
            gender="F",
            presenting_complaint="Routine diabetes follow-up",
            medical_history=["Type 2 Diabetes (8 years)", "Hypertension", "Obesity"],
            current_medications=["Metformin 1000mg BID", "Lisinopril 10mg daily"],
            allergies=["NSAIDs"],
        )
        
        vitals = Vitals(
            heart_rate=random.randint(75, 85),
            blood_pressure=f"{140 + random.randint(-10, 10)}/{90 + random.randint(-5, 5)}",
            temperature=36.8,
            respiratory_rate=16,
            oxygen_saturation=97.0,
        )
        
        symptoms = ["Mild leg pain", "Occasional blurred vision"]
        physical_exam = {
            "weight": f"{95 + random.randint(-5, 5)} kg",
            "bmi": f"{35 + random.randint(-2, 2):.1f}",
            "feet": "Decreased sensation to monofilament",
        }
        
        lab_results = {
            "glucose": f"{180 + random.randint(-30, 30)} mg/dL",
            "HbA1c": f"{8.2 + random.uniform(-0.5, 0.5):.1f}%",
            "creatinine": f"{1.1 + random.uniform(-0.1, 0.1):.2f}",
        }
        
        return Observation(
            patient_info=patient,
            vitals=vitals,
            symptoms=symptoms,
            physical_exam_findings=physical_exam,
            lab_results=lab_results,
            imaging_results=None,
            case_id="diabetes_001",
            episode_number=1,
            task_name="type2_diabetes",
        )

    @staticmethod
    def generate_sepsis_triage() -> Observation:
        """Generate sepsis triage case."""
        patient = PatientInfo(
            name="Robert Davis",
            age=random.randint(60, 80),
            gender="M",
            presenting_complaint="Confusion, fever, unwell",
            medical_history=["COPD", "Benign prostate hyperplasia"],
            current_medications=["Albuterol inhaler"],
            allergies=["Sulfa drugs"],
        )
        
        vitals = Vitals(
            heart_rate=random.randint(110, 130),
            blood_pressure=f"{90 + random.randint(-10, 10)}/{55 + random.randint(-5, 5)}",
            temperature=39.2 + random.uniform(-0.5, 1.0),
            respiratory_rate=random.randint(22, 28),
            oxygen_saturation=94.0 + random.uniform(-2, 0),
        )
        
        symptoms = ["Fever", "Confusion", "Difficulty breathing", "Myalgia"]
        physical_exam = {
            "mental_status": "Altered, confused",
            "skin": "Cold, clammy, signs of poor perfusion",
            "lungs": "Crackles in left lower lobe",
        }
        
        lab_results = {
            "WBC": f"{18 + random.randint(-3, 5)}",
            "lactate": f"{2.5 + random.uniform(0, 1.5):.1f}",
            "procalcitonin": f"{5.2 + random.uniform(0, 3.0):.1f}",
        }
        
        return Observation(
            patient_info=patient,
            vitals=vitals,
            symptoms=symptoms,
            physical_exam_findings=physical_exam,
            lab_results=lab_results,
            imaging_results=None,
            case_id="sepsis_001",
            episode_number=1,
            task_name="sepsis_triage",
        )

    @staticmethod
    def generate_drug_interaction() -> Observation:
        """Generate drug interaction case."""
        patient = PatientInfo(
            name="Patricia Miller",
            age=random.randint(55, 70),
            gender="F",
            presenting_complaint="Dizziness, increased bleeding, muscle pain",
            medical_history=["Atrial fibrillation", "Arthritis", "High cholesterol"],
            current_medications=[
                "Warfarin 5mg daily",
                "Atorvastatin 20mg daily",
                "Ibuprofen 600mg TID",
                "Metronidazole 500mg BID",
            ],
            allergies=["Penicillin"],
        )
        
        vitals = Vitals(
            heart_rate=random.randint(88, 100),
            blood_pressure="128/82",
            temperature=36.8,
            respiratory_rate=16,
            oxygen_saturation=98.0,
        )
        
        symptoms = ["Dizziness", "Unusual bruising", "Muscle aches", "GI upset"]
        physical_exam = {
            "skin": "Multiple petechiae and ecchymosis",
            "abdomen": "Mild discomfort, soft",
            "neuro": "Intact",
        }
        
        lab_results = {
            "INR": f"{4.5 + random.uniform(-0.5, 1.0):.1f}",
            "Hgb": f"{11.2 + random.uniform(-0.5, 0.0):.1f}",
            "AST": f"{55 + random.randint(-10, 20)}",
        }
        
        return Observation(
            patient_info=patient,
            vitals=vitals,
            symptoms=symptoms,
            physical_exam_findings=physical_exam,
            lab_results=lab_results,
            imaging_results=None,
            case_id="drug_interaction_001",
            episode_number=1,
            task_name="drug_interaction",
        )

    @staticmethod
    def generate_rare_disease() -> Observation:
        """Generate rare disease case."""
        patient = PatientInfo(
            name="William Wilson",
            age=random.randint(40, 60),
            gender="M",
            presenting_complaint="Progressive weakness, dark urine, abdominal pain",
            medical_history=["None significant"],
            current_medications=["Vitamin D"],
            allergies=["None"],
        )
        
        vitals = Vitals(
            heart_rate=random.randint(95, 105),
            blood_pressure=f"{125 + random.randint(-10, 10)}/{80 + random.randint(-5, 5)}",
            temperature=37.0 + random.uniform(0, 0.5),
            respiratory_rate=18,
            oxygen_saturation=97.5,
        )
        
        symptoms = ["Progressive muscle weakness", "Dark urine", "Abdominal pain", "Nausea"]
        physical_exam = {
            "abdomen": "Tenderness in right upper quadrant",
            "neuro": "Proximal muscle weakness appreciated",
            "skin": "Normal",
        }
        
        lab_results = {
            "CK": f"{2500 + random.randint(-500, 1500)}",
            "myoglobin": f"{85 + random.randint(0, 100)}",
            "creatinine": f"{1.8 + random.uniform(-0.2, 0.4):.1f}",
            "urine_color": "Dark brown (myoglobin positive)",
        }
        
        return Observation(
            patient_info=patient,
            vitals=vitals,
            symptoms=symptoms,
            physical_exam_findings=physical_exam,
            lab_results=lab_results,
            imaging_results=None,
            case_id="rare_disease_001",
            episode_number=1,
            task_name="rare_disease_hunt",
        )

    @staticmethod
    def generate_case(task: str) -> Observation:
        """Generate case for specified task."""
        generators = {
            "viral_uri": CaseGenerator.generate_viral_uri,
            "type2_diabetes": CaseGenerator.generate_type2_diabetes,
            "sepsis_triage": CaseGenerator.generate_sepsis_triage,
            "drug_interaction": CaseGenerator.generate_drug_interaction,
            "rare_disease_hunt": CaseGenerator.generate_rare_disease,
        }
        
        if task not in generators:
            raise ValueError(f"Unknown task: {task}")
        
        return generators[task]()
