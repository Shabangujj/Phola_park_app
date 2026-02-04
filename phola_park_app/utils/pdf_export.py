from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_reports_pdf(path, reports):
    doc = SimpleDocTemplate(path)
    styles = getSampleStyleSheet()
    elements = []

    for r in reports:
        elements.append(
            Paragraph(
                f"Report #{r.id} - {r.category} - {r.status}",
                styles["Normal"]
            )
        )

    doc.build(elements)
