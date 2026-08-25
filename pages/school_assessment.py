import streamlit as st
import pandas as pd

from utils.session import logout
from utils.school_db import (
    create_student_table,
    create_report_table,
    create_skill_assessment_table,
    save_assessment_score,
    save_skill_assessment_results,
    get_latest_assessment,
    get_skill_assessment_results,
    get_student_profile,
    add_notification
)
# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Skill Assessment",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# DATABASE
# ==========================================================

create_student_table()
create_report_table()
create_skill_assessment_table()
# ==========================================================
# LOGIN CHECK
# ==========================================================

if (
    "logged_in" not in st.session_state
    or not st.session_state.logged_in
):
    st.warning("Please login first.")
    st.switch_page("pages/login.py")
    st.stop()


email = st.session_state.email


# ==========================================================
# STUDENT PROFILE
# ==========================================================

student = get_student_profile(email)

if student is None:
    student = {
        "email": email,
        "class": "Not Available",
        "school": "Not Available",
        "subject": "",
        "career": ""
    }


student_name = st.session_state.get(
    "name",
    email.split("@")[0].title()
)


# ==========================================================
# CSS
# ==========================================================

st.markdown(
    """
    <style>

    .assessment-header {
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 25px;
        background: linear-gradient(
            135deg,
            rgba(102,126,234,0.18),
            rgba(118,75,162,0.12)
        );
        border: 1px solid rgba(128,128,128,0.18);
    }

    .assessment-header h1 {
        margin-bottom: 8px;
    }

    .assessment-header p {
        font-size: 16px;
        opacity: 0.75;
    }

    .assessment-card {
        padding: 22px;
        border-radius: 18px;
        margin-bottom: 15px;
        border: 1px solid rgba(128,128,128,0.18);
        background: rgba(255,255,255,0.04);
    }

    .assessment-card h3 {
        margin-bottom: 10px;
    }

    .assessment-card p {
        font-size: 17px;
        font-weight: 500;
    }

    .skill-label {
        font-size: 13px;
        opacity: 0.65;
    }

    .score-card {
        padding: 25px;
        border-radius: 18px;
        text-align: center;
        border: 1px solid rgba(128,128,128,0.18);
        background: rgba(255,255,255,0.04);
    }

    .score-number {
        font-size: 38px;
        font-weight: 700;
        margin: 10px 0;
    }

    .result-card {
        padding: 25px;
        border-radius: 18px;
        border: 1px solid rgba(128,128,128,0.18);
        margin-top: 20px;
    }

    .skill-result-card {
        padding: 18px;
        border-radius: 15px;
        border: 1px solid rgba(128,128,128,0.15);
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

st.markdown(
    f"""
    <div class="assessment-header">
      <h1>📝 Skill Assessment</h1>
      <p>
         Welcome, {student_name} 👋
      </p>
      <p>
        Evaluate your problem-solving, logical,
        technical and interpersonal skills.
      </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# STUDENT INFORMATION
# ==========================================================

c1, c2, c3 = st.columns(3)

with c1:
    st.info(
        f"🏫 Class: "
        f"{student.get('class') or 'Not Available'}"
    )

with c2:
    st.info(
        f"📚 Subject: "
        f"{student.get('subject') or 'Not Selected'}"
    )

with c3:
    st.info(
        f"🎯 Career: "
        f"{student.get('career') or 'Not Selected'}"
    )


# ==========================================================
# PREVIOUS SCORE
# ==========================================================

previous_score = get_latest_assessment(email)

if previous_score is None:
    previous_score = 0
previous_skill_scores = get_skill_assessment_results(email)

st.write("")

st.subheader("📊 Previous Assessment Performance")

score_col1, score_col2 = st.columns(2)


with score_col1:

    st.markdown(
        f"""
        <div class="score-card">
          <h4>Latest Score</h4>
          <div class="score-number">
            {previous_score}%
          </div>
          <p>
            Your latest recorded assessment score
          </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with score_col2:

    if previous_score >= 80:
        status = "🌟 Excellent"

    elif previous_score >= 60:
        status = "👍 Good"

    elif previous_score >= 40:
        status = "📈 Developing"

    else:
        status = "🚀 Getting Started"

    st.markdown(
        f"""
        <div class="score-card">
          <h4>Performance Status</h4>
          <div class="score-number">
            {status}
          </div>
          <p>
            Based on your latest assessment
          </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# SKILL ASSESSMENT
# ==========================================================

st.write("")

st.subheader("🧠 Skill Assessment")

st.write(
    "Answer the following questions honestly. "
    "Each question evaluates a different skill area."
)


# ==========================================================
# 8 PROFESSIONAL QUESTIONS
# ==========================================================

questions = [

    {
        "question":
            "When you face a difficult problem, what do you usually do first?",

        "skill":
            "Problem Solving",

        "options": [
            "Break the problem into smaller parts",
            "Try different solutions until one works",
            "Ask someone for help immediately",
            "Avoid the problem until later"
        ],

        "scores": [4, 3, 2, 1]
    },

    {
        "question":
            "Which activity best describes your logical thinking ability?",

        "skill":
            "Logical Thinking",

        "options": [
            "Solving puzzles and finding patterns",
            "Understanding step-by-step instructions",
            "Following solutions given by others",
            "I find logical problems difficult"
        ],

        "scores": [4, 3, 2, 1]
    },

    {
        "question":
            "You are given a project with no fixed solution. What would you prefer to do?",

        "skill":
            "Creativity",

        "options": [
            "Create a new and unique approach",
            "Modify an existing idea",
            "Follow an example from someone else",
            "Wait for detailed instructions"
        ],

        "scores": [4, 3, 2, 1]
    },

    {
        "question":
            "How do you handle presenting your ideas in front of others?",

        "skill":
            "Communication",

        "options": [
            "I confidently explain my ideas",
            "I can explain with some preparation",
            "I prefer communicating through writing",
            "I feel very uncomfortable speaking"
        ],

        "scores": [4, 3, 2, 1]
    },

    {
        "question":
            "Which activity would you enjoy the most?",

        "skill":
            "Technical Skills",

        "options": [
            "Building a website or application",
            "Learning how technology works",
            "Using software and digital tools",
            "I prefer non-technical activities"
        ],

        "scores": [4, 3, 2, 1]
    },

    {
        "question":
            "When making an important decision, what do you normally consider?",

        "skill":
            "Analytical Thinking",

        "options": [
            "Facts, evidence and possible outcomes",
            "My previous experience",
            "Advice from other people",
            "My first instinct"
        ],

        "scores": [4, 3, 2, 1]
    },

    {
        "question":
            "What would you do if your team members disagreed with your idea?",

        "skill":
            "Teamwork",

        "options": [
            "Listen to their ideas and find a common solution",
            "Explain my idea and discuss the differences",
            "Let someone else make the decision",
            "Continue with my idea without discussion"
        ],

        "scores": [4, 3, 2, 1]
    },

    {
        "question":
            "If you are selected as the leader of a school project, what would you do?",

        "skill":
            "Leadership",

        "options": [
            "Divide responsibilities and motivate the team",
            "Coordinate tasks and monitor progress",
            "Complete most of the work myself",
            "Let the team decide everything"
        ],

        "scores": [4, 3, 2, 1]
    }

]


# ==========================================================
# DISPLAY QUESTIONS
# ==========================================================

answers = []

for index, question in enumerate(questions):

    st.markdown(
        f"""
        <div class="assessment-card">
          <h3>
            Question {index + 1}
          </h3>
          <p>
            {question["question"]}
          </p>
          <span class="skill-label">
            Skill evaluated:
            {question["skill"]}
          </span>

        </div>
        """,
        unsafe_allow_html=True
    )

    answer = st.radio(
        "Select your answer:",
        question["options"],
        key=f"skill_question_{index}",
        label_visibility="collapsed"
    )

    answers.append(answer)

    st.write("")


# ==========================================================
# SUBMIT
# ==========================================================

st.write("")

if st.button(
    "🚀 Submit Assessment",
    type="primary",
    use_container_width=True
):

    # ------------------------------------------------------
    # CALCULATE SKILL SCORES
    # ------------------------------------------------------

    skill_scores = {}

    total_score = 0

    max_score = len(questions) * 4


    for index, question in enumerate(questions):

        selected_answer = answers[index]

        selected_index = question["options"].index(
            selected_answer
        )

        score = question["scores"][selected_index]

        skill = question["skill"]

        skill_scores[skill] = int(
            (score / 4) * 100
        )

        total_score += score


    # ------------------------------------------------------
    # OVERALL SCORE
    # ------------------------------------------------------

    overall_score = round(
        (total_score / max_score) * 100
    )
    # ------------------------------------------------------
    # SAVE OVERALL SCORE
    # ------------------------------------------------------

    save_assessment_score(
        email,
        overall_score
    )
    # ------------------------------------------------------
    # SAVE SKILL-WISE SCORES
    # ------------------------------------------------------

    save_skill_assessment_results(
        email,
        skill_scores
    )
    add_notification(
        email,
        "Assessment Completed 🎉",
        f"Your skill assessment has been completed successfully with an overall score of {overall_score}%.",
        "Assessment"
    )
    # ------------------------------------------------------
    # STORE RESULT IN SESSION
    # ------------------------------------------------------

    st.session_state.assessment_result = {
        "overall_score": overall_score,
        "skill_scores": skill_scores
    }
    st.success(
        f"🎉 Assessment completed successfully! "
        f"Your overall skill score is {overall_score}%."
    )


# ==========================================================
# DISPLAY RESULTS
# ==========================================================
# ==========================================================
# DISPLAY RESULTS
# ==========================================================

if "assessment_result" in st.session_state:

    result = st.session_state.assessment_result

    overall_score = result.get(
        "overall_score",
        0
    )

    skill_scores = result.get(
        "skill_scores",
        {}
    )

elif previous_skill_scores:

    overall_score = previous_score

    skill_scores = previous_skill_scores

else:

    overall_score = 0
    skill_scores = {}


# ==========================================================
# RESULTS SECTION
# ==========================================================

st.write("")
st.divider()

st.subheader("📊 Your Skill Assessment Results")


if skill_scores:
    # ======================================================
    # OVERALL RESULT
    # ======================================================

    result_col1, result_col2 = st.columns(2)


    with result_col1:

        st.markdown(
            f"""
            <div class="score-card">
              <h4>Overall Skill Score</h4>
              <div class="score-number">
                {overall_score}%
              </div>
              <p>
                Based on all 8 skill areas
              </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ======================================================
    # STRONGEST SKILL
    # ======================================================

    strongest_skill = max(
        skill_scores,
        key=skill_scores.get
    )

    strongest_score = skill_scores[
        strongest_skill
    ]


    with result_col2:

        st.markdown(
            f"""
            <div class="score-card">
              <h4>🌟 Strongest Skill</h4>
              <div class="score-number">
                {strongest_score}%
              </div>
              <p>
                {strongest_skill}
              </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ======================================================
    # BAR GRAPH
    # ======================================================

    st.write("")

    st.subheader("📈 Skill-wise Performance")

    st.write(
        "Your assessment responses have been converted "
        "into percentage scores for each skill."
    )


    chart_data = pd.DataFrame(
        {
            "Skill": list(skill_scores.keys()),
            "Score": list(skill_scores.values())
        }
    )


    chart_data = chart_data.set_index("Skill")


    st.bar_chart(
        chart_data,
        y="Score",
        height=450
    )


    # ======================================================
    # SKILL BREAKDOWN
    # ======================================================

    st.write("")

    st.subheader("🎯 Skill Breakdown")


    result_columns = st.columns(4)


    for index, (skill, score) in enumerate(
        skill_scores.items()
    ):

        with result_columns[index % 4]:

            st.metric(
                skill,
                f"{score}%"
            )


    # ======================================================
    # STRONGEST / WEAKEST
    # ======================================================

    weakest_skill = min(
        skill_scores,
        key=skill_scores.get
    )

    weakest_score = skill_scores[
        weakest_skill
    ]


    st.write("")

    strong_col, weak_col = st.columns(2)


    with strong_col:

        st.success(
            f"🌟 **Strongest Skill**\n\n"
            f"{strongest_skill} — {strongest_score}%"
        )


    with weak_col:

        st.warning(
            f"📚 **Development Area**\n\n"
            f"{weakest_skill} — {weakest_score}%"
        )


    # ======================================================
    # PERFORMANCE ANALYSIS
    # ======================================================

    st.write("")

    st.subheader("💡 Performance Analysis")


    if overall_score >= 80:

        st.success(
            f"🌟 Excellent performance! "
            f"Your strongest area is **{strongest_skill}**. "
            f"You are demonstrating strong overall skills."
        )

    elif overall_score >= 60:

        st.info(
            f"👍 Good performance! "
            f"Your strongest area is **{strongest_skill}**. "
            f"Continue developing **{weakest_skill}** "
            f"to create a more balanced skill profile."
        )

    elif overall_score >= 40:

        st.warning(
            f"📈 You are developing your skills. "
            f"Your strongest area is **{strongest_skill}**. "
            f"Focus more on improving **{weakest_skill}**."
        )

    else:

        st.warning(
            f"🚀 This is a starting point. "
            f"Focus on improving **{weakest_skill}** "
            f"through regular practice and learning."
        )


    # ======================================================
    # RECOMMENDED DEVELOPMENT AREAS
    # ======================================================

    st.write("")

    st.subheader("🚀 Recommended Development Areas")


    for skill, score in skill_scores.items():

        if score < 60:

            st.write(
                f"📌 **{skill} — {score}%**  \n"
                f"Practice recommended. Work on exercises "
                f"and learning activities related to this skill."
            )

        elif score < 80:

            st.write(
                f"📈 **{skill} — {score}%**  \n"
                f"Good foundation. Continue practicing "
                f"to strengthen this skill."
            )

        else:

            st.write(
                f"⭐ **{skill} — {score}%**  \n"
                f"Strong performance. Continue challenging "
                f"yourself in this area."
            )


    # ======================================================
    # RETAKE
    # ======================================================

    st.write("")
    st.divider()

    if st.button(
        "🔄 Take New Assessment",
        use_container_width=True
    ):

        # Clear previous answers
        for index in range(len(questions)):

            key = f"skill_question_{index}"

            if key in st.session_state:
                del st.session_state[key]


        # Clear result
        if "assessment_result" in st.session_state:
            del st.session_state.assessment_result


        st.rerun()

