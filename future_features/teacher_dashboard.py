import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from ai.gemini import ask_gemini
from utils.session import logout
from PIL import Image

from utils.school_db import (
    get_all_students,
    get_total_students,
    get_student_profile
)
from future_db.teacher_db import (
    add_feedback,
    add_assignment,
    get_assessments
)
from utils.notification_db import (
    get_notifications,
    add_notification
)


# ----------------------------------------------------
# PAGE CONFIGURATION
# ----------------------------------------------------

st.set_page_config(
    page_title="Teacher Dashboard",
    page_icon="👨‍🏫",
    layout="wide"
)

# ----------------------------------------------------
# LOAD CSS
# ----------------------------------------------------

css_file = Path(__file__).parent.parent / "assets" / "style.css"

if css_file.exists():
    with open(css_file) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# ----------------------------------------------------
# LOGIN CHECK
# ----------------------------------------------------

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.stop()

# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------
logo = Path(__file__).parent.parent / "assets" / "logo.png"

if logo.exists():
    try:
        img = Image.open(logo)
        st.sidebar.image(img, width=120)
    except Exception:
        st.sidebar.warning("Logo image is invalid.")

st.sidebar.title("👨‍🏫 Teacher Dashboard")

st.sidebar.success(f"👤 {st.session_state.name}")

st.sidebar.info(st.session_state.email)

st.sidebar.markdown("---")

st.sidebar.write("🏠 Dashboard")
st.sidebar.write("👨‍🎓 Students")
st.sidebar.write("📚 Assignments")
st.sidebar.write("📝 Assessments")
st.sidebar.write("📊 Analytics")
st.sidebar.write("📩 Messages")
st.sidebar.write("🔔 Notifications")

st.sidebar.markdown("---")

if st.sidebar.button("🚪 Logout"):
    logout()
    st.switch_page("app.py")

# ----------------------------------------------------
# HEADER
# ----------------------------------------------------

st.title("👨‍🏫 Teacher Dashboard")

st.info(
"""
Welcome to TalentSphere Elevate.

Monitor student progress, assessments and career development.
"""
)

st.markdown("---")

# ----------------------------------------------------
# DASHBOARD METRICS
# ----------------------------------------------------

st.header("📊 Dashboard Analytics")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric(
        "Students",
        get_total_students()
    )
with c2:
    st.metric("Assessments", "48")

with c3:
    st.metric("Average Score", "86%")

with c4:
    st.metric("Attendance", "94%")

c5, c6, c7 = st.columns(3)

with c5:
    st.metric("Assignments", "32")

with c6:
    st.metric("AI Readiness", "89%")

with c7:
    st.metric("Career Match", "92%")

st.markdown("---")

# ----------------------------------------------------
# STUDENT OVERVIEW
# ----------------------------------------------------

st.header("👨‍🎓 Student Overview")
students = get_all_students()
if students:

    df = pd.DataFrame(students)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No student records found.")

st.markdown("---")
# ----------------------------------------------------
# STUDENT PERFORMANCE
# ----------------------------------------------------
st.header("📈 Student Performance")
performance = pd.DataFrame(
    {
        "Subject": [
            "Mathematics",
            "Science",
            "English",
            "Computer Science"
        ],
        "Average Marks": [
            88,
            84,
            79,
            93
        ]
    }
)

fig = px.bar(
    performance,
    x="Subject",
    y="Average Marks",
    color="Average Marks",
    text="Average Marks",
    color_continuous_scale="Viridis",
    title="Average Subject Performance"
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")
# ----------------------------------------------------
# ATTENDANCE
# ----------------------------------------------------
st.header("🏫 Attendance Summary")
attendance = pd.DataFrame(
    {
        "Class": [
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12"
        ],
        "Attendance": [
            94,
            95,
            91,
            96,
            92,
            93,
            95
        ]
    }
)

fig = px.line(
    attendance,
    x="Class",
    y="Attendance",
    markers=True,
    title="Attendance by Class"
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.markdown("---")
# ----------------------------------------------------
# STUDENT SEARCH
# ----------------------------------------------------
st.header("🔍 Search Students")
search = st.text_input("Search by Name or School")
if students:
    search_df = df.copy()
    if search.strip():
        search = search.lower()
        search_df = search_df[
            search_df.astype(str)
            .apply(lambda x: x.str.lower())
            .any(axis=1)
        ]

    st.dataframe(
        search_df,
        use_container_width=True,
        hide_index=True
    )

st.markdown("---")
# ----------------------------------------------------
# ASSESSMENT RESULTS
# ----------------------------------------------------
st.header("📝 Assessment Results")
assessment = pd.DataFrame(get_assessments())
if not assessment.empty:
    assessment["score"] = assessment["score"].round(1)
    st.dataframe(
        assessment,
        use_container_width=True,
        hide_index=True
    )
    fig = px.bar(
        assessment,
        x="quiz",
        y="score",
        color="score",
        text="score",
        color_continuous_scale="Viridis",
        title="Assessment Performance"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:
    st.info("No assessment data available yet.")

st.markdown("---")
#-----------------------------------------------------
# ASSIGNMENT MANAGEMENT
# ----------------------------------------------------
st.header("📚 Assignment Management")
assignment = st.text_input("Assignment Title")
due_date = st.date_input("Due Date")
description = st.text_area("Assignment Description")
if st.button("➕ Publish Assignment"):
    if assignment.strip() == "":
        st.warning("Please enter assignment title.")
    else:

        add_assignment(
            assignment,
            description,
            str(due_date)
        )

        st.success("✅ Assignment Published Successfully!")
st.markdown("---")
# ----------------------------------------------------
# CAREER RECOMMENDATION SUMMARY
# ----------------------------------------------------
st.header("🎯 Career Recommendation Summary")
career_df = pd.DataFrame(
    {
        "Career": [
            "AI Engineer",
            "Software Developer",
            "Data Scientist",
            "Robotics Engineer"
        ],
        "Students Interested": [
            35,
            28,
            18,
            12
        ]
    }
)

fig = px.pie(
    career_df,
    names="Career",
    values="Students Interested",
    hole=0.45,
    title="Career Interests"
)
fig.update_layout(
    template="plotly_white"
)
st.plotly_chart(
    fig,
    use_container_width=True
)
st.markdown("---")
# ----------------------------------------------------
# TEACHER FEEDBACK
# ----------------------------------------------------
st.header("💬 Teacher Feedback")
student_list = get_all_students()
student_options = [s["email"] for s in student_list]
selected_student = st.selectbox(
    "Select Student",
    student_options if student_options else ["No students available"]
)

feedback = st.text_area("Write Feedback")

if st.button("📩 Send Feedback"):

    if not student_options:
        st.warning("No students available.")

    elif feedback.strip() == "":
        st.warning("Please write feedback.")

    else:
        # Save feedback
        add_feedback(
            selected_student,
            st.session_state.name,
            feedback
        )

        # Notify student
        add_notification(
            selected_student,
            "Your teacher has submitted new feedback.",
            "info"
        )

        # Notify parent (if parent email exists)
        student = get_student_profile(selected_student)

        if student.get("parent_email"):
            add_notification(
                student["parent_email"],
                "Teacher has submitted feedback for your child.",
                "info"
            )

        st.success("✅ Feedback Sent Successfully.")

# ----------------------------------------------------
# PARENT MESSAGE
# ----------------------------------------------------
st.header("👨‍👩‍👧 Parent Communication")
parent_list = get_all_students()

parent_options = {}

for student in parent_list:

    student = dict(student)   # convert sqlite Row to dictionary

    if student.get("parent_email"):

        parent_options[
            student["parent_email"]
        ] = student.get(
            "student_name",
            student.get("email", "Student")
        )
selected_parent = st.selectbox(
    "Select Parent",
    list(parent_options.keys())
    if parent_options
    else ["No parent available"]
)
parent_message = st.text_area("Message to Parent")


if st.button("📨 Send Parent Message"):

    if selected_parent == "No parent available":
        st.warning("No parent email found.")

    elif parent_message.strip() == "":
        st.warning("Please enter a message.")

    else:

        add_notification(
            selected_parent,
            f"Message from Teacher {st.session_state.name}: {parent_message}",
            "info"
        )

        st.success("✅ Message sent to parent successfully.")
# ----------------------------------------------------
# CLASS ANNOUNCEMENT
# ----------------------------------------------------
st.header("📢 Class Announcement")
announcement = st.text_area("Announcement")
if st.button("Publish Announcement"):
    if announcement.strip() == "":
        st.warning("Please enter announcement.")

    else:
        st.success("Announcement Published.")

st.markdown("---")
# ----------------------------------------------------
# TOP PERFORMERS
# ----------------------------------------------------
st.header("🏆 Top Performing Students")
top = pd.DataFrame(
    {
        "Student": [
            "Rahul",
            "Priya",
            "Ankit",
            "Neha",
            "Aman"
        ],
        "Score": [
            96,
            94,
            92,
            91,
            90
        ]
    }
)
st.dataframe(
    top,
    use_container_width=True,
    hide_index=True
)
st.markdown("---")

# ----------------------------------------------------
# SKILL ANALYTICS
# ----------------------------------------------------
st.header("📈 Skill Analytics")
skill_df = pd.DataFrame({
    "Skill": [
        "Python",
        "Artificial Intelligence",
        "Mathematics",
        "Communication",
        "Problem Solving",
        "Leadership"
    ],
    "Average Score": [
        87,
        82,
        90,
        76,
        88,
        79
    ]
})

fig = px.bar(
    skill_df,
    x="Skill",
    y="Average Score",
    color="Average Score",
    text="Average Score",
    color_continuous_scale="Viridis",
    title="Class Skill Performance"
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ----------------------------------------------------
# DOWNLOAD REPORT
# ----------------------------------------------------

st.header("📄 Download Class Report")

report = f"""
TalentSphere Elevate

Teacher Report

Total Students : 120

Average Attendance : 94%

Average Assessment Score : 86%

AI Readiness : 89%

Top Career :
AI Engineer

Generated Successfully.
"""

st.download_button(
    label="📥 Download Report",
    data=report,
    file_name="Teacher_Report.txt",
    mime="text/plain"
)
st.markdown("---")
# ----------------------------------------------------
# TEACHER ACHIEVEMENTS
# ----------------------------------------------------

st.header("🏅 Teacher Achievements")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.success("👨‍🏫 120 Students")

with col2:
    st.success("📚 48 Assessments")

with col3:
    st.success("⭐ 94% Attendance")

with col4:
    st.success("🏆 Excellent Mentor")

st.markdown("---")

# ----------------------------------------------------
# QUICK ACCESS TO AI TOOLS
# ----------------------------------------------------

st.header("🚀 AI Tools")

col1, col2 = st.columns(2)

with col1:

    if st.button("💬 AI Career Coach"):
        st.switch_page("pages/chatbot.py")

    if st.button("📄 Resume Analyzer"):
        st.switch_page("pages/resume_analyzer.py")

    if st.button("📊 Skill Gap Analysis"):
        st.switch_page("pages/skill_gap_analysis.py")

with col2:

    if st.button("🎯 Career Recommendation"):
        st.switch_page("pages/career_recommendation.py")

    if st.button("📚 Learning Roadmap"):
        st.switch_page("pages/learning_roadmap.py")

    if st.button("📈 Dashboard"):
        st.switch_page("pages/dashboard.py")

st.markdown("---")
# ----------------------------------------------------
# TEACHER NOTIFICATIONS
# ----------------------------------------------------

st.markdown("---")
st.header("🔔 Notifications")
notifications = get_notifications(st.session_state.email)
if notifications:

    for notification in notifications:
        message = notification[1]
        notification_type = notification[2]
        created_at = notification[3]
        if notification_type == "success":
            st.success(f"{created_at} : {message}")
        elif notification_type == "warning":
            st.warning(f"{created_at} : {message}")
        else:
            st.info(f"{created_at} : {message}")
else:
    st.info("No notifications available.")
    # ----------------------------------------------------
# AI TEACHER ASSISTANT
# ----------------------------------------------------

st.markdown("---")
st.header("🤖 AI Teacher Assistant")

selected_class = st.selectbox(
    "Select Class",
    ["6", "7", "8", "9", "10", "11", "12"]
)
if st.button("Generate Teaching Activities"):
    with st.spinner("Generating suggestions..."):
        prompt = f"""
You are an experienced school teacher.
Suggest 10 classroom activities to improve
students' problem-solving, logical thinking,
communication, and teamwork.
Class: {selected_class}
Give practical and engaging activities.
"""
        answer = ask_gemini(prompt)
    st.success("Activities Generated Successfully")
    st.markdown(answer)
# ----------------------------------------------------
# FOOTER
# ----------------------------------------------------
st.markdown(
"""
---
<div style="text-align:center; padding:20px;">
<h2>🚀 TalentSphere Elevate</h2>
<h4>Teacher Dashboard</h4>
<p>AI Powered Career Development Platform</p>
<p>Made with ❤️ using Streamlit + Gemini AI</p>
<p>© 2026 TalentSphere Elevate</p>
</div>
""",
unsafe_allow_html=True
)