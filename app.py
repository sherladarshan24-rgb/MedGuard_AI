from flask import Flask, render_template, request
from triage import analyze_patient
from save_patient import save_patient
from firebase import get_patients
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    report = None

    if request.method == "POST":
        patient_notes = request.form["patient_notes"]

        report = analyze_patient(patient_notes)

        save_patient(report)

    return render_template("index.html", report=report)
@app.route("/dashboard")
def dashboard():

    patients = get_patients()

    # Search
    search = request.args.get("search", "").lower()

    if search:
        patients = [
            p for p in patients
            if search in p.get("name", "").lower()
        ]

    total = len(patients)

    high = sum(1 for p in patients if "High" in p["risk"])
    moderate = sum(1 for p in patients if "Moderate" in p["risk"])
    low = sum(1 for p in patients if "Low" in p["risk"])

    return render_template(
        "dashboard.html",
        patients=patients,
        total=total,
        high=high,
        moderate=moderate,
        low=low,
        search=search
    )
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)