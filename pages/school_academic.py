import streamlit as st

from utils.session import logout
from utils.school_db import (
    create_student_table,
    get_student_profile
)

# ==========================================================
# DATABASE
# ==========================================================

create_student_table()

# ==========================================================
# LOGIN CHECK
# ==========================================================

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.switch_page("pages/login.py")
    st.stop()

email = st.session_state.email

# ==========================================================
# GET STUDENT PROFILE
# ==========================================================

student = get_student_profile(email)

if student is None:
    st.warning("Student profile not found.")
    st.stop()

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Academic Information",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CSS
# ==========================================================

st.markdown(
    """
    <style>

    .academic-header {
        padding: 25px;
        border-radius: 18px;
        margin-bottom: 25px;
    }

    .academic-card {
        padding: 22px;
        border-radius: 16px;
        border: 1px solid rgba(128,128,128,0.2);
        margin-bottom: 18px;
        min-height: 130px;
    }

    .academic-card h3 {
        margin-bottom: 8px;
    }

    .academic-value {
        font-size: 20px;
        font-weight: 600;
    }

    .subject-box {
        padding: 18px;
        border-radius: 14px;
        border: 1px solid rgba(128,128,128,0.2);
        text-align: center;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("🏫 TalentSphere Elevate")
    st.caption("High School Student Portal")

    st.divider()

    st.page_link(
        "pages/school.py",
        label="🏠 Dashboard"
    )

    st.page_link(
        "pages/school_academic.py",
        label="📚 Academic Information"
    )

    st.page_link(
        "pages/school_career.py",
        label="🎯 Career Assessment"
    )

    st.page_link(
        "pages/school_roadmap.py",
        label="🗺 Learning Roadmap"
    )

    st.page_link(
        "pages/school_assessment.py",
        label="📝 Skill Assessment"
    )

    st.page_link(
        "pages/school_notifications.py",
        label="🔔 Notifications"
    )

    st.page_link(
        "pages/school_reports.py",
        label="📊 Reports"
    )

    st.page_link(
        "pages/school_ai_tools.py",
        label="🤖 AI Tools"
    )

    st.page_link(
        "pages/chatbot.py",
        label="💬 AI Chatbot"
    )

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):
        logout()
        st.switch_page("app.py")

# ==========================================================
# HEADER
# ==========================================================

st.markdown(
    """
    <div class="academic-header">

        <h1>📚 Academic Information</h1>

        <p>
            View your school and academic profile
            at one place.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# STUDENT INFORMATION
# ==========================================================

st.subheader("👨‍🎓 Student Information")

c1, c2, c3 = st.columns(3)

with c1:

    st.markdown(
        f"""
        <div class="academic-card">

            <h3>👤 Student</h3>

            <div class="academic-value">
                {st.session_state.get("name", "Student")}
            </div>

            <p>{student.get("email", email)}</p>

        </div>
        """,
        unsafe_allow_html=True
    )

with c2:

    st.markdown(
        f"""
        <div class="academic-card">

            <h3>🎓 Class</h3>

            <div class="academic-value">
                Class {student.get("class", "Not Available")}
            </div>

            <p>Current Class</p>

        </div>
        """,
        unsafe_allow_html=True
    )

with c3:

    school_name = student.get("school", "")

    if not school_name:
        school_name = "Not Added"

    st.markdown(
        f"""
        <div class="academic-card">

            <h3>🏫 School</h3>

            <div class="academic-value">
                {school_name}
            </div>

            <p>School Information</p>

        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================================
# ACADEMIC DETAILS
# ==========================================================

st.subheader("📖 Academic Details")

c1, c2 = st.columns(2)

with c1:

    subject = student.get("subject", "")

    if not subject:
        subject = "Not Selected"

    st.markdown(
        f"""
        <div class="academic-card">

            <h3>📚 Favourite Subject</h3>

            <div class="academic-value">
                {subject}
            </div>

            <p>
                Your preferred academic subject
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

with c2:

    interests = student.get("interests", "")

    if not interests:
        interests = "No interests added"

    st.markdown(
        f"""
        <div class="academic-card">

            <h3>💡 Interests</h3>

            <div class="academic-value">
                {interests}
            </div>

            <p>
                Areas you are interested in
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================================
# CAREER INFORMATION
# ==========================================================

st.subheader("🎯 Career Information")

c1, c2 = st.columns(2)

with c1:

    career = student.get("career", "")

    if not career:
        career = "Not Selected"

    st.markdown(
        f"""
        <div class="academic-card">

            <h3>🚀 Dream Career</h3>

            <div class="academic-value">
                {career}
            </div>

            <p>
                Your selected career goal
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

with c2:

    goal = student.get("goal", "")

    if not goal:
        goal = "No goal added"

    st.markdown(
        f"""
        <div class="academic-card">

            <h3>🎯 Short-Term Goal</h3>

            <div class="academic-value">
                {goal}
            </div>

            <p>
                Your current academic goal
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================================
# ACADEMIC SUMMARY
# ==========================================================

st.subheader("📊 Academic Summary")

summary1, summary2, summary3, summary4 = st.columns(4)

with summary1:

    st.metric(
        "🎓 Class",
        student.get("class", "N/A")
    )

with summary2:

    st.metric(
        "📚 Subject",
        student.get("subject") or "N/A"
    )

with summary3:

    st.metric(
        "🎯 Career",
        student.get("career") or "N/A"
    )

with summary4:

    age = student.get("age")

    if age:
        age_value = str(age)
    else:
        age_value = "N/A"

    st.metric(
        "🎂 Age",
        age_value
    )

# ==========================================================
# INTERESTS
# ==========================================================

st.subheader("💡 My Interests")

interest_text = student.get("interests", "")

if interest_text:

    interests_list = [
        item.strip()
        for item in interest_text.split(",")
        if item.strip()
    ]

    if interests_list:

        columns = st.columns(
            min(len(interests_list), 4)
        )

        for index, interest in enumerate(interests_list):

            with columns[index % len(columns)]:

                st.markdown(
                    f"""
                    <div class="subject-box">

                        <h3>💡</h3>

                        <b>{interest}</b>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

else:

    st.info(
        "No interests have been added to your profile yet."
    )

# ==========================================================
# PARENT INFORMATION
# ==========================================================

st.subheader("👨‍👩‍👧 Parent Information")

parent_email = student.get("parent_email", "")

if parent_email:

    st.success(
        f"Parent Email: {parent_email}"
    )

else:

    st.info(
        "Parent email has not been added yet."
    )

# ==========================================================
# EDIT PROFILE
# ==========================================================

st.divider()

if st.button(
    "✏️ Update Academic Information",
    use_container_width=True
):

    st.switch_page(
        "pages/school_profile.py"
    )
