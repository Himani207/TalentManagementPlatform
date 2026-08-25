import streamlit as st

from utils.session import logout
from utils.school_db import (
    create_student_table,
    get_student_profile,
    save_profile,
    calculate_profile_completion
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Student Profile",
    page_icon="👤",
    layout="wide"
)

# ==========================================================
# LOGIN CHECK
# ==========================================================

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.switch_page("pages/login.py")
    st.stop()

email = st.session_state.email

# ==========================================================
# CREATE TABLE
# ==========================================================

create_student_table()

# ==========================================================
# GET PROFILE
# ==========================================================

profile = get_student_profile(email)

if profile is None:
    profile = {
        "email": email,
        "parent_email": "",
        "age": 15,
        "class": "",
        "school": "",
        "interests": "",
        "subject": "",
        "career": "",
        "goal": ""
    }
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
        "pages/school_profile.py",
        label="👤 Student Profile"
    )
    st.page_link(
        "pages/school_career.py",
        label="🎯 Career Assessment"
    )

    st.page_link(
        "pages/school_roadmap.py",
        label="📚 Learning Roadmap"
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

st.title("👤 Student Profile")

st.write(
    "Complete your profile to get personalized "
    "career recommendations and learning suggestions."
)
st.divider()
# ==========================================================
# PROFILE COMPLETION
# ==========================================================

completion = calculate_profile_completion(email)

st.subheader("📊 Profile Completion")

st.progress(
    min(completion, 100) / 100
)

st.write(f"**{completion}% Complete**")

st.divider()
# ==========================================================
# PROFILE FORM
# ==========================================================

with st.form("student_profile_form"):

    # ======================================================
    # PERSONAL + CAREER INFORMATION
    # ======================================================

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("👤 Personal Information")

        parent_email = st.text_input(
            "Parent Email",
            value=profile.get("parent_email") or ""
        )

        age = st.number_input(
            "Age",
            min_value=10,
            max_value=25,
            value=int(profile.get("age") or 15)
        )

        class_name = st.text_input(
            "Class",
            value=profile.get("class") or "",
            placeholder="Example: 10"
        )

        school = st.text_input(
            "School Name",
            value=profile.get("school") or ""
        )

    with col2:

        st.subheader("🎯 Career Information")

        interests = st.text_input(
            "Interests",
            value=profile.get("interests") or "",
            placeholder="Example: Programming, Science, Sports"
        )

        career = st.text_input(
            "Dream Career",
            value=profile.get("career") or "",
            placeholder="Example: Software Engineer"
        )

        goal = st.text_area(
            "Career Goal",
            value=profile.get("goal") or "",
            placeholder="Example: Become a software engineer"
        )

    # ======================================================
    # ACADEMIC INFORMATION
    # ======================================================
    st.divider()
    st.subheader("📚 Academic Information")
    academic_col1, academic_col2 = st.columns(2)
    with academic_col1:
        overall_percentage = st.text_input(
            "Overall Percentage",
            value=str(profile.get("overall_percentage") or ""),
            placeholder="Example: 80.5"
        )
        recent_exam_score = st.text_input(
            "Recent Exam Score",
            value=str(profile.get("recent_exam_score") or ""),
            placeholder="Example: 80.5"
        )
        favourite_subject = st.text_input(
            "Favourite Subject",
            value=profile.get("favourite_subject") or "",
            placeholder="Example: Mathematics"
        )

        strong_subjects = st.text_input(
            "Strong Subjects",
            value=profile.get("strong_subjects") or "",
            placeholder="Example: Mathematics, Science"
        )

    with academic_col2:

        weak_subjects = st.text_input(
            "Subjects Needing Improvement",
            value=profile.get("weak_subjects") or "",
            placeholder="Example: English, Social Science"
        )
        attendance_percentage = st.text_input(
            "Attendance Percentage",
            value=str(profile.get("attendance_percentage") or ""),
            placeholder="Example: 80.5"
        )
        academic_achievements = st.text_area(
        "Academic Achievements",
        value=profile.get("academic_achievements") or "",
        placeholder="Example: School topper, Science competition"
        )

        academic_goal = st.text_area(
            "Academic Goal",
            value=profile.get("academic_goal") or "",
            placeholder="Example: Score above 90% in final exams"
        )

    # ======================================================
    # SAVE BUTTON
    # ======================================================

    st.divider()

    submitted = st.form_submit_button(
        "💾 Save Profile",
        use_container_width=True
    )
# ==========================================================
# SAVE PROFILE DATA
# ==========================================================
if submitted:

    try:
        overall_percentage = float(overall_percentage)
        recent_exam_score = float(recent_exam_score)
        attendance_percentage = float(attendance_percentage)
    except ValueError:
        st.error("Please enter valid percentage values, e.g. 80 or 80.5")
        st.stop()

    if not 0 <= overall_percentage <= 100:
        st.error("Overall Percentage must be between 0 and 100.")
        st.stop()

    if not 0 <= recent_exam_score <= 100:
        st.error("Recent Exam Score must be between 0 and 100.")
        st.stop()

    if not 0 <= attendance_percentage <= 100:
        st.error("Attendance Percentage must be between 0 and 100.")
        st.stop()

    save_profile(
        email=email,
        parent_email=parent_email,
        age=age,
        class_name=class_name,
        school=school,
        interests=interests,
        favorite_subject=favourite_subject,
        dream_career=career,
        goals=goal,
        overall_percentage=overall_percentage,
        recent_exam_score=recent_exam_score,
        strong_subjects=strong_subjects,
        weak_subjects=weak_subjects,
        academic_achievements=academic_achievements,
        attendance_percentage=attendance_percentage,
        academic_goal=academic_goal
    )

    st.success("✅ Profile saved successfully!")