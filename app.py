from flask import (
    Flask,
    render_template,
    request,
    send_file,
    redirect
)

from io import BytesIO

from generate_pdf import create_pdf
from triage import analyze_patient
from save_patient import save_patient

from firebase import (
    get_patients,
    get_patient,
    delete_patient
)


app = Flask(__name__)

latest_report = None

app.secret_key = "medguard_ai_secret"



# Home page - Patient screening
@app.route("/", methods=["GET", "POST"])
def home():

    global latest_report

    report = None


    if request.method == "POST":

        patient_notes = request.form["patient_notes"]

        report = analyze_patient(patient_notes)

        latest_report = report

        save_patient(report)


    return render_template(
        "index.html",
        report=report
    )





# Dashboard
@app.route("/dashboard")
def dashboard():

    patients = get_patients()


    # Search
    search = request.args.get("search", "").lower()


    if search:

        patients = [
            p for p in patients
            if search in (p.get("name") or "").lower()
        ]



    # Statistics

    total = len(patients)


    high = sum(
        1 for p in patients
        if "High" in p.get("risk", "")
    )


    moderate = sum(
        1 for p in patients
        if "Moderate" in p.get("risk", "")
        or "Medium" in p.get("risk", "")
    )


    low = sum(
        1 for p in patients
        if "Low" in p.get("risk", "")
    )



    return render_template(
        "dashboard.html",
        patients=patients,
        total=total,
        high=high,
        moderate=moderate,
        low=low,
        search=search
    )






# Delete patient
@app.route("/delete/<patient_id>")
def delete(patient_id):

    delete_patient(patient_id)

    return redirect("/dashboard")






# Download PDF Report
@app.route("/download_report")
def download_report():

    global latest_report


    if latest_report is None:

        return "No report available."



    pdf = create_pdf(latest_report)



    return send_file(
        BytesIO(pdf),
        download_name="Patient_Report.pdf",
        as_attachment=True,
        mimetype="application/pdf"
    )

@app.route("/patient/<patient_id>")
def patient(patient_id):

    patient = get_patient(patient_id)

    if patient is None:
        return "Patient not found"

    return render_template(
        "patient_details.html",
        patient=patient
    )




if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )