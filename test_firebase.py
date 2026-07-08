from firebase import db

doc_ref = db.collection("patients").document("test")

doc_ref.set({
    "name": "Rahul",
    "age": 25,
    "risk": "Low"
})

print("Firebase Connected Successfully!")