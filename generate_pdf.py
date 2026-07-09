from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph


def create_pdf(report):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b><font size=18>🏥 MedGuard AI</font></b>", styles["Title"]))
    story.append(Paragraph("<b>AI Powered Patient Triage Report</b><br/><br/>", styles["Heading2"]))

    story.append(Paragraph(f"<b>Name:</b> {report['name']}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Age:</b> {report['age']}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Symptoms:</b> {', '.join(report['symptoms'])}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Allergies:</b> {', '.join(report['allergies'])}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Medications:</b> {', '.join(report['medications'])}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Risk Level:</b> {report['risk']}", styles["BodyText"]))

    doc.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf