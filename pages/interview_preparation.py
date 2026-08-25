import random
import streamlit as st
from utils.professional_sidebar import professional_sidebar
from utils.professional_theme import load_professional_theme
from utils.interview_db import (
    create_interview_table,
    save_interview,
    get_history
)

st.set_page_config(
    page_title="AI Interview Preparation",
    page_icon="💼",
    layout="wide"
)

load_professional_theme()
profile = professional_sidebar()

if not profile:
    st.stop()
create_interview_table()
st.markdown("""
<style>

.main-title{
font-size:34px;
font-weight:700;
color:#1F2937;
margin-bottom:5px;
}

.subtitle{
color:#6B7280;
font-size:16px;
margin-bottom:25px;
}

.metric-card{
background:white;
padding:20px;
border-radius:12px;
border:1px solid #E5E7EB;
box-shadow:0 2px 8px rgba(0,0,0,.05);
}

.section-card{
background:white;
padding:25px;
border-radius:15px;
border:1px solid #E5E7EB;
box-shadow:0 4px 10px rgba(0,0,0,.05);
margin-bottom:20px;
}

.question-card{
padding:18px;
border-radius:12px;
background:#F8FAFC;
border-left:5px solid #2563EB;
margin-bottom:15px;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<div class="main-title">
AI Interview Preparation
</div>

<div class="subtitle">
Prepare personalized interview questions based on your profile,
experience and technical skills.
</div>
""", unsafe_allow_html=True)

st.divider()
experience = int(profile.get("experience",0))

skills = [
    skill.strip().lower()
    for skill in profile.get(
        "technical_skills",
        ""
    ).split(",")
    if skill.strip()
]

current_role = profile.get(
    "current_role",
    "Professional"
)
c1,c2,c3,c4 = st.columns(4)

with c1:

    st.metric(
        "Current Role",
        current_role
    )

with c2:

    st.metric(
        "Experience",
        f"{experience} Years"
    )

with c3:

    st.metric(
        "Technical Skills",
        len(skills)
    )

with c4:

    readiness = min(
        45 +
        experience*6 +
        len(skills)*4,
        100
    )

    st.metric(
        "Interview Readiness",
        f"{readiness}%"
    )
st.markdown('<div class="section-card">',unsafe_allow_html=True)

st.subheader("Interview Configuration")

left,right = st.columns(2)

with left:

    interview_type = st.selectbox(

        "Interview Type",

        [

            "Technical",

            "HR",

            "Behavioral",

            "Coding"

        ]

    )

with right:

    difficulty = st.selectbox(

        "Difficulty",

        [

            "Easy",

            "Intermediate",

            "Advanced"

        ]

    )

st.markdown("</div>",unsafe_allow_html=True)
def generate_questions():

    questions = []

    # -------------------------
    # Python
    # -------------------------

    if "python" in skills:

        questions.extend([

            "Explain Python decorators.",

            "What are generators?",

            "Difference between List and Tuple?",

            "Explain Exception Handling.",

            "What are Python modules?"

        ])

    # -------------------------
    # Java
    # -------------------------

    if "java" in skills:

        questions.extend([

            "Explain JVM.",

            "Difference between JDK and JRE.",

            "Explain Multithreading."

        ])

    # -------------------------
    # SQL
    # -------------------------

    if "sql" in skills:

        questions.extend([

            "Explain SQL JOIN.",

            "What is Normalization?",

            "Difference between DELETE and TRUNCATE."

        ])

    # -------------------------
    # HTML/CSS
    # -------------------------

    if "html" in skills:

        questions.append(

            "What is Semantic HTML?"

        )

    if "css" in skills:

        questions.append(

            "Difference between Flexbox and Grid?"

        )

    # -------------------------
    # React
    # -------------------------

    if "react" in skills:

        questions.extend([

            "Explain React Hooks.",

            "Difference between useState and useEffect."

        ])

    # -------------------------
    # Git
    # -------------------------

    if "git" in skills:

        questions.append(

            "Explain Git Branching."

        )

    # -------------------------
    # FastAPI
    # -------------------------

    if "fastapi" in skills:

        questions.extend([

            "Explain Dependency Injection in FastAPI.",

            "Difference between FastAPI and Flask."

        ])
    if experience <= 2:

        questions.extend([

            "Tell me about yourself.",

            "Explain your final project.",

            "Why should we hire you?"

        ])

    elif experience <= 5:

        questions.extend([

            "Describe a challenging project.",

            "How do you improve application performance?",

            "How do you handle deadlines?"

        ])

    else:

        questions.extend([

            "How do you mentor junior developers?",

            "Explain System Design principles.",

            "Describe your leadership experience."

        ])
    random.shuffle(questions)

    if difficulty == "Easy":

        return questions[:5]

    elif difficulty == "Intermediate":

        return questions[:8]

    else:

        return questions[:10]
generate = st.button(

    "Generate Interview Questions",

    use_container_width=True

)

if generate:

    questions = generate_questions()

    st.session_state["questions"] = questions
if "questions" in st.session_state:

    st.divider()

    st.subheader("Interview Questions")

    answers = []

    for i, question in enumerate(st.session_state["questions"], 1):

        st.markdown(
            f"""
            <div class="question-card">

            <b>Question {i}</b><br><br>

            {question}

            </div>
            """,
            unsafe_allow_html=True
        )

        answer = st.text_area(

            "Your Answer",

            key=f"answer_{i}",

            height=120

        )

        answers.append(answer)
    submit = st.button(

        "Submit Interview",

        use_container_width=True

    )
    if submit:

        score = 0

        answered = 0

        for answer in answers:

            if len(answer.strip()) > 20:

                score += 10

                answered += 1

            elif len(answer.strip()) > 5:

                score += 5

                answered += 1
        score += experience * 2
        score += len(skills)
        if score > 100:
            score = 100
        save_interview(
            profile["email"],
            interview_type,
            difficulty,
            score
        )
        st.success("Interview completed successfully.")
        st.divider()

        st.subheader("Interview Result")

        st.metric(

            "Interview Score",

            f"{score}%"

        )
        st.progress(score / 100)
        if score >= 90:

            st.success(

                "Excellent interview performance."

            )

        elif score >= 75:

            st.info(

                "Good performance. Keep practicing advanced concepts."

            )

        elif score >= 60:

            st.warning(

                "Average performance. Improve technical depth."

            )

        else:

            st.error(

                "You need more interview preparation."

            )
        st.divider()

        c1,c2,c3 = st.columns(3)

        with c1:

            st.metric(

                "Questions",

                len(st.session_state["questions"])

            )

        with c2:

            st.metric(

                "Answered",

                answered

            )

        with c3:

            st.metric(

                "Skipped",

                len(st.session_state["questions"]) - answered

            )
        st.divider()

        st.subheader("Recommendations")

        if score < 70:

            st.warning(
                "Revise your core technical concepts."
            )

        if experience < 3:

            st.info(
                "Gain more hands-on project experience."
            )

        if len(skills) < 5:

            st.warning(
                "Learn more industry-relevant technologies."
            )

        st.success(
            "Practice mock interviews regularly to improve confidence."
        )
        st.subheader("Personalized Recommendations")
        recommendations = []
        if experience < 3:
            recommendations.append(
                "Work on more real-world projects to strengthen practical experience."
            )
        if len(skills) < 5:
            recommendations.append(
                "Expand your technical skill set by learning additional industry tools."
            )

        if score < 80:

           recommendations.append(
                "Practice mock interviews regularly to improve confidence and communication."
            )

        if interview_type == "Technical":

            recommendations.append(
                "Revise core programming concepts and problem-solving techniques."
            )

        elif interview_type == "HR":
            recommendations.append(
                "Prepare concise STAR-based answers for behavioral questions."
            )

        if not recommendations:
            recommendations.append(
                "Excellent preparation. Continue practicing to maintain your interview readiness."
            )
        for recommendation in recommendations:
            st.info(recommendation)
    st.divider()

st.subheader("Interview History")

history = get_history(profile["email"])

if history:

    for interview in history:

        with st.container(border=True):

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.write(interview["interview_type"])

            with c2:
                st.write(interview["difficulty"])

            with c3:
                st.metric(
                    "Score",
                    f"{interview['score']}%"
                )

            with c4:
                st.caption(interview["date"])

else:

    st.info("No interview history available.")
# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "TalentSphere Elevate • AI Powered Interview Preparation"
)