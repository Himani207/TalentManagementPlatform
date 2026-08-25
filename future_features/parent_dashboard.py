import streamlit as st
import pandas as pd
import plotly.express as px
from utils.notification_db import get_notifications, add_notification
from pathlib import Path
from utils.session import logout
from utils.school_db import get_student_by_parent
#page configuration
st.set_page_config(
    page_title="Parent Dashboard",
    page_icon="👨‍👩‍👧",
    layout="wide"
)

#load css
css_file = Path(__file__).parent.parent / "assets" / "style.css"

if css_file.exists():
    with open(css_file) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
if (
    "logged_in" not in st.session_state
    or not st.session_state.logged_in
):
    st.warning("Please login first.")
    st.stop()
st.sidebar.title("👨‍👩‍👧 Parent Dashboard")
st.sidebar.success(st.session_state.name)

if st.sidebar.button("Logout"):
    logout()
    st.switch_page("app.py")
st.title("👨‍👩‍👧 Parent Dashboard")
st.info("""
Monitor your child's academic progress,
career readiness, and learning habits.
""")
student = get_student_by_parent(st.session_state.email)
if student is None:
    st.error("❌ Student profile not found.")
    st.info("Please ask the student to complete the profile first.")
    st.stop()
st.header("👤 Student Overview")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Class", student["class"])

with c2:
    st.metric("Age", student["age"])

with c3:
    st.metric("Dream Career", student["career"])

c4, c5, c6 = st.columns(3)

with c4:
    st.metric("School", student["school"])

with c5:
    st.metric("Favorite Subject", student["subject"])

with c6:
    st.metric("Interests", len(student["interests"].split(",")))

# ----------------------------------------------------   
#Student details
# ----------------------------------------------------
st.header("📋 Student Details")

st.write("**School:**", student["school"])
st.write("**Favorite Subject:**", student["subject"])
st.write("**Interests:**", student["interests"])
st.write("**Career Goal:**", student["goal"])

# ----------------------------------------------------
# ACADEMIC PROGRESS
# ----------------------------------------------------

st.header("📚 Academic Progress")
progress = pd.DataFrame({
    "Subject":[
        "Math",
        "Science",
        "English",
        "Computer"
    ],
    "Marks":[
        88,
        79,
        83,
        94
    ]
})

fig = px.bar(
    progress,
    x="Subject",
    y="Marks",
    color="Marks",
    text="Marks"
)

st.plotly_chart(fig,use_container_width=True)
st.header("🎯 Goal Progress")

st.progress(0.75)

st.success("3 of 4 Weekly Goals Completed")
st.header("🏫 Attendance")

st.metric(
    "Attendance",
    "94%"
)
st.header("⏰ Weekly Study Hours")

hours = 18

st.metric(
    "Hours",
    f"{hours} hrs"
)
st.header("🤖 AI Readiness")

score = 89

st.metric(
    "AI Readiness",
    f"{score}%"
)

st.progress(score/100)
st.header("📝 Assessment Results")

assessment = pd.DataFrame({

    "Quiz":[
        "Python",
        "Math",
        "AI"
    ],

    "Score":[
        90,
        82,
        88
    ]
})

st.dataframe(assessment,use_container_width=True)
st.header("💼 Career Recommendation")

st.success("""
Recommended Career

✔ AI Engineer

✔ Software Developer

✔ Data Scientist
""")
st.header("👨‍👩‍👧 Suggestions for Parents")

st.info("""
✔ Encourage daily study.

✔ Limit screen time.

✔ Appreciate achievements.

✔ Help with homework.

✔ Support career goals.

✔ Motivate project building.
""")
# ----------------------------------------------------
# Teacher Communication
# ----------------------------------------------------
st.header("📨 Teacher Communication")
message = st.text_area("Message to Teacher")

teacher_email = "himaniu454@gmail.com"   # change with actual teacher email)
if st.button("Send Message"):

    if message.strip() == "":
        st.warning("Please enter a message.")

    else:

        add_notification(
            teacher_email,
            f"New message from parent {st.session_state.name}: {message}",
            "info"
        )

        st.success("Message sent to teacher successfully.")
# ----------------------------------------------------
# Notifications
# ----------------------------------------------------
st.header("🔔 Notifications")
notifications = get_notifications(st.session_state.email)
if notifications:
    for notification in notifications:

        message = notification[1]
        notification_type = notification[2]
        created_at = notification[3]


        if notification_type == "success":

            st.success(
                f"{created_at} : {message}"
            )

        elif notification_type == "warning":

            st.warning(
                f"{created_at} : {message}"
            )

        else:

            st.info(
                f"{created_at} : {message}"
            )

else:
    st.info("No notifications available.")
# ----------------------------------------------------
# DOWNLOAD STUDENT REPORT
# ----------------------------------------------------
st.header("📄 Download Student Report")

report = f"""
Student Report

Name : {st.session_state.name}
Age : {student['age']}
Class : {student['class']}
School : {student['school']}
Favorite Subject : {student['subject']}
Dream Career : {student['career']}
Career Goal : {student['goal']}

Attendance : 94%
Weekly Study Hours : 18 hrs
AI Readiness : 89%
"""

st.download_button(
    label="📄 Download Student Report",
    data=report,
    file_name="Student_Report.txt",
    mime="text/plain"
)
# ----------------------------------------------------
# Footer
# ----------------------------------------------------
st.markdown("---")
st.markdown(
    """
---
<div style="text-align:center">
<h3>🚀 TalentSphere Elevate</h3>
<p>parent Dashboard</p>
<p>Made with ❤️ using Streamlit</p>

</div>
""",
    unsafe_allow_html=True
)