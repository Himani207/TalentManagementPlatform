import streamlit as st
import PyPDF2

from utils.professional_sidebar import professional_sidebar


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ==========================================================
# LOAD PROFILE
# ==========================================================

profile = professional_sidebar()

if not profile:
    st.warning("Please complete your professional profile first.")
    st.stop()


# ==========================================================
# HEADER
# ==========================================================

st.title("📄 AI Resume Analyzer")

st.caption(
    "AI analyzes your resume structure and provides professional improvement suggestions."
)

st.divider()


# ==========================================================
# RESUME UPLOAD
# ==========================================================

uploaded_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)


# ==========================================================
# EXTRACT RESUME TEXT
# ==========================================================

def extract_resume_text(file):

    pdf_reader = PyPDF2.PdfReader(file)

    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text() or ""

    return text



# ==========================================================
# RESUME ANALYSIS
# ==========================================================

def analyze_resume(text, profile):

    text = text.lower()

    strengths = []

    suggestions = []


    # Name Check

    if profile["full_name"].lower() in text:

        strengths.append(
            "Your name is correctly mentioned in the resume."
        )

    else:

        suggestions.append(
            "Add your complete name clearly at the top of the resume."
        )


    # Experience

    if "experience" in text:

        strengths.append(
            "Experience section found."
        )

    else:

        suggestions.append(
            "Add your professional experience section."
        )


    # Projects

    if "project" in text:

        strengths.append(
            "Projects section is available."
        )

    else:

        suggestions.append(
            "Add technical projects to showcase your skills."
        )


    # Education

    if "education" in text or "degree" in text:

        strengths.append(
            "Education details found."
        )

    else:

        suggestions.append(
            "Add your education details."
        )


    # Certifications

    if "certification" in text:

        strengths.append(
            "Certifications section found."
        )

    else:

        suggestions.append(
            "Add relevant certifications."
        )


    # GitHub

    if "github" in text:

        strengths.append(
            "GitHub profile link found."
        )

    else:

        suggestions.append(
            "Add your GitHub profile link."
        )


    # LinkedIn

    if "linkedin" in text:

        strengths.append(
            "LinkedIn profile link found."
        )

    else:

        suggestions.append(
            "Add your LinkedIn profile link."
        )


    return strengths, suggestions



# ==========================================================
# ANALYZE BUTTON
# ==========================================================

if uploaded_file:

    st.success(
        "Resume uploaded successfully!"
    )


    if st.button(
        "🤖 Analyze Resume",
        use_container_width=True
    ):


        with st.spinner(
            "AI analyzing your resume..."
        ):


            resume_text = extract_resume_text(
                uploaded_file
            )


            strengths, suggestions = analyze_resume(
                resume_text,
                profile
            )


        st.divider()


        # ==================================================
        # RESULT
        # ==================================================

        st.subheader(
            "📊 Resume Analysis Result"
        )


        st.markdown(
            "### ✅ Resume Strengths"
        )


        for item in strengths:

            st.success(item)



        st.divider()


        st.markdown(
            "### 💡 Improvement Suggestions"
        )


        if suggestions:

            for item in suggestions:

                st.warning(item)

        else:

            st.success(
                "Your resume contains all important professional sections."
            )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "TalentSphere Elevate • AI Powered Resume Analyzer"
)

