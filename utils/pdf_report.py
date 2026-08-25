from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
def create_report(text):
    filename = "AI_Report.pdf"
    pdf = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("<b>TalentSphere Elevate</b>", styles["Heading1"]))
    story.append(Paragraph("AI Resume Analysis Report", styles["Heading2"]))
    story.append(Paragraph(text.replace("\n", "<br/>"), styles["BodyText"]))
    pdf.build(story)
    return filename