import os
import json
from dotenv import load_dotenv
from google import genai

from prompts import SYSTEM_PROMPT

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_patient(notes):

    prompt = f"""
{SYSTEM_PROMPT}

Patient Notes:

{notes}
"""

    try:
            response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

    except Exception:
        return {
            "name": "Unavailable",
            "age": "",
            "symptoms": [],
            "allergies": [],
            "medications": [],
            "risk": "Unable to analyze now. Gemini API quota exceeded.",
            "score": 0,
            "department": "Not Available",
            "recommendation": [
                "Please try again later."
            ],
            "reason": [
                "Gemini API daily quota has been exceeded."
            ]
        }

    text = response.text.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    data = json.loads(text)
    # Default values if Gemini misses any field
    data.setdefault("name", "Unknown")
    data.setdefault("age", "N/A")
    data.setdefault("symptoms", [])
    data.setdefault("allergies", [])
    data.setdefault("medications", [])

    symptoms = [s.lower() for s in data["symptoms"]]

    if any("chest pain" in s for s in symptoms):
        risk = "High"
    elif any("shortness of breath" in s for s in symptoms):
        risk = "Moderate"
    elif any("fever" in s for s in symptoms):
        risk = "Moderate"
    else:
        risk = "Low"

    data["risk"] = risk
    if risk == "High":
        data["score"] = 92
        data["department"] = "Cardiology"
        data["recommendation"] = [
            "ECG",
            "Troponin Test",
            "Immediate Emergency Admission"
        ]
        data["reason"] = [
            "Severe chest pain detected",
            "Shortness of breath detected",
            "Possible cardiac emergency"
        ]

    elif risk == "Moderate":
        data["score"] = 65
        data["department"] = "General Medicine"
        data["recommendation"] = [
            "Clinical Examination",
            "Blood Tests",
            "Observation"
        ]
        data["reason"] = [
            "Moderate symptoms detected",
            "Needs physician evaluation"
        ]

    else:
        data["score"] = 20
        data["department"] = "General OPD"
        data["recommendation"] = [
            "Rest",
            "Hydration",
            "Routine Follow-up"
        ]
        data["reason"] = [
            "No emergency symptoms detected"
        ]
    return data