import streamlit as st
import re
from ai.gemini import ask_gemini
from utils.mock_interview_db import save_mock_interview_score

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="AI Mock Interview",
    page_icon="🎤",
    layout="wide"
)

# ==========================================================
# LOGIN CHECK
# ==========================================================

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("pages/login.py")

email = st.session_state.email

# ==========================================================
# TITLE
# ==========================================================

st.title("🎤 AI Mock Interview")

# ==========================================================
# SELECT ROLE
# ==========================================================

role = st.selectbox(
    "Choose Interview Role",
    [
        "Software Developer",
        "Python Developer",
        "Data Analyst",
        "Frontend Developer",
        "Machine Learning Engineer"
    ]
)

level = st.selectbox(
    "Experience Level",
    [
        "Fresher",
        "Intermediate",
        "Advanced"
    ]
)

# ==========================================================
# SESSION STATE
# ==========================================================

if "question" not in st.session_state:
    st.session_state.question = None

if "feedback" not in st.session_state:
    st.session_state.feedback = None

# ==========================================================
# START INTERVIEW
# ==========================================================

if st.button("🎯 Start Interview"):

    prompt = f"""
You are an AI technical interviewer.

Generate ONE interview question.

Role: {role}
Experience: {level}

Return only the interview question.
"""

    st.session_state.question = ask_gemini(prompt)
    st.session_state.feedback = None

# ==========================================================
# SHOW QUESTION
# ==========================================================

if st.session_state.question:

    st.subheader("🤖 Interview Question")

    st.info(st.session_state.question)

    answer = st.text_area(
        "Your Answer",
        height=200
    )

    if st.button("Submit Answer"):

        if answer.strip() == "":
            st.warning("Please enter your answer.")
            st.stop()

        feedback_prompt = f"""
You are an expert technical interviewer.

Interview Question:
{st.session_state.question}

Candidate Answer:
{answer}

Evaluate the answer.

Return EXACTLY in this format:

Communication: X/10
Technical Accuracy: X/10
Confidence: X/10
Overall Score: X/100

Feedback:
(Write detailed feedback)

Suggestions:
(List improvement suggestions)
"""

        with st.spinner("AI is evaluating your answer..."):

            feedback = ask_gemini(feedback_prompt)

        st.session_state.feedback = feedback

        # ==========================================
        # EXTRACT SCORE
        # ==========================================

        match = re.search(
            r"Overall Score\s*:\s*(\d+)",
            feedback,
            re.IGNORECASE
        )

        if match:
            score = int(match.group(1))
        else:
            score = 0

        # ==========================================
        # SAVE SCORE
        # ==========================================

        save_mock_interview_score(
            email=email,
            score=score,
            feedback=feedback
        )

# ==========================================================
# DISPLAY FEEDBACK
# ==========================================================

if st.session_state.feedback:

    st.divider()

    st.subheader("📊 AI Interview Feedback")

    st.write(st.session_state.feedback)

    match = re.search(
        r"Overall Score\s*:\s*(\d+)",
        st.session_state.feedback,
        re.IGNORECASE
    )

    if match:

        score = int(match.group(1))

        st.metric(
            "Interview Score",
            f"{score}/100"
        )

        st.progress(score / 100)

    if st.button("Next Question"):

        st.session_state.question = None
        st.session_state.feedback = None

        st.rerun()