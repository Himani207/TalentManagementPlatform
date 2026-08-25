import streamlit as st
from utils.college_db import get_profile
from utils.resume_db import get_resume_score
from utils.coding_db import get_coding_score
from utils.job_matching_db import calculate_job_matches
st.set_page_config(
    page_title="Job Matching",
    page_icon="💼",
    layout="wide"
)
if "logged_in" not in st.session_state:
    st.switch_page("pages/login.py")
email = st.session_state.email
profile = get_profile(email)
resume_score = get_resume_score(email)
coding_score = get_coding_score(email)
st.title("💼 AI Job Matching Engine")
st.caption(
    "AI analyzes your profile and recommends suitable roles"
)

if profile:
    matches = calculate_job_matches(

        skills=profile["skills"],

        cgpa=profile["cgpa"],

        projects=profile["projects"],

        resume_score=resume_score,

        coding_score=coding_score,

        location=profile["location"]

    )
    st.subheader("🎯 Recommended Job Roles")
    for job in matches:


        st.markdown(
        f"""
        ## 💼 {job['role']}

        **Match Percentage:** {job['match']}%

        **Location:** {job['location']}

        **Required Skills:**
        {", ".join(job['skills'])}

        """
        )


        st.progress(
            job["match"]/100
        )
        st.divider()
else:

    st.warning(
        "Complete your profile first"
    )