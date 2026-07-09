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

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    data = json.loads(text)

    symptoms = [s.lower() for s in data.get("symptoms", [])]

    if any("chest pain" in s for s in symptoms):
        risk = "High"
    elif any("shortness of breath" in s for s in symptoms):
        risk = "Moderate"
    elif any("fever" in s for s in symptoms):
        risk = "Moderate"
    else:
        risk = "Low"

    data["risk"] = risk

    return data