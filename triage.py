import os
import json
from firebase import db
from dotenv import load_dotenv
from google import genai

from prompts import SYSTEM_PROMPT

# Load .env file
load_dotenv()

# Read API Key
API_KEY = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=API_KEY)


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

    # -----------------------------
    # Risk Prediction
    # -----------------------------

    symptoms = [s.lower() for s in data.get("symptoms", [])]

    if any("chest pain" in s for s in symptoms):
        risk = "🔴 High"

    elif any("shortness of breath" in s for s in symptoms):
        risk = "🟠 Medium"

    elif any("fever" in s for s in symptoms):
        risk = "🟡 Medium"

    else:
        risk = "🟢 Low"

    data["risk"] = risk
# Save patient report to Firestore
    db.collection("patients").add(data)
    return data