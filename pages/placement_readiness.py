import streamlit as st

from utils.coding_db import get_coding_score
from utils.college_db import get_project_score
from utils.mock_interview_db import get_mock_interview_score
from utils.internship_db import get_internship_score
from utils.resume_db import get_resume_score

from utils.placement_db import (
    save_placement_score,
    get_placement
)


st.set_page_config(
    page_title="Placement Readiness",
    page_icon="🎯",
    layout="wide"
)


# -----------------------------
# Login
# -----------------------------

if "logged_in" not in st.session_state:
    st.switch_page("pages/login.py")


email = st.session_state.email



st.title("🎯 Placement Readiness Dashboard")

st.caption(
    "AI-powered evaluation of your placement preparation"
)



# -----------------------------
# Fetch Scores
# -----------------------------

resume_score = get_resume_score(email)

coding_score = get_coding_score(email)

project_score = get_project_score(email)

communication_score = get_mock_interview_score(email)

internship_score = get_internship_score(email)



# -----------------------------
# Placement Formula
# -----------------------------

placement_score = round(

    (resume_score * 0.25) +

    (coding_score * 0.30) +

    (project_score * 0.20) +

    (communication_score * 0.15) +

    (internship_score * 0.10)

)



# -----------------------------
# Save Result
# -----------------------------

save_placement_score(

    email=email,

    resume=resume_score,

    coding=coding_score,

    projects=project_score,

    communication=communication_score,

    internship=internship_score,

    placement=placement_score

)



# -----------------------------
# Get Saved Score
# -----------------------------

placement = get_placement(email)



if placement:


    final_score = placement["placement_score"]


else:

    final_score = placement_score



# -----------------------------
# Overall Score
# -----------------------------

st.divider()

st.subheader("🚀 Overall Placement Readiness")



col1,col2 = st.columns(2)


with col1:

    st.metric(
        "🎯 Placement Score",
        f"{final_score}%"
    )


with col2:


    if final_score >= 90:

        status="Excellent 🚀"


    elif final_score >=75:

        status="Ready 👍"


    elif final_score >=50:

        status="Improving 📈"


    else:

        status="Needs Work ⚠️"



    st.metric(
        "Status",
        status
    )



st.progress(
    final_score/100
)



# -----------------------------
# Score Breakdown
# -----------------------------

st.divider()

st.subheader("📊 Skill Breakdown")



c1,c2,c3,c4,c5 = st.columns(5)


c1.metric(
    "📄 Resume",
    f"{resume_score}%"
)


c2.metric(
    "💻 Coding",
    f"{coding_score}%"
)


c3.metric(
    "🚀 Projects",
    f"{project_score}%"
)


c4.metric(
    "🗣 Interview",
    f"{communication_score}%"
)


c5.metric(
    "💼 Internship",
    f"{internship_score}%"
)



# -----------------------------
# Recommendations
# -----------------------------

st.divider()

st.subheader("🤖 AI Recommendations")



recommendations = []


if resume_score < 80:

    recommendations.append(
        "Improve ATS resume with projects and skills."
    )


if coding_score < 80:

    recommendations.append(
        "Practice more DSA and coding problems."
    )


if project_score < 80:

    recommendations.append(
        "Add industry-level projects."
    )


if communication_score < 80:

    recommendations.append(
        "Practice more mock interviews."
    )
if internship_score < 80:

    recommendations.append(
        "Complete internships to gain experience."
    )

if recommendations:

    for item in recommendations:

        st.warning(item)


else:

    st.success(
        "🎉 Your profile is placement ready!"
    )