import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()


# Get all patients from Firestore
def get_patients():
    docs = db.collection("patients").stream()

    patients = []

    for doc in docs:
        patient = doc.to_dict()
        patient["id"] = doc.id
        patients.append(patient)

    return patients