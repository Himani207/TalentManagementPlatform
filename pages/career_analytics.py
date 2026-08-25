import streamlit as st
import pandas as pd
from utils.professional_db import get_skill_gap
from utils.professional_sidebar import professional_sidebar
from utils.professional_theme import load_professional_theme
from utils.professional_db import get_learning_roadmap
from utils.professional_db import (
    calculate_skill_score,
    calculate_promotion_score,
    calculate_career_growth,
    calculate_salary_growth
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Career Analytics",
    page_icon="📊",
    layout="wide"
)
load_professional_theme()
# ==========================================================
# LOAD SIDEBAR
# ==========================================================

profile = professional_sidebar()

# ==========================================================
# PROFILE CHECK
# ==========================================================

if not profile.get("company"):
    st.warning("Please complete your professional profile first.")
    st.switch_page("pages/edit_professional_profile.py")
    st.stop()

# ==========================================================
# CALCULATIONS
# ==========================================================

skill_score = calculate_skill_score(profile)

promotion_score = calculate_promotion_score(profile)

career_growth = calculate_career_growth(profile)

salary_growth = calculate_salary_growth(profile)

experience = int(profile.get("experience", 0))

leadership = int(profile.get("leadership", 0))

skills = [
    skill.strip()
    for skill in profile.get("technical_skills", "").split(",")
    if skill.strip()
]

skill_count = len(skills)

# ==========================================================
# HEADER
# ==========================================================

st.title("📊 Career Analytics")

st.caption(
    "Track your career growth and analyze your professional performance."
)

st.divider()

# ==========================================================
# KPI CARDS
# ==========================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Skill Score",
        f"{skill_score}%"
    )

with c2:
    st.metric(
        "Promotion Readiness",
        f"{promotion_score}%"
    )

with c3:
    st.metric(
        "Career Growth",
        f"{career_growth}%"
    )

with c4:
    st.metric(
        "Salary Growth",
        f"+{salary_growth}%"
    )

st.write("")

# ==========================================================
# PROFESSIONAL SUMMARY
# ==========================================================

left, right = st.columns([2, 1])

with left:

    st.subheader("Professional Overview")

    st.info(f"""
**Current Role:** {profile.get("current_role","-")}

**Company:** {profile.get("company","-")}

**Experience:** {experience} Years

**Preferred Role:** {profile.get("preferred_role","-")}
""")

with right:

    st.subheader("Quick Stats")

    st.metric(
        "Technical Skills",
        skill_count
    )

    st.metric(
        "Leadership",
        f"{leadership}%"
    )

st.divider()

# ==========================================================
# PERFORMANCE PROGRESS
# ==========================================================

st.subheader("Performance Progress")

p1, p2 = st.columns(2)

with p1:

    st.write("Technical Skills")

    st.progress(skill_score / 100)

    st.write("Leadership")

    st.progress(leadership / 100)

with p2:

    st.write("Promotion Readiness")

    st.progress(promotion_score / 100)

    st.write("Career Growth")

    st.progress(career_growth / 100)

st.divider()

# ==========================================================
# PERFORMANCE CHART
# ==========================================================

st.subheader("Performance Overview")

chart_df = pd.DataFrame({
    "Metric": [
        "Skills",
        "Leadership",
        "Promotion",
        "Career Growth"
    ],
    "Score": [
        skill_score,
        leadership,
        promotion_score,
        career_growth
    ]
})

st.bar_chart(
    chart_df,
    x="Metric",
    y="Score"
)

st.divider()

# ==========================================================
# EXPERIENCE ANALYSIS
# ==========================================================

st.subheader("Experience Analysis")

if experience < 2:

    st.warning(
        "You are in the early stage of your career. Focus on learning and gaining practical experience."
    )

elif experience < 5:

    st.info(
        "You are progressing well. Strengthen your technical expertise and leadership skills."
    )

elif experience < 10:

    st.success(
        "You are at a senior level. Prepare for management and strategic responsibilities."
    )

else:

    st.success(
        "You are an experienced professional. Focus on mentoring, innovation, and organizational leadership."
    )

st.divider()

# ==========================================================
# SKILL ANALYSIS
# ==========================================================

st.subheader("Technical Skill Analysis")

if skills:

    skill_df = pd.DataFrame({
        "Skill": skills,
        "Proficiency": [
            min(60 + i * 8, 100)
            for i in range(len(skills))
        ]
    })

    st.dataframe(
        skill_df,
        use_container_width=True
    )

else:

    st.info("No technical skills added.")
# ==========================================================
# SKILL GAP ANALYSIS
# ==========================================================

st.divider()

st.subheader("📉 Skill Gap Analysis")
missing_skills = get_skill_gap(profile)
if missing_skills:

    st.warning("Recommended Skills to Learn")

    cols = st.columns(3)

    for i, skill in enumerate(missing_skills):

        with cols[i % 3]:
            st.info(skill)

else:

    st.success("Excellent! Your skill profile is strong.")

# ==========================================================
# AI CAREER INSIGHTS
# ==========================================================

st.divider()

st.subheader("🤖 AI Career Insights")

insights = []

if experience < 3:
    insights.append(
        "Gain more hands-on industry experience by working on challenging projects."
    )

if leadership < 70:
    insights.append(
        "Improve leadership and communication skills for faster promotions."
    )

if promotion_score < 70:
    insights.append(
        "Focus on certifications and measurable business impact."
    )

if salary_growth < 15:
    insights.append(
        "Learning cloud technologies and AI can significantly improve salary growth."
    )

if career_growth >= 85:
    insights.append(
        "You are ready for senior-level opportunities."
    )

if len(insights) == 0:
    insights.append(
        "Excellent profile! Continue learning and mentoring others."
    )

for item in insights:
    st.success(item)

# ==========================================================
# PROMOTION READINESS
# ==========================================================

st.divider()

st.subheader("🚀 Promotion Readiness")

st.metric(
    "Promotion Score",
    f"{promotion_score}%"
)

st.progress(promotion_score / 100)

if promotion_score >= 85:

    st.success("Promotion Highly Recommended")

elif promotion_score >= 70:

    st.info("You are close to your next promotion.")

else:

    st.warning(
        "Improve technical expertise and leadership before your next promotion."
    )

# ==========================================================
# SALARY GROWTH PREDICTION
# ==========================================================

st.divider()

st.subheader("💰 Salary Growth Prediction")

st.metric(
    "Expected Salary Growth",
    f"+{salary_growth}%"
)

st.progress(min(salary_growth, 100) / 100)

if salary_growth >= 25:

    st.success("Excellent salary growth potential.")

elif salary_growth >= 15:

    st.info("Good salary growth expected.")

else:

    st.warning(
        "Upskilling can increase your salary growth."
    )

# ==========================================================
# LEARNING ROADMAP
# ==========================================================
# ==========================================================
# LEARNING ROADMAP
# ==========================================================

st.divider()
st.subheader("📚 Personalized Learning Roadmap")
roadmap = get_learning_roadmap(profile)
if roadmap:
    for item in roadmap:
        st.write(
            f"✅ {item['skill']} ({item['duration']}) - {item['priority']} Priority"
        )
else:
    st.success("🎉 Great! No major skill gaps found.")
# ==========================================================
# NEXT CAREER STEPS
# ==========================================================

st.divider()

st.subheader("🎯 Recommended Next Steps")

steps = []

if skill_score < 80:
    steps.append("Improve technical skills.")

if leadership < 75:
    steps.append("Participate in leadership programs.")

if promotion_score < 80:
    steps.append("Lead high-impact projects.")

if len(missing_skills) > 0:
    steps.append(f"Learn {missing_skills[0]}.")

steps.append("Update your resume every 6 months.")

for step in steps:

    st.write(f"✔ {step}")

# ==========================================================
# CAREER TIMELINE
# ==========================================================

st.divider()

st.subheader("📅 Career Timeline")

timeline = {
    "Stage": [
        "Current",
        "6 Months",
        "1 Year",
        "3 Years"
    ],
    "Goal": [
        profile.get("current_role", ""),
        "Advanced Skills",
        profile.get("preferred_role", ""),
        "Leadership Position"
    ]
}

st.table(pd.DataFrame(timeline))

# ==========================================================
# QUICK ACTIONS
# ==========================================================

st.divider()

c1, c2, c3 = st.columns(3)

with c1:

    if st.button(
        "👤 View Profile",
        use_container_width=True
    ):
        st.switch_page("pages/professional_profile.py")

with c2:

    if st.button(
        "✏ Edit Profile",
        use_container_width=True
    ):
        st.switch_page("pages/edit_professional_profile.py")

with c3:

    if st.button(
        "💼 Job Matching",
        use_container_width=True
    ):
        st.switch_page("pages/job_matching.py")

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "TalentSphere Elevate • AI Powered Career Analytics"
)