import streamlit as st
import pandas as pd
import plotly.express as px
import random
from future_db .teacher_db import add_assessment
from datetime import date
from pathlib import Path
from utils.school_db import save_profile
from utils.session import logout
from ai.gemini import ask_gemini
from data.questions import questions
from utils.school_db import create_student_table

from utils.school_db import (
    save_profile,
    get_student_profile
)

# ----------------------------------------------------
# PAGE CONFIGURATION
# ----------------------------------------------------

st.set_page_config(
    page_title="High School Dashboard",
    page_icon="🏫",
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
if "logged_in" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

if not st.session_state.logged_in:
    st.warning("Please login first.")
    st.stop()
student_profile = get_student_profile(st.session_state.email)

if student_profile is None:
    student_profile = {
        "parent_email": "",
        "age": 15,
        "class": "10",
        "school": "",
        "interests": "",
        "subject": "Mathematics",
        "career": "Software Engineer",
        "goal": ""
    }
# ----------------------------------------------------
# INITIALIZE DASHBOARD VALUES
# ----------------------------------------------------

if "hours" not in st.session_state:
    st.session_state.hours = 0

if "completed" not in st.session_state:
    st.session_state.completed = 0
# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------

logo = Path(__file__).parent.parent / "assets" / "logo.png"

try:
    if logo.exists():
        st.sidebar.image(str(logo), width=130)
except Exception:
    st.sidebar.warning("⚠️ Logo could not be loaded.")

st.sidebar.title("🚀 TalentSphere Elevate")

st.sidebar.markdown("---")

st.sidebar.success(f"👤 {st.session_state.name}")

st.sidebar.info(st.session_state.email)
st.sidebar.markdown("---")
st.sidebar.title("🏫 High School")

if st.sidebar.button("🏠 Dashboard"):
    st.switch_page("pages/school.py")

if st.sidebar.button("👤 Student Profile"):
    st.switch_page("pages/school_profile.py")

if st.sidebar.button("🎯 Career Assessment"):
    st.switch_page("pages/school_career.py")

if st.sidebar.button("📚 Learning Roadmap"):
    st.switch_page("pages/school_roadmap.py")

if st.sidebar.button("📝 Skill Assessment"):
    st.switch_page("pages/school_assessment.py")

if st.sidebar.button("🔔 Notifications"):
    st.switch_page("pages/school_notifications.py")

if st.sidebar.button("🤖 AI Tools"):
    st.switch_page("pages/school_ai_tools.py")

st.sidebar.markdown("---")

if st.sidebar.button("🚪 Logout"):
    logout()
    st.switch_page("app.py")
# ----------------------------------------------------
# HEADER
# ----------------------------------------------------

st.title("🏫 High School Student Dashboard")

st.markdown(
f"""
### Welcome **{st.session_state.name}** 👋

Build your future with the power of Artificial Intelligence.
"""
)

st.info(
"""
🚀 Every expert was once a beginner.

Start learning today to build your dream career.
"""
)

st.markdown("---")
# ----------------------------------------------------
#Dashboard Overview
# ----------------------------------------------------

st.header("📊 Dashboard Analytics")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Career Match", "92%")

with c2:
    st.metric("Learning Progress", "68%")

with c3:
    st.metric("Weekly Study Hours", f"{st.session_state.hours} hrs")

with c4:
    st.metric("Goals Completed", f"{st.session_state.completed}/4")
c5, c6, c7 = st.columns(3)

with c5:
    st.metric("Projects Completed", "4")

with c6:
    st.metric("Certificates Earned", "3")

with c7:
    st.metric("Current Streak", "15 Days 🔥")

st.markdown("---")
# ----------------------------------------------------
# HIGH SCHOOL STUDENT PROFILE
# ----------------------------------------------------

st.header("👤 High School Student Profile")

st.markdown("Complete your profile to receive personalized AI career guidance.")

st.markdown("---")

# ============================
# PERSONAL INFORMATION
# ============================

st.subheader("👤 Personal Information")

col1, col2 = st.columns(2)

with col1:

    full_name = st.text_input(
        "Full Name",
        value=st.session_state.name
    )

    email = st.text_input(
        "Email Address",
        value=st.session_state.email,
        disabled=True
    )
    parent_email = st.text_input(
        "Parent Email",
        value=student_profile["parent_email"]
    )

    phone = st.text_input("Phone Number")
    dob = st.date_input(
    "Date of Birth",
    value=date(2010, 1, 1),
    min_value=date(2000, 1, 1),
    max_value=date.today()
)
    age = st.number_input(
        "Age",
        min_value=10,
        max_value=20,
        value=student_profile["age"]
    )

with col2:

    gender = st.selectbox(
        "Gender",
        ["Male", "Female", "Other"]
    )

    city = st.text_input("City")

    state = st.text_input("State")

    country = st.text_input(
        "Country",
        value="India"
    )

    profile_photo = st.file_uploader(
        "Upload Profile Photo",
        type=["jpg", "jpeg", "png"]
    )

st.markdown("---")

# ============================
# ACADEMIC INFORMATION
# ============================

st.subheader("🎓 Academic Information")

col1, col2 = st.columns(2)

with col1:

    school = st.text_input(
    "School Name",
    value=student_profile["school"]
)
    classes = ["6","7","8","9","10","11","12"]
    class_name = st.selectbox(
    "Class",
    classes,
    index=classes.index(student_profile["class"])
)
   
    board = st.selectbox(
        "Board",
        [
            "CBSE",
            "ICSE",
            "State Board"
        ]
    )

    medium = st.selectbox(
        "Medium of Study",
        [
            "English",
            "Hindi",
            "Other"
        ]
    )

with col2:

    percentage = st.number_input(
        "Current Percentage",
        min_value=0.0,
        max_value=100.0,
        step=0.1
    )
    subjects = [
    "Mathematics",
    "Science",
    "Computer Science",
    "English",
    "Biology",
    "Social Science"
]

    favorite_subject = st.selectbox(
        "Favorite Subject",
    subjects,
    index=subjects.index(student_profile["subject"])
)

    dream_career = st.selectbox(
        "Dream Career",
        [
            "Software Engineer",
            "AI Engineer",
            "Doctor",
            "Data Scientist",
            "IAS Officer",
            "Scientist",
            "Teacher",
            "Business Entrepreneur"
        ]
    )
    
    interests = st.multiselect(
        "🌟 Your Interests",
        [
            "Programming",
            "Artificial Intelligence",
            "Robotics",
            "Mathematics",
            "Science",
            "Technology",
            "Research",
            "Design",
            "Business",
            "Communication",
            "Sports",
            "Creativity"
        ]
    )

    goal = st.text_area(
        "🎯 Career Goal",
        placeholder="Example: I want to become an AI Engineer"
    )

st.markdown("---")


# ----------------------------------------------------
# SAVE PROFILE
# ----------------------------------------------------
if st.button("💾 Save Profile"):

    st.write("Saving profile...")

    save_profile(
        st.session_state.email,
        parent_email,
        age,
        class_name,
        school,
        ",".join(interests),
        favorite_subject,
        dream_career,
        goal
    )

    st.success("Profile Saved!")

    st.success("✅ Profile Saved Successfully!")
    st.rerun()
    st.markdown("---")

# ----------------------------------------------------
# GOAL TRACKER
# ----------------------------------------------------

st.header("🎯 Weekly Goal Tracker")

g1 = st.checkbox("🐍 Learn Python")

g2 = st.checkbox("🤖 Learn AI Basics")

g3 = st.checkbox("📚 Complete Mathematics")

g4 = st.checkbox("💬 Improve Communication Skills")

completed = sum([g1, g2, g3, g4])
st.session_state.completed = completed
progress = completed / 4
st.progress(progress)
st.success(f"Completed {completed} out of 4 Goals")
if completed == 4:
    st.balloons()
    st.success("🏆 Congratulations! Weekly Goals Completed.")

st.markdown("---")
#-------------------------------------------------
#Weekly Hours
#-------------------------------------------------
st.header("⏰ Weekly Study Hours")
hours = st.slider(
    "Hours Studied",
    0,
    40,
    st.session_state.hours
)
st.session_state.hours = hours
st.metric("Study Hours", hours)
if hours >= 20:
    st.success("Excellent consistency!")
# ----------------------------------------------------
# STUDENT SUMMARY
# ----------------------------------------------------

st.header("📋 Student Summary")

summary = pd.DataFrame(
    {
        "Field": [
            "Age",
            "Class",
            "School",
            "Favorite Subject",
            "Dream Career"
        ],
        "Value": [
            age,
            class_name,
            school if school else "-",
            favorite_subject,
            dream_career
        ]
    }
)

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")
# ----------------------------------------------------
# CAREER INTEREST ASSESSMENT
# ----------------------------------------------------

st.header("🎯 Career Interest Assessment")

career_score = {
    "Technology": 0,
    "Engineering": 0,
    "Healthcare": 0,
    "Design": 0,
    "Business": 0
}

q1 = st.radio(
    "1. Which activity do you enjoy the most?",
    [
        "Solving coding problems",
        "Drawing designs",
        "Helping people",
        "Building machines",
        "Selling products"
    ]
)

if q1 == "Solving coding problems":
    career_score["Technology"] += 20

elif q1 == "Drawing designs":
    career_score["Design"] += 20

elif q1 == "Helping people":
    career_score["Healthcare"] += 20

elif q1 == "Building machines":
    career_score["Engineering"] += 20

else:
    career_score["Business"] += 20


q2 = st.radio(
    "2. Which subject do you like most?",
    [
        "Mathematics",
        "Physics",
        "Biology",
        "Computer Science",
        "Commerce"
    ]
)

if q2 == "Mathematics":
    career_score["Technology"] += 20
    career_score["Engineering"] += 20

elif q2 == "Physics":
    career_score["Engineering"] += 20

elif q2 == "Biology":
    career_score["Healthcare"] += 20

elif q2 == "Computer Science":
    career_score["Technology"] += 20

else:
    career_score["Business"] += 20


q3 = st.radio(
    "3. What would you like to create?",
    [
        "AI Software",
        "Robot",
        "Hospital",
        "Fashion Brand",
        "Startup"
    ]
)

if q3 == "AI Software":
    career_score["Technology"] += 30

elif q3 == "Robot":
    career_score["Engineering"] += 30

elif q3 == "Hospital":
    career_score["Healthcare"] += 30

elif q3 == "Fashion Brand":
    career_score["Design"] += 30

else:
    career_score["Business"] += 30


if st.button("Analyze Career Interest"):

    result = pd.DataFrame({
        "Career Domain": list(career_score.keys()),
        "Score": list(career_score.values())
    })

    st.dataframe(result, use_container_width=True)
    fig = px.bar(
        result,
        x="Career Domain",
        y="Score",
        color="Score",
        text="Score",
        color_continuous_scale="Viridis",
        title="Career Interest Score"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        height=450
    )

    fig.update_traces(textposition="outside")

    st.plotly_chart(fig, use_container_width=True)

    best_career = max(career_score, key=career_score.get)

    st.success(f"🏆 Best Career Match : {best_career}")
# ----------------------------------------------------
# PERSONALITY ANALYSIS
# ----------------------------------------------------

st.header("🧠 Personality & Aptitude Analysis")

personality = pd.DataFrame({

    "Skill":[
        "Logical Thinking",
        "Problem Solving",
        "Creativity",
        "Leadership",
        "Communication",
        "Teamwork"
    ],

    "Score":[
        95,
        91,
        78,
        82,
        70,
        86
    ]

})

fig = px.bar(
    personality,
    x="Skill",
    y="Score",
    color="Score",
    text="Score",
    color_continuous_scale="Viridis"
)

fig.update_layout(
    template="plotly_white",
    title="Personality & Aptitude Analysis",
    title_x=0.5
)
st.plotly_chart(fig,use_container_width=True)
# -----------------------------
# YOUR STRENGTHS
# -----------------------------
st.header("⭐ Your Strengths")

st.success("""
✔ Strong Logical Thinking

✔ Excellent Mathematics

✔ Technology Interest

✔ Good Problem Solving

✔ Fast Learner
""")
# ----------------------------------------------------
# AI READINESS SCORE
# ----------------------------------------------------

st.header("🤖 AI Readiness Score")
score = 89
st.metric(
    "Overall Score",
    f"{score}%"
)

st.progress(score / 100)

if score > 85:
    st.success("🚀 Excellent AI Career Potential!")

elif score > 70:
    st.info("👍 Good Progress")

else:
    st.warning("📚 Need More Practice")
# ----------------------------------------------------
# AREAS TO IMPROVE
# ----------------------------------------------------

st.header("📈 Areas to Improve")

st.warning("""
• Communication

• Public Speaking

• Leadership

• Team Collaboration
""")

# ----------------------------------------------------
# AI CAREER RECOMMENDATION
# ----------------------------------------------------

st.header("🤖 AI Career Recommendation")

st.write("Generate personalized career guidance using Gemini AI.")
# ----------------------------------------------------
# TOP CAREER RECOMMENDATION
# ----------------------------------------------------

st.header("💼 Top Career Recommendations")

career_df = pd.DataFrame({
    "Career": [
        "AI Engineer",
        "Software Developer",
        "Robotics Engineer",
        "Data Scientist"
    ],
    "Match %": [
        95,
        92,
        88,
        84
    ]
})

st.dataframe(career_df, use_container_width=True)
#-------------------------------------------------
# Career Match Pie Chart 
#-------------------------------------------------
fig = px.pie(
    career_df,
    names="Career",
    values="Match %",
    hole=0.4,
    title="Career Match Distribution"
)

st.plotly_chart(fig, use_container_width=True)

st.info("""
### Why these careers?

✔ Strong Mathematics

✔ Excellent Logical Thinking

✔ Technology Interest

✔ Good Problem Solving
""")

# ----------------------------------------------------
# GEMINI AI RECOMMENDATION
# ----------------------------------------------------

if st.button("🚀 Generate AI Recommendation"):

    with st.spinner("Analyzing your profile..."):

        prompt = f"""
You are an expert career counselor.

Student Details

Age: {age}
Class: {class_name}
School: {school}
Favorite Subject: {favorite_subject}
Interests: {interests}
Dream Career: {dream_career}
Goal: {goal}

Provide:

1. Best Career
2. Skills Required
3. Learning Roadmap
4. Best Courses
5. Future Scope
6. Motivation
"""

        answer = ask_gemini(prompt)
    st.success("✅ Recommendation Generated Successfully")
    st.markdown(answer)

st.markdown("---")

# ----------------------------------------------------
# FUTURE SKILLS ROADMAP
# -----------------------------------------------

st.header("🚀 Future Skills Roadmap")

st.write("Click any skill to explore its roadmap and career opportunities.")

col1, col2 = st.columns(2)

# ---------------- LEFT COLUMN ---------------- #

with col1:

    if st.button("🐍 Python Programming"):

        st.success("🐍 Python Programming")

        st.markdown("""
### 📖 Introduction
Python is one of the easiest and most popular programming languages.

### 📚 Learning Roadmap
- ✅ Python Basics
- ✅ Variables & Data Types
- ✅ Loops & Functions
- ✅ Object-Oriented Programming (OOP)
- ✅ File Handling
- ✅ Exception Handling
- ✅ Build Projects
- ✅ Learn AI & Machine Learning

### 💼 Career Opportunities
- Python Developer
- Software Engineer
- Data Analyst
- AI Engineer

### 🌐 Free Resources
- Python Official Documentation
- W3Schools
- GeeksforGeeks
- freeCodeCamp
""")

    if st.button("🤖 Artificial Intelligence"):

        st.success("🤖 Artificial Intelligence")

        st.markdown("""
### 📖 Introduction
Artificial Intelligence enables machines to think and solve problems.

### 📚 Learning Roadmap
- ✅ Python
- ✅ Mathematics
- ✅ Machine Learning
- ✅ Deep Learning
- ✅ Neural Networks

### 💼 Career Opportunities
- AI Engineer
- AI Researcher
- Robotics Engineer
- NLP Engineer
""")

    if st.button("🧠 Machine Learning"):

        st.success("🧠 Machine Learning")

        st.markdown("""
### 📖 Introduction
Machine Learning helps computers learn from data.

### 📚 Learning Roadmap
- ✅ Python
- ✅ Statistics
- ✅ NumPy & Pandas
- ✅ Scikit-Learn
- ✅ Projects

### 💼 Career Opportunities
- Machine Learning Engineer
- Data Scientist
- AI Engineer
""")

    if st.button("📊 Data Science"):

        st.success("📊 Data Science")

        st.markdown("""
### 📖 Introduction
Data Science helps extract meaningful insights from data.

### 📚 Learning Roadmap
- ✅ Python
- ✅ SQL
- ✅ Excel
- ✅ Power BI
- ✅ Data Visualization

### 💼 Career Opportunities
- Data Scientist
- Business Analyst
- Data Analyst
""")

# ---------------- RIGHT COLUMN ---------------- #

with col2:

    if st.button("💬 Communication"):

        st.success("💬 Communication Skills")

        st.markdown("""
### Importance
Good communication improves confidence and teamwork.

### Improve By
- Reading Books
- Public Speaking
- Group Discussions
- Presentations
""")

    if st.button("🧩 Problem Solving"):

        st.success("🧩 Problem Solving")

        st.markdown("""
### Improve By
- Coding Practice
- Aptitude Questions
- Logical Reasoning
- Competitive Programming

### Platforms
- LeetCode
- HackerRank
- CodeChef
""")

    if st.button("🌐 Web Development"):

        st.success("🌐 Web Development")

        st.markdown("""
### Learning Roadmap
- HTML
- CSS
- JavaScript
- Python
- Streamlit
- Django / Flask

### Career Opportunities
- Frontend Developer
- Backend Developer
- Full Stack Developer
""")

    if st.button("👨‍💼 Leadership"):

        st.success("👨‍💼 Leadership")

        st.markdown("""
### Importance
Leadership helps manage teams and projects effectively.

### Improve By
- Team Projects
- Volunteering
- Decision Making
- Time Management

### Career Benefits
- Team Lead
- Project Manager
- Entrepreneur
""")

st.markdown("---")
st.header("🗓 Personalized Learning Timeline")

timeline = {
    "Class 10": [
        "Python Basics",
        "Mathematics",
        "Scratch Programming"
    ],
    "Class 11": [
        "Intermediate Python",
        "Statistics",
        "Mini Projects"
    ],
    "Class 12": [
        "Data Structures",
        "Machine Learning",
        "Portfolio"
    ]
}

for year, items in timeline.items():
    with st.expander(year):
        for item in items:
            st.write("✅", item)
# ----------------------------------------------------
# LEARNING VIDEOS
# ----------------------------------------------------

st.markdown("---")

st.header("🎥 Learning Videos")

st.write("Watch recommended videos to improve your skills.")

video_category = st.selectbox(
    "Choose Topic",
    [
        "Python Programming",
        "Artificial Intelligence",
        "Machine Learning",
        "Web Development",
        "Communication Skills"
    ]
)


videos = {
    "Python Programming":
    "https://www.youtube.com/embed/rfscVS0vtbw",

    "Artificial Intelligence":
    "https://www.youtube.com/embed/ad79nYk2keg",

    "Machine Learning":
    "https://www.youtube.com/embed/GwIo3gDZCVQ",

    "Web Development":
    "https://www.youtube.com/embed/UB1O30fR-EE",

    "Communication Skills":
    "https://www.youtube.com/embed/HAnw168huqA"
}


st.video(videos[video_category])
# ----------------------------------------------------
# ASSESSMENT QUESTIONS
# ----------------------------------------------------
st.header("📝 Skill Assessment")

# Keep the same questions until the user starts a new assessment
if "selected_questions" not in st.session_state:
    st.session_state.selected_questions = random.sample(
        questions,
        min(10, len(questions))
    )

selected_questions = st.session_state.selected_questions

score = 0

for i, q in enumerate(selected_questions):

    st.subheader(f"Q{i+1}. {q['question']}")

    answer = st.radio(
        "Choose Answer",
        q["options"],
        key=f"quiz_{i}"
    )

    if answer == q["answer"]:
        score += 1

if st.button("Submit Assessment"):
    st.success(f"🎉 Your Score: {score}/{len(selected_questions)}")
    # Save assessment in database
    add_assessment(
        st.session_state.email,
        "Python Assessment",
        score
    )
    
    quiz_percentage = (score / len(selected_questions)) * 100

    st.progress(quiz_percentage / 100)

    st.metric("Quiz Percentage", f"{quiz_percentage:.1f}%")

    if quiz_percentage >= 80:
        st.success("🌟 Excellent Performance!")

    elif quiz_percentage >= 60:
        st.info("👍 Good Job! Keep Practicing.")

    else:
        st.warning("📚 Keep Learning!")

    st.markdown("---")
    st.subheader("📖 Study Recommendations")

    if quiz_percentage < 60:
        st.write("• Revise Python Basics")
        st.write("• Practice Mathematics")
        st.write("• Learn AI Fundamentals")
        st.write("• Improve Logical Reasoning")
        st.write("• Practice Communication Skills")

    else:
        st.write("• Start Machine Learning")
        st.write("• Build Mini Projects")
        st.write("• Practice Coding Daily")
if st.button("🔄 New Assessment"):
    st.session_state.selected_questions = random.sample(
        questions,
        min(10, len(questions))
    )

    # Clear previous answers
    for i in range(10):
        st.session_state.pop(f"quiz_{i}", None)

    st.rerun()
#----------------------------------------------------
#Certifications and Badges
#----------------------------------------------------
st.markdown("---")
st.header("🏅 Certificates & Badges")

badges = [
    "🐍 Python Beginner",
    "🤖 AI Explorer",
    "🧠 Logic Master",
    "⚡ Fast Learner",
    "📚 Consistent Student"
]

cols = st.columns(len(badges))

for col, badge in zip(cols, badges):
    with col:
        st.success(badge)
# ----------------------------------------------------
# SKILL PROGRESS CHART
# ----------------------------------------------------

st.header("📈 Skill Progress")

df = pd.DataFrame({
    "Skill": [
        "Python",
        "Mathematics",
        "Communication",
        "Artificial Intelligence",
        "Problem Solving",
        "Leadership"
    ],
    "Score": [
        80,
        75,
        65,
        60,
        78,
        70
    ]
})

fig = px.bar(
    df,
    x="Skill",
    y="Score",
    color="Score",
    text="Score",
    color_continuous_scale="Viridis",
    title="Current Skill Levels"
)

fig.update_layout(
    template="plotly_white",
    height=450,
    title_x=0.5
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")

# ----------------------------------------------------
# LEARNING DISTRIBUTION
# ----------------------------------------------------

st.header("📊 Learning Distribution")

pie = px.pie(
    names=[
        "Programming",
        "AI",
        "Math",
        "Communication"
    ],
    values=[
        40,
        25,
        20,
        15
    ],
    hole=0.5
)

pie.update_layout(
    template="plotly_white"
)

st.plotly_chart(
    pie,
    use_container_width=True
)

st.markdown("---")
st.header("🔥 Today's Challenge")

challenge = random.choice([
    "Solve 5 Python questions.",
    "Learn one new AI concept.",
    "Read for 30 minutes.",
    "Complete one coding challenge.",
    "Practice logical reasoning for 20 minutes."
])

st.info(challenge)

# ----------------------------------------------------
# DAILY MOTIVATION
# ----------------------------------------------------

st.header("💡 Daily Motivation")

st.info(
"""
🌟 Success doesn't come from what you do occasionally.

It comes from what you do consistently.

Keep Learning 🚀
"""
)

st.markdown("---")

# ----------------------------------------------------
# AI TOOLS
# ----------------------------------------------------

st.header("🤖 AI Career Tools")

col1, col2 = st.columns(2)

with col1:

    st.info("💬 AI Career Coach")

    if st.button("Open AI Career Coach", key="chatbot"):
        st.switch_page("pages/chatbot.py")

    st.info("📄 AI Resume Analyzer")

    if st.button("Open Resume Analyzer", key="resume"):
        st.switch_page("pages/resume_analyzer.py")

    st.info("📊 Skill Gap Analysis")

    if st.button("Open Skill Gap Analysis", key="skillgap"):
        st.switch_page("pages/skill_gap_analysis.py")

with col2:

    st.info("🎯 Career Recommendation")

    if st.button("Open Career Recommendation", key="career"):
        st.switch_page("pages/career_recommendation.py")

    st.info("📚 Learning Roadmap")

    if st.button("Open Learning Roadmap", key="roadmap"):
        st.switch_page("pages/learning_roadmap.py")

    st.info("📈 Dashboard")

    if st.button("Open Dashboard", key="dashboard"):
        st.switch_page("pages/dashboard.py")

st.markdown("---")

# ----------------------------------------------------
# FOOTER
# ----------------------------------------------------

st.markdown(
"""
---
<div style="text-align:center; padding:20px;">

### 🚀 TalentSphere Elevate

AI-Powered Career Development Platform

Made with ❤️ using Streamlit + Gemini AI

© 2026 TalentSphere Elevate

</div>
""",
unsafe_allow_html=True
)
