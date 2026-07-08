from firebase import db
from firebase_admin import firestore

def save_patient(data):

    data["timestamp"] = firestore.SERVER_TIMESTAMP

    db.collection("patients").add(data)