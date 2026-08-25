from PyPDF2 import PdfReader
from ai.gemini import ask_gemini


def extract_text(pdf):

    reader = PdfReader(pdf)

    text = ""

    for page in reader.pages:

        if page.extract_text():

            text += page.extract_text()

    return text


def analyze_resume(pdf):

    resume = extract_text(pdf)

    prompt = f"""
You are an ATS Resume Expert.

Analyze this resume.

Return your answer in this format.

1. ATS Score (0-100)

2. Strengths

3. Weaknesses

4. Missing Skills

5. Resume Improvements

6. Best Career Path

7. Suggested Certifications

8. Final Verdict

Resume:

{resume}

"""

    return ask_gemini(prompt)