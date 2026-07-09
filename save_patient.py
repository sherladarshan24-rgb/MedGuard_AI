from firebase import db
from firebase_admin import firestore
from datetime import datetime

def save_patient(data):

    data["timestamp"] = firestore.SERVER_TIMESTAMP
    data["date"] = datetime.now().strftime("%d-%m-%Y %H:%M")

    db.collection("patients").add(data)