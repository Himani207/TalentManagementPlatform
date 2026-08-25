import streamlit as st

from utils.professional_sidebar import professional_sidebar
from utils.professional_theme import load_professional_theme

from utils.job_application_db import (
    create_job_tables,
    save_job,
    apply_job,
    check_applied
)

from utils.professional_db import (
    get_job_matches,
    calculate_skill_score,
    calculate_promotion_score,
    calculate_salary_growth
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Career Opportunity Matcher",
    page_icon="💼",
    layout="wide"
)

load_professional_theme()

# ==========================================================
# LOAD PROFILE
# ==========================================================

profile = professional_sidebar()

create_job_tables()

# ==========================================================
# PROFILE CHECK
# ==========================================================

required_fields = [
    "technical_skills",
    "experience",
    "current_role",
    "preferred_role"
]

missing = [
    field
    for field in required_fields
    if not profile.get(field)
]

if missing:

    st.warning(
        "Please complete your professional profile before viewing job recommendations."
    )

    st.switch_page(
        "pages/edit_professional_profile.py"
    )

    st.stop()

# ==========================================================
# DYNAMIC DATA
# ==========================================================
jobs = get_job_matches(profile)

skill_score = calculate_skill_score(profile)

promotion_score = calculate_promotion_score(profile)

salary_growth = calculate_salary_growth(profile)

experience = int(profile.get("experience", 0))

technical_skills = [
    skill.strip()
    for skill in profile.get("technical_skills", "").split(",")
    if skill.strip()
]

# ==========================================================
# PROFESSIONAL CSS
# ==========================================================

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
    max-width:1400px;
}

.page-header{
    background:white;
    border-radius:16px;
    padding:30px;
    border:1px solid #E5E7EB;
    box-shadow:0 6px 18px rgba(0,0,0,.05);
    margin-bottom:25px;
}

.page-title{
    font-size:34px;
    font-weight:700;
    color:#111827;
    margin-bottom:8px;
}

.subtitle{
    color:#6B7280;
    font-size:15px;
}

.custom-card{
    background:white;
    padding:24px;
    border-radius:16px;
    border:1px solid #E5E7EB;
    box-shadow:0 5px 14px rgba(0,0,0,.04);
    margin-bottom:20px;
}

.section-title{
    font-size:22px;
    font-weight:700;
    color:#1F2937;
    margin-bottom:18px;
}

.job-card{

    background:white;
    padding:25px;

    border-radius:18px;

    border:1px solid #E5E7EB;

    margin-bottom:25px;

    box-shadow:0 6px 18px rgba(0,0,0,.05);

    transition:0.3s;
}

.job-card:hover{

    box-shadow:0 12px 28px rgba(0,0,0,.12);

    transform:translateY(-2px);
}

.metric-card{

    background:#F8FAFC;

    border-radius:14px;

    padding:15px;

    border:1px solid #E5E7EB;

    margin-bottom:15px;
}

.filter-card{

    background:white;

    border-radius:16px;

    padding:20px;

    border:1px solid #E5E7EB;

    margin-bottom:25px;

    box-shadow:0 5px 14px rgba(0,0,0,.04);
}

hr{

    border:none;

    border-top:1px solid #E5E7EB;

    margin-top:15px;

    margin-bottom:15px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# HEADER
# ==========================================================

st.markdown(f"""

<div class="page-header">

<div class="page-title">

Career Opportunity Matcher

</div>

<div class="subtitle">

Discover career opportunities tailored to your skills, experience and career goals.

</div>

<hr>

<b>{profile.get("full_name")}</b><br>

{profile.get("current_role")} • {profile.get("company")}

</div>

""", unsafe_allow_html=True)

# ==========================================================
# FILTERS
# ==========================================================

st.markdown('<div class="filter-card">', unsafe_allow_html=True)

st.subheader("Search Opportunities")

c1, c2, c3 = st.columns(3)

with c1:

    search = st.text_input(
        "Search by Role",
        placeholder="Backend Developer"
    )

with c2:

    selected_location = st.selectbox(
        "Location",
        [
            "All",
            "Remote",
            "Bangalore",
            "Hyderabad",
            "Delhi",
            "Mumbai",
            "Pune"
        ]
    )

with c3:

    minimum_match = st.slider(
        "Minimum Match",
        0,
        100,
        40
    )

st.markdown("</div>", unsafe_allow_html=True)
# ==========================================================
# CAREER PROFILE
# ==========================================================

left, right = st.columns([2, 1])

with left:

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Career Profile</div>',
        unsafe_allow_html=True
    )

    st.write(f"**Current Role** : {profile.get('current_role')}")

    st.write(f"**Company** : {profile.get('company')}")

    st.write(f"**Experience** : {experience} Years")

    st.write(f"**Preferred Role** : {profile.get('preferred_role')}")

    st.write(f"**Location** : {profile.get('location')}")

    st.markdown("</div>", unsafe_allow_html=True)

with right:

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Career Scores</div>',
        unsafe_allow_html=True
    )

    st.metric(
        "Skill Score",
        f"{skill_score}%"
    )

    st.progress(skill_score/100)

    st.metric(
        "Promotion Readiness",
        f"{promotion_score}%"
    )

    st.progress(promotion_score/100)

    st.metric(
        "Expected Salary Growth",
        f"+{salary_growth}%"
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# JOB MATCHING
# ==========================================================

st.markdown(
    '<div class="section-title">Recommended Opportunities</div>',
    unsafe_allow_html=True
)

filtered_jobs = []

for job in jobs:

    if search:

        if search.lower() not in job["role"].lower():

            continue

    if selected_location != "All":

        if job["location"] != selected_location:

            continue

    if job["match"] < minimum_match:

        continue

    filtered_jobs.append(job)

if len(filtered_jobs) == 0:

    st.warning("No matching opportunities found.")

else:

    st.success(f"{len(filtered_jobs)} opportunities found.")

    for index, job in enumerate(filtered_jobs):

        job_id = job["role"] + job["company"]

        st.markdown('<div class="job-card">', unsafe_allow_html=True)

        top_left, top_right = st.columns([4,1])

        with top_left:

            st.subheader(job["role"])

            st.caption(job["company"])

        with top_right:

            st.metric(
                "Match",
                f"{job['match']}%"
            )

            st.progress(job["match"]/100)

        st.divider()

        info1, info2, info3 = st.columns(3)

        with info1:

            st.write("**Location**")

            st.write(job["location"])

        with info2:

            st.write("**Salary**")

            st.write(job["salary"])

        with info3:

            st.write("**Experience**")

            st.write(f"{job['experience']} Years")

        st.write("### Job Type")

        st.info(job["job_type"])

        st.write("### Required Skills")

        skill_cols = st.columns(4)

        for i, skill in enumerate(job["skills"]):

            with skill_cols[i % 4]:

                st.success(skill)

        user_skills = [

            skill.strip().lower()

            for skill in profile["technical_skills"].split(",")

        ]

        missing_skills = [

            skill

            for skill in job["skills"]

            if skill.lower() not in user_skills

        ]

        if missing_skills:

            st.write("### Skills Gap")

            for skill in missing_skills:

                st.warning(skill)

        else:

            st.success(
                "Your skills match this opportunity."
            )

        with st.expander("View Job Description"):

            st.write(job["description"])

        st.write("### AI Recommendation")

        if job["match"] >= 90:

            st.success(
                "Excellent match. You should apply for this opportunity."
            )

        elif job["match"] >= 75:

            st.info(
                "Good match. Learning a few additional skills will improve your chances."
            )

        else:

            st.warning(
                "Moderate match. Build missing skills before applying."
            )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "Apply Now",
                key=f"apply_{index}",
                use_container_width=True
            ):

                apply_job(
                    profile["email"],
                    job_id,
                    job["role"],
                    job["company"],
                    job["location"]
                )

                st.success("Application submitted successfully.")

        with col2:

            if st.button(
                "Save Job",
                key=f"save_{index}",
                use_container_width=True
            ):

                save_job(
                    profile["email"],
                    job_id,
                    job["role"],
                    job["company"],
                    job["location"]
                )

                st.success("Job saved successfully.")

        st.markdown("</div>", unsafe_allow_html=True)
# ==========================================================
# INTERVIEW PREPARATION
# ==========================================================

st.markdown('<div class="custom-card">', unsafe_allow_html=True)

st.markdown(
    '<div class="section-title">Interview Preparation</div>',
    unsafe_allow_html=True
)

tips = [

    "Review your core technical concepts related to your target role.",

    "Practice coding and problem-solving questions regularly.",

    "Prepare project explanations with measurable outcomes.",

    "Research the company's products, culture and recent updates.",

    "Prepare HR interview questions using the STAR method.",

    "Keep your resume and LinkedIn profile updated."
]

for tip in tips:

    st.write(f"• {tip}")

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# CAREER SUGGESTIONS
# ==========================================================

st.markdown('<div class="custom-card">', unsafe_allow_html=True)

st.markdown(
    '<div class="section-title">Career Suggestions</div>',
    unsafe_allow_html=True
)

if promotion_score < 60:

    st.warning("""
You should focus on strengthening your technical foundation,
building more real-world projects and improving leadership skills.
""")

elif promotion_score < 80:

    st.info("""
You are progressing well.
Focus on certifications, open-source contributions and advanced projects
to become ready for senior opportunities.
""")

else:

    st.success("""
Your profile is highly competitive.

Continue mentoring others, learning new technologies and applying for
leadership positions.
""")

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# PROFILE INSIGHTS
# ==========================================================

st.markdown('<div class="custom-card">', unsafe_allow_html=True)

st.markdown(
    '<div class="section-title">Profile Insights</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Experience",
        f"{experience} Years"
    )

with col2:

    st.metric(
        "Technical Skills",
        len(technical_skills)
    )

with col3:

    st.metric(
        "Job Matches",
        len(filtered_jobs)
    )

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# QUICK ACTIONS
# ==========================================================

st.markdown('<div class="custom-card">', unsafe_allow_html=True)

st.markdown(
    '<div class="section-title">Quick Actions</div>',
    unsafe_allow_html=True
)

btn1, btn2, btn3 = st.columns(3)

with btn1:

    if st.button(
        "Career Analytics",
        use_container_width=True
    ):

        st.switch_page(
            "pages/career_analytics.py"
        )

with btn2:

    if st.button(
        "My Profile",
        use_container_width=True
    ):

        st.switch_page(
            "pages/professional_profile.py"
        )

with btn3:

    if st.button(
        "Edit Profile",
        use_container_width=True
    ):

        st.switch_page(
            "pages/edit_professional_profile.py"
        )

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# FOOTER
# ==========================================================

st.divider()
st.markdown(
"""
<div style="text-align:center;
padding:18px;
color:#6B7280;
font-size:14px;">

TalentSphere Elevate<br>

AI-Powered Career Development Platform

</div>
""",
unsafe_allow_html=True
)