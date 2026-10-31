import streamlit as st
from utils.professional_sidebar import professional_sidebar
from utils.professional_theme import load_professional_theme
from utils.professional_db import (
    calculate_skill_score,
    calculate_promotion_score,
    calculate_career_growth,
    calculate_salary_growth,
    get_job_matches,
    get_certifications,
)
# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Professional Dashboard",
    page_icon="💼",
    layout="wide"
)
load_professional_theme()
st.markdown("""
<style>

/* Hide Streamlit's page navigation */
[data-testid="stSidebarNav"] {
    display: none !important;
}

/* Hide the page selector */
[data-testid="stPageNav"] {
    display: none !important;
}

</style>
""", unsafe_allow_html=True)
# ==========================================================
# LOAD SIDEBAR + PROFILE
# ==========================================================

profile = professional_sidebar()
# ==========================================================
# ENSURE PROFILE HAS ALL REQUIRED FIELDS
# ==========================================================

profile = profile or {}

profile.setdefault("technical_skills", "")
profile.setdefault("preferred_role", "")
profile.setdefault("experience", 0)
profile.setdefault("leadership", 0)

profile.setdefault("full_name", "Professional")
profile.setdefault("phone", "")
profile.setdefault("location", "")
profile.setdefault("company", "")
profile.setdefault("current_role", "")
profile.setdefault("soft_skills", "")
profile.setdefault("work_experience", "")
profile.setdefault("achievements", "")
profile.setdefault("certifications", "")
profile.setdefault("career_goal", "")
profile.setdefault("current_salary", 0)
profile.setdefault("linkedin", "")
profile.setdefault("github", "")
profile.setdefault("resume_score", 0)
# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

.block-container{
padding-top:1rem;
max-width:1400px;
}

.stApp{
background:#F5F7FB;
}

/* KPI Card */

.metric-card{
background:white;
padding:22px;
border-radius:18px;
box-shadow:0 4px 12px rgba(0,0,0,.05);
border:1px solid #E5E7EB;
text-align:center;
}

/* White Card */

.white-card{
background:white;
padding:24px;
border-radius:18px;
border:1px solid #E5E7EB;
margin-bottom:20px;
box-shadow:0 4px 12px rgba(0,0,0,.04);
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# DYNAMIC DATA
# ==========================================================

skill_score = calculate_skill_score(profile)

promotion_score = calculate_promotion_score(profile)

career_growth = calculate_career_growth(profile)

salary_growth = calculate_salary_growth(profile)

job_matches = get_job_matches(profile)

certifications = get_certifications(profile)
experience = int(profile.get("experience", 0))
skills = [
    s.strip()
    for s in profile.get("technical_skills", "").split(",")
    if s.strip()
]

skill_count = len(skills)
leadership = int(profile.get("leadership", 0))
# ==========================================================
# CAREER LEVEL
# ==========================================================

if experience < 2:
    career_level = "Entry Level"

elif experience < 5:
    career_level = "Mid Level"

elif experience < 10:
    career_level = "Senior Level"

else:
    career_level = "Expert"

# ==========================================================
# WELCOME BANNER
# ==========================================================

st.markdown(f"""
<div style="
background:white;
padding:30px;
border-radius:18px;
border:1px solid #E5E7EB;
margin-bottom:25px;
box-shadow:0 5px 15px rgba(0,0,0,.05);
">

<h1 style="margin:0;color:#111827;">
Welcome, {profile.get("full_name","Professional")} 👋
</h1>

<h3 style="color:#4B5563;">
{profile.get("current_role","Professional")}
</h3>
<p style="font-size:17px;color:#6B7280;">
🏢 {profile.get("company","-")}
&nbsp;&nbsp;&nbsp;
📍 {profile.get("location","-")}
</p>

</div>
""", unsafe_allow_html=True)

# ==========================================================
# KPI CARDS
# ==========================================================

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown(f"""
    <div class="metric-card">

    <h4>Skill Score</h4>

    <h1 style="color:#2563EB;">
    {skill_score}%
    </h1>

    </div>
    """, unsafe_allow_html=True)

with c2:

    st.markdown(f"""
    <div class="metric-card">

    <h4>Promotion</h4>

    <h1 style="color:#16A34A;">
    {promotion_score}%
    </h1>

    </div>
    """, unsafe_allow_html=True)

with c3:

    st.markdown(f"""
    <div class="metric-card">

    <h4>Career Growth</h4>

    <h1 style="color:#7C3AED;">
    {career_growth}%
    </h1>

    </div>
    """, unsafe_allow_html=True)

with c4:

    st.markdown(f"""
    <div class="metric-card">

    <h4>Salary Growth</h4>

    <h1 style="color:#EA580C;">
    +{salary_growth}%
    </h1>

    </div>
    """, unsafe_allow_html=True)

st.write("")

# ==========================================================
# PROFESSIONAL SUMMARY
# ==========================================================

left, right = st.columns([2, 1])

with left:

    st.markdown('<div class="white-card">', unsafe_allow_html=True)

    st.subheader("Professional Summary")

    st.write(f"**Current Role:** {profile.get('current_role','-')}")

    st.write(f"**Company:** {profile.get('company','-')}")

    st.write(f"**Experience:** {experience} Years")

    st.write(f"**Career Level:** {career_level}")

    st.write(f"**Preferred Role:** {profile.get('preferred_role','-')}")

    st.markdown("</div>", unsafe_allow_html=True)

with right:

    st.markdown('<div class="white-card">', unsafe_allow_html=True)

    st.subheader("Career Snapshot")

    st.metric("Technical Skills", skill_count)

    st.metric("Leadership", f"{leadership}%")

    st.metric("Career Growth", f"{career_growth}%")

    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

# ==========================================================
# AI CAREER OBJECTIVE
# ==========================================================
st.markdown('<div class="white-card">', unsafe_allow_html=True)

st.subheader("AI Career Objective")

st.info(
    "Generate a personalized AI career objective based on your profile."
)

if st.button("✨ Generate Career Objective"):
    st.switch_page("pages/career_recommendation.py")
st.markdown("</div>", unsafe_allow_html=True)
# ==========================================================
# CAREER PROGRESS
# ==========================================================

st.markdown('<div class="white-card">', unsafe_allow_html=True)

st.subheader("Career Progress")

p1, p2 = st.columns(2)

with p1:

    st.write("Technical Skills")
    st.progress(skill_score / 100)

    st.write("Leadership")
    st.progress(leadership / 100)

    st.write("Promotion Readiness")
    st.progress(promotion_score / 100)

with p2:

    st.write("Career Growth")
    st.progress(career_growth / 100)

    st.write("Learning Progress")
    st.progress(min(skill_score + 5, 100) / 100)

    completed = len([
        x for x in [
            profile.get("full_name"),
            profile.get("company"),
            profile.get("current_role"),
            profile.get("technical_skills"),
            profile.get("career_goal"),
            profile.get("preferred_role"),
            profile.get("experience")
        ] if x
    ])

    st.write("Profile Completion")
    st.progress(completed / 7)

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# AI CAREER INSIGHTS
# ==========================================================

st.markdown('<div class="white-card">', unsafe_allow_html=True)

st.subheader("AI Career Insights")

insights = []

if experience < 3:
    insights.append(
        "Gain more hands-on industry experience by contributing to larger projects."
    )

if leadership < 70:
    insights.append(
        "Improve leadership and communication skills to increase promotion opportunities."
    )

if skill_count < 5:
    insights.append(
        "Learn more modern technologies to improve your employability."
    )

if promotion_score >= 85:
    insights.append(
        "You are ready for senior responsibilities and leadership roles."
    )

if not insights:
    insights.append(
        "Excellent progress! Continue learning and mentoring others."
    )
for item in insights:
    st.success(item)
st.markdown("</div>", unsafe_allow_html=True)
# ==========================================================
# CAREER ACTION CENTER
# ==========================================================

st.markdown('<div class="white-card">', unsafe_allow_html=True)

st.subheader("Career Action Center")

a1, a2, a3 = st.columns(3)

with a1:

    if st.button("🗺 Generate Career Roadmap", use_container_width=True):

        st.success("Personalized Career Roadmap")

        st.write(f"Current Role : {profile.get('current_role','-')}")
        st.write(f"Target Role : {profile.get('preferred_role','-')}")

        st.write("Recommended Actions")

        for skill in skills:
            st.write(f"✔ Improve {skill}")

        st.write("✔ Complete advanced certifications")
        st.write("✔ Build impactful projects")
        st.write("✔ Improve communication")

with a2:

    if st.button("📈 Promotion Analysis", use_container_width=True):

        st.metric(
            "Promotion Readiness",
            f"{promotion_score}%"
        )

        st.progress(promotion_score / 100)

        if promotion_score >= 85:
            st.success("Promotion Highly Recommended")

        elif promotion_score >= 70:
            st.info("Almost Ready for Promotion")

        else:
            st.warning("Needs Improvement")

with a3:

    if st.button("💼 View Matching Jobs", use_container_width=True):

        st.switch_page("pages/job_matching.py")

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# RECOMMENDED JOBS
# ==========================================================

st.markdown('<div class="white-card">', unsafe_allow_html=True)

st.subheader("Recommended Jobs")

for job in job_matches:

    c1, c2 = st.columns([4, 1])

    with c1:

        st.write(f"### {job['role']}")

        st.caption(
            f"{job['company']} • {job['location']}"
        )

    with c2:

        st.metric(
            "Match",
            f"{job['match']}%"
        )

    st.divider()

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# CERTIFICATIONS & INDUSTRY TRENDS
# ==========================================================

left, right = st.columns(2)

with left:

    st.markdown('<div class="white-card">', unsafe_allow_html=True)

    st.subheader("Recommended Certifications")

    for cert in certifications:

        st.write(f"✔ {cert}")

    st.markdown("</div>", unsafe_allow_html=True)

with right:

    st.markdown('<div class="white-card">', unsafe_allow_html=True)
    st.subheader("Industry Trends")
    st.info(
        "View personalized AI-powered industry trends.")

    if st.button("📈 Open Industry Trends"):
        st.switch_page("pages/industry_trends.py")
        st.markdown("</div>", unsafe_allow_html=True)
# ==========================================================
# PERFORMANCE OVERVIEW
# ==========================================================

st.markdown('<div class="white-card">', unsafe_allow_html=True)

st.subheader("📊 Career Performance Analytics")

st.caption(
    "Analyze your technical skills, leadership, promotion readiness, and overall career growth."
)

# Quick summary
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Skill Score", f"{skill_score}%")

with c2:
    st.metric("Promotion", f"{promotion_score}%")

with c3:
    st.metric("Career Growth", f"{career_growth}%")

with c4:
    st.metric("Leadership", f"{leadership}%")

st.divider()

# Performance Chart
chart_data = {
    "Metric": [
        "Skill",
        "Promotion",
        "Career Growth",
        "Leadership"
    ],
    "Score": [
        skill_score,
        promotion_score,
        career_growth,
        leadership
    ]
}

st.bar_chart(
    chart_data,
    x="Metric",
    y="Score"
)

# Overall Insight
average_score = int(
    (skill_score + promotion_score + career_growth + leadership) / 4
)

st.divider()

if average_score >= 85:
    st.success("🌟 Excellent performance! You are on track for senior opportunities.")

elif average_score >= 70:
    st.info("🚀 Good progress. Continue improving leadership and advanced technical skills.")

else:
    st.warning("📈 Focus on upskilling, certifications, and practical experience to accelerate career growth.")

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "TalentSphere Elevate • AI Powered Career Development Platform"
)