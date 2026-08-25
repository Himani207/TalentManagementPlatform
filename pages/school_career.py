import streamlit as st

from utils.session import logout

from utils.school_db import (
    create_student_table,
    create_report_table,
    create_learning_progress_table,
    create_certificate_table,
    create_notification_table,
    get_student_profile,
    get_latest_assessment,
    save_assessment_score,
    get_career_match,
)


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Career Assessment",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# CREATE DATABASE TABLES
# ==========================================================

create_student_table()
create_report_table()
create_learning_progress_table()
create_certificate_table()
create_notification_table()


# ==========================================================
# LOGIN CHECK
# ==========================================================

if "logged_in" not in st.session_state or not st.session_state.logged_in:

    st.warning("Please login first.")

    st.switch_page("pages/login.py")

    st.stop()


email = st.session_state.email


# ==========================================================
# LOAD STUDENT PROFILE
# ==========================================================

student_profile = get_student_profile(email)

if student_profile is None:

    student_profile = {
        "email": email,
        "parent_email": "",
        "age": "",
        "class": "",
        "school": "",
        "interests": "",
        "subject": "",
        "career": "",
        "goal": ""
    }


student_name = st.session_state.get(
    "name",
    email.split("@")[0].title()
)


# ==========================================================
# CURRENT ASSESSMENT
# ==========================================================

latest_score = get_latest_assessment(email)


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
    <style>

    .welcome-card {
        padding: 25px;
        border-radius: 18px;
        margin-bottom: 25px;
        background: linear-gradient(
            135deg,
            rgba(102, 126, 234, 0.15),
            rgba(118, 75, 162, 0.10)
        );
        border: 1px solid rgba(128, 128, 128, 0.18);
    }

    .welcome-card h1 {
        margin-bottom: 8px;
    }

    .welcome-card p {
        font-size: 16px;
        margin-bottom: 0;
    }

    .metric-card {
        padding: 22px;
        border-radius: 18px;
        text-align: center;
        min-height: 150px;
        border: 1px solid rgba(128, 128, 128, 0.18);
        background: rgba(255, 255, 255, 0.05);
    }

    .metric-card h1,
    .metric-card h2,
    .metric-card h3 {
        margin: 5px;
    }

    .metric-card p {
        margin-top: 8px;
        opacity: 0.75;
    }

    .career-card {
        padding: 25px;
        border-radius: 18px;
        text-align: center;
        border: 1px solid rgba(128, 128, 128, 0.18);
        background: rgba(255, 255, 255, 0.05);
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

left, right = st.columns([6, 1])

with left:

    st.markdown(
        f"""
        <div class="welcome-card">
          <h1>🎯 Career Interest Assessment</h1>
          <p>
            Welcome, {student_name} 👋
          </p>
          <p>
            Explore your interests, personality and aptitude
            to discover suitable career domains.
          </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with right:

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        logout()

        st.switch_page("app.py")


# ==========================================================
# STUDENT PROFILE SUMMARY
# ==========================================================

st.subheader("👤 Your Profile")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.info(
        f"🏫 Class: {student_profile.get('class') or 'Not selected'}"
    )


with c2:

    st.info(
        f"📚 Subject: {student_profile.get('subject') or 'Not selected'}"
    )


with c3:

    st.info(
        f"🎯 Goal: {student_profile.get('career') or 'Not selected'}"
    )


with c4:

    st.info(
        f"📊 Previous Score: {latest_score}%"
    )


# ==========================================================
# CAREER INTEREST QUESTIONS
# ==========================================================

st.divider()

st.header("1️⃣ Career Interest Assessment")

st.write(
    "Choose the option that best describes your interest."
)


# ----------------------------------------------------------
# Question 1
# ----------------------------------------------------------

q1 = st.radio(
    "1. Which activity do you enjoy most?",
    [
        "Solving puzzles",
        "Drawing designs",
        "Helping people",
        "Building things"
    ],
    key="career_q1"
)


# ----------------------------------------------------------
# Question 2
# ----------------------------------------------------------

q2 = st.radio(
    "2. What would you like to create?",
    [
        "Mobile App",
        "Machine",
        "Artwork",
        "Business"
    ],
    key="career_q2"
)


# ----------------------------------------------------------
# Question 3
# ----------------------------------------------------------

q3 = st.radio(
    "3. Which subject excites you the most?",
    [
        "Mathematics",
        "Physics",
        "Biology",
        "Computer Science"
    ],
    key="career_q3"
)


# ----------------------------------------------------------
# Question 4
# ----------------------------------------------------------

q4 = st.radio(
    "4. Which type of work sounds most interesting?",
    [
        "Working with computers",
        "Designing and creating",
        "Helping and caring for people",
        "Managing a business"
    ],
    key="career_q4"
)


# ----------------------------------------------------------
# Question 5
# ----------------------------------------------------------

q5 = st.radio(
    "5. Which problem would you like to solve?",
    [
        "Technology problems",
        "Engineering problems",
        "Health problems",
        "Business problems"
    ],
    key="career_q5"
)


# ==========================================================
# PERSONALITY & APTITUDE
# ==========================================================

st.divider()

st.header("2️⃣ Personality & Aptitude Analysis")

st.write(
    "Rate each statement from 1 to 5."
)

st.caption(
    "1 = Strongly Disagree    |    5 = Strongly Agree"
)


# ----------------------------------------------------------
# Personality Questions
# ----------------------------------------------------------

p1 = st.slider(
    "1. I enjoy solving logical problems.",
    1,
    5,
    3,
    key="personality_q1"
)


p2 = st.slider(
    "2. I enjoy creating new and original ideas.",
    1,
    5,
    3,
    key="personality_q2"
)


p3 = st.slider(
    "3. I can communicate my ideas clearly.",
    1,
    5,
    3,
    key="personality_q3"
)


p4 = st.slider(
    "4. I enjoy finding solutions to difficult problems.",
    1,
    5,
    3,
    key="personality_q4"
)


p5 = st.slider(
    "5. I enjoy working with a team and taking responsibility.",
    1,
    5,
    3,
    key="personality_q5"
)


# ==========================================================
# CALCULATE CAREER DOMAIN SCORES
# ==========================================================

if st.button(
    "🚀 Analyze My Career Profile",
    use_container_width=True,
    type="primary"
):

    # ------------------------------------------------------
    # Initial scores
    # ------------------------------------------------------

    scores = {
        "Technology": 0,
        "Engineering": 0,
        "Design": 0,
        "Healthcare": 0,
        "Business": 0
    }


    # ------------------------------------------------------
    # Question 1 scoring
    # ------------------------------------------------------

    if q1 == "Solving puzzles":

        scores["Technology"] += 25
        scores["Engineering"] += 20

    elif q1 == "Drawing designs":

        scores["Design"] += 25

    elif q1 == "Helping people":

        scores["Healthcare"] += 25

    elif q1 == "Building things":

        scores["Engineering"] += 25
        scores["Technology"] += 10


    # ------------------------------------------------------
    # Question 2 scoring
    # ------------------------------------------------------

    if q2 == "Mobile App":

        scores["Technology"] += 25

    elif q2 == "Machine":

        scores["Engineering"] += 25

    elif q2 == "Artwork":

        scores["Design"] += 25

    elif q2 == "Business":

        scores["Business"] += 25


    # ------------------------------------------------------
    # Question 3 scoring
    # ------------------------------------------------------

    if q3 == "Mathematics":

        scores["Technology"] += 10
        scores["Engineering"] += 15
        scores["Business"] += 5

    elif q3 == "Physics":

        scores["Engineering"] += 20

    elif q3 == "Biology":

        scores["Healthcare"] += 25

    elif q3 == "Computer Science":

        scores["Technology"] += 25


    # ------------------------------------------------------
    # Question 4 scoring
    # ------------------------------------------------------

    if q4 == "Working with computers":

        scores["Technology"] += 25

    elif q4 == "Designing and creating":

        scores["Design"] += 25

    elif q4 == "Helping and caring for people":

        scores["Healthcare"] += 25

    elif q4 == "Managing a business":

        scores["Business"] += 25


    # ------------------------------------------------------
    # Question 5 scoring
    # ------------------------------------------------------

    if q5 == "Technology problems":

        scores["Technology"] += 25

    elif q5 == "Engineering problems":

        scores["Engineering"] += 25

    elif q5 == "Health problems":

        scores["Healthcare"] += 25

    elif q5 == "Business problems":

        scores["Business"] += 25


    # ------------------------------------------------------
    # Normalize career scores
    # ------------------------------------------------------

    max_score = max(scores.values())

    if max_score == 0:

        max_score = 1


    # Convert to percentage
    career_percentages = {}

    for career, score in scores.items():

        career_percentages[career] = min(
            100,
            int((score / 125) * 100)
        )


    # ------------------------------------------------------
    # Personality scores
    # ------------------------------------------------------

    logical = int((p1 / 5) * 100)

    creativity = int((p2 / 5) * 100)

    communication = int((p3 / 5) * 100)

    problem_solving = int((p4 / 5) * 100)

    teamwork = int((p5 / 5) * 100)

    leadership = int(
        ((p3 + p5) / 10) * 100
    )


    personality_scores = {

        "Logical Thinking": logical,

        "Creativity": creativity,

        "Communication": communication,

        "Problem Solving": problem_solving,

        "Teamwork": teamwork,

        "Leadership": leadership
    }


    # ------------------------------------------------------
    # Best career domain
    # ------------------------------------------------------

    best_domain = max(
        career_percentages,
        key=career_percentages.get
    )


    best_domain_score = career_percentages[
        best_domain
    ]


    # ------------------------------------------------------
    # Career recommendation
    # ------------------------------------------------------

    career_recommendations = {

        "Technology": "AI & Software Engineering",

        "Engineering": "Engineering & Robotics",

        "Design": "UI/UX & Creative Design",

        "Healthcare": "Medicine & Healthcare",

        "Business": "Business & Entrepreneurship"
    }


    recommended_career = career_recommendations.get(
        best_domain,
        "Career Exploration"
    )


    # ------------------------------------------------------
    # Overall assessment score
    # ------------------------------------------------------

    personality_average = int(
        sum(personality_scores.values())
        / len(personality_scores)
    )


    overall_score = int(
        (best_domain_score * 0.60)
        +
        (personality_average * 0.40)
    )


    overall_score = max(
        0,
        min(100, overall_score)
    )


    # ------------------------------------------------------
    # Save score
    # ------------------------------------------------------

    save_assessment_score(
        email,
        overall_score
    )


    # ------------------------------------------------------
    # Save results in session
    # ------------------------------------------------------

    st.session_state["career_scores"] = career_percentages

    st.session_state["personality_scores"] = personality_scores

    st.session_state["best_domain"] = best_domain

    st.session_state["best_domain_score"] = best_domain_score

    st.session_state["recommended_career"] = recommended_career

    st.session_state["overall_assessment_score"] = overall_score

    st.success(
        "✅ Career assessment completed successfully!"
    )


# ==========================================================
# SHOW RESULTS
# ==========================================================

if "career_scores" in st.session_state:

    career_scores = st.session_state["career_scores"]

    personality_scores = st.session_state[
        "personality_scores"
    ]

    best_domain = st.session_state[
        "best_domain"
    ]

    best_domain_score = st.session_state[
        "best_domain_score"
    ]

    recommended_career = st.session_state[
        "recommended_career"
    ]

    overall_score = st.session_state[
        "overall_assessment_score"
    ]


    # ======================================================
    # CAREER DOMAIN RESULTS
    # ======================================================

    st.divider()

    st.header("📊 Career Domain Analysis")

    st.write(
        "Your responses indicate the following career interests:"
    )


    # Display each career score

    for career, score in sorted(
        career_scores.items(),
        key=lambda item: item[1],
        reverse=True
    ):

        st.write(
            f"**{career}: {score}%**"
        )

        st.progress(
            score / 100
        )


    # ======================================================
    # BEST CAREER MATCH
    # ======================================================

    st.divider()

    st.header("🏆 Best Career Match")

    st.markdown(
        f"""
        <div class="career-card">
          <h1>🎯 {recommended_career}</h1>
          <h2>{best_domain_score}%</h2>
          <p>
            Best matching career domain:
            <b>{best_domain}</b>
          </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ======================================================
    # PERSONALITY RESULTS
    # ======================================================

    st.header("🧠 Personality & Aptitude Analysis")

    personality_columns = st.columns(3)

    items = list(
        personality_scores.items()
    )


    for index, (skill, score) in enumerate(items):

        column = personality_columns[
            index % 3
        ]

        with column:

            st.markdown(
                f"""
                <div class="metric-card">
                  <h3>{skill}</h3>
                  <h1>{score}%</h1>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress(
                score / 100
            )


    # ======================================================
    # OVERALL SCORE
    # ======================================================

    st.divider()

    st.header("📝 Overall Assessment")

    score_col1, score_col2, score_col3 = st.columns(3)


    with score_col1:

        st.metric(
            "Assessment Score",
            f"{overall_score}%"
        )


    with score_col2:

        st.metric(
            "Best Domain",
            best_domain
        )


    with score_col3:

        st.metric(
            "Career Match",
            f"{best_domain_score}%"
        )


    # ======================================================
    # GUIDANCE
    # ======================================================

    st.divider()

    st.header("💡 Career Guidance")


    if overall_score >= 80:

        st.success(
            f"""
            🌟 Excellent career alignment!

            Your responses strongly indicate an interest
            in **{recommended_career}**.

            Continue developing your technical,
            academic and problem-solving skills.
            """
        )


    elif overall_score >= 60:

        st.info(
            f"""
            👍 Good career alignment!

            **{recommended_career}** appears to be a
            promising direction for you.

            Explore projects, courses and activities
            related to this field.
            """
        )


    elif overall_score >= 40:

        st.warning(
            f"""
            📚 You are still exploring your interests.

            **{recommended_career}** may be worth exploring.

            Try different subjects, projects and activities
            before making a final career decision.
            """
        )


    else:

        st.info(
            """
            💡 Your interests are still developing.

            Explore different subjects, hobbies and
            career areas to discover what you enjoy most.
            """
        )


    # ======================================================
    # PERSONALITY HIGHLIGHT
    # ======================================================

    strongest_personality = max(
        personality_scores,
        key=personality_scores.get
    )

    strongest_score = personality_scores[
        strongest_personality
    ]


    st.subheader("⭐ Your Strongest Trait")

    st.info(
        f"""
        Your strongest current trait is
        **{strongest_personality}**
        with a score of **{strongest_score}%**.
        """
    )


# ==========================================================
# NO RESULT MESSAGE
# ==========================================================

else:

    st.divider()

    st.info(
        "👆 Complete the assessment and click "
        "**Analyze My Career Profile** to see your results."
    )

