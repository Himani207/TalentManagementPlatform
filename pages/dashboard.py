import streamlit as st
import pandas as pd
import plotly.express as px
from utils.session import logout

# Check if user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.switch_page("pages/login.py")
if "category" not in st.session_state:
    st.session_state.category = "Student"

# Page Settings
st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

# Header
st.title("📊 TalentSphere Elevate Dashboard")
st.write(f"### Welcome, {st.session_state.name} 👋")

st.markdown("---")

# User Profile
st.subheader("👤 User Profile")

col1, col2 = st.columns(2)

with col1:
    st.info(f"**Name:** {st.session_state.name}")

with col2:
    st.info(f"**Email:** {st.session_state.email}")
st.success(f"Category: {st.session_state.get('category', 'Not Available')}")
st.markdown("---")
# Dashboard Card
st.subheader("📊 Dashboard Overview")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        label="📄 Resume Score",
        value="84",
        delta="+5"
    )

with c2:
    st.metric(
        label="💻 Skill Score",
        value="76",
        delta="+8"
    )

with c3:
    st.metric(
        label="🎯 Placement Readiness",
        value="82%",
        delta="+3%"
    )

st.markdown("---")

# Skill Performance Chart
st.subheader("📈 Skill Performance")

df = pd.DataFrame({
    "Skill": [
        "Python",
        "SQL",
        "Git",
        "AI"
    ],
    "Score": [
        80,
        60,
        50,
        70
    ]
})

fig = px.bar(
    df,
    x="Skill",
    y="Score",
    color="Score",
    text="Score",
    title="Skill Performance"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Dashboard Metrics
st.subheader("📈 Career Progress")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Skill Score", "78%", "+5%")

with c2:
    st.metric("Placement Readiness", "82%", "+3%")

with c3:
    st.metric("Learning Progress", "45%", "+10%")

st.markdown("---")

# Progress Bar
st.subheader("📚 Course Progress")

progress = 45

st.progress(progress)

st.write(f"{progress}% Completed")

st.markdown("---")

# AI Recommendation
st.subheader("🤖 AI Career Recommendation")

st.success("""
Recommended Skills

✔ Python
✔ SQL
✔ Git
✔ Object-Oriented Programming
✔ APIs
✔ Data Structures
""")

st.markdown("---")
# Weekly Goals
st.subheader("🎯 Weekly Goals")
st.checkbox("Complete Python Course")
st.checkbox("Solve 20 Coding Questions")
st.checkbox("Update Resume")
st.checkbox("Practice Aptitude")
st.markdown("---")
# Upcoming Tasks
st.subheader("📅 Upcoming Tasks")
st.write("• Resume Review")
st.write("• Coding Challenge")
st.write("• Mock Interview")
st.write("• Skill Assessment")
st.markdown("---")
# Notifications
st.subheader("🔔 Notifications")
st.info("New Python Course Available")
st.info("Coding Contest on Saturday")
st.info("Resume Score Improved")
st.markdown("---")
st.subheader("🤖 AI Tools")
if st.button("Open AI Career Chatbot"):
    st.switch_page("pages/chatbot.py")

st.subheader("AI Resume")

if st.button("Open Resume Analyzer"):
    st.switch_page("pages/resume_analyzer.py")
st.markdown("---")
st.subheader("🤖 AI Features")

col1, col2 = st.columns(2)

with col1:

    if st.button("🎯 Career Recommendation"):
        st.switch_page("pages/career_recommendation.py")

    if st.button("📊 Skill Gap Analysis"):
        st.switch_page("pages/skill_gap_analysis.py")

with col2:

    if st.button("📚 Learning Roadmap"):
        st.switch_page("pages/learning_roadmap.py")

    if st.button("💬 AI Chatbot"):
        st.switch_page("pages/chatbot.py")


# Logout Button
if st.button("🚪 Logout"):

    logout()

    st.success("Logged Out Successfully")

    st.switch_page("app.py")
    
