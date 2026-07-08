import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

if not firebase_admin._apps:

    firebase_credentials = json.loads(
        os.environ["FIREBASE_CREDENTIALS"]
    )

    cred = credentials.Certificate(firebase_credentials)

    firebase_admin.initialize_app(cred)

db = firestore.client()


def get_patients():

    docs = db.collection("patients").stream()

    patients = []

    for doc in docs:
        patient = doc.to_dict()
        patient["id"] = doc.id
        patients.append(patient)

    return patients