import streamlit as st
from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from utils.session import logout
from utils.college_db import get_profile
from utils.resume_db import save_resume_score


# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Resume Builder",
    page_icon="📄",
    layout="wide"
)
# =====================================================
# LOGIN CHECK
# =====================================================

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.switch_page("pages/login.py")

email = st.session_state.email


# =====================================================
# GET PROFILE FROM DATABASE
# =====================================================

profile = get_profile(email)
# ====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🎓 TalentSphere")

    st.divider()

    st.page_link(
        "pages/college.py",
        label="🏠 Dashboard"
    )

    st.page_link(
        "pages/profile.py",
        label="👤 Profile"
    )


    if st.button("🚪 Logout"):
        logout()
        st.switch_page("app.py")



# =====================================================
# TITLE
# =====================================================

st.title("📄 AI Professional Resume Builder")

if not profile:

    st.warning(
        "Please complete your profile first."
    )

    if st.button("Go To Profile"):
        st.switch_page(
            "pages/profile.py"
        )

    st.stop()



# =====================================================
# AUTO FILLED DATA
# =====================================================

default_name = profile["full_name"]

default_college = profile["college"]

default_degree = profile["degree"]

default_department = profile["department"]

default_year = profile["year"]

default_skills = profile["skills"]

default_about = profile["about"]



# =====================================================
# RESUME FORM
# =====================================================

with st.form("resume"):


    st.subheader("👤 Personal Details")


    name = st.text_input(
        "Name",
        value=default_name
    )


    email_id = st.text_input(
        "Email",
        value=email
    )


    phone = st.text_input(
        "Phone",
        value=profile["phone"]
    )


    linkedin = st.text_input(
        "LinkedIn"
    )


    github = st.text_input(
        "GitHub"
    )



    st.divider()



    st.subheader("🎯 Professional Summary")


    summary = st.text_area(
        "Summary",
        value=default_about
    )



    st.subheader("🎓 Education")


    education = st.text_area(
        "Education",
        value=f"""
{default_degree}
{default_department}
{default_college}
{default_year}
"""
    )



    st.subheader("💻 Skills")


    skills = st.text_area(
        "Skills",
        value=default_skills
    )



    st.subheader("🚀 Projects")


    projects = st.text_area(
        "Projects",
        placeholder="""
Project Name:
Technology Used:
Your Contribution:
Outcome:
"""
    )



    st.subheader("🏆 Achievements")


    achievements = st.text_area(
        "Achievements"
    )



    submit = st.form_submit_button(
        "✨ Generate Resume"
    )



# =====================================================
# PDF GENERATOR
# =====================================================

def generate_pdf(text):

    buffer = BytesIO()

    pdf = SimpleDocTemplate(
        buffer,
        pagesize=letter
    )


    styles = getSampleStyleSheet()

    content=[]


    for line in text.split("\n"):

        content.append(
            Paragraph(
                line,
                styles["Normal"]
            )
        )

        content.append(
            Spacer(1,10)
        )


    pdf.build(content)

    buffer.seek(0)

    return buffer



# =====================================================
# GENERATE
# =====================================================

if submit:


    resume = f"""

{name}

{default_degree} | {default_department}



CONTACT

Email: {email_id}

Phone: {phone}

LinkedIn: {linkedin}

Github: {github}



PROFESSIONAL SUMMARY

{summary}



EDUCATION

{education}



TECHNICAL SKILLS

{skills}



PROJECTS

{projects}



ACHIEVEMENTS

{achievements}

"""



    st.success(
        "Resume Created Successfully 🎉"
    )


    st.subheader(
        "📄 Preview"
    )


    st.text(resume)



    pdf = generate_pdf(
        resume
    )


    st.download_button(
        "⬇ Download PDF Resume",
        pdf,
        file_name=f"{name}_Resume.pdf",
        mime="application/pdf"
    )



# =====================================================
# ATS SCORE
# =====================================================
if submit:

    score = 0

    if skills:
        score += 20

    if projects:
        score += 20

    if linkedin:
        score += 15

    if github:
        score += 15

    if achievements:
        score += 10

    if summary:
        score += 20

    # Save ATS score to database
    save_resume_score(email, score)
    st.subheader("🤖 ATS Resume Score")

    st.progress(score / 100)

    st.metric(
        "ATS Score",
        f"{score}%"
    )
    