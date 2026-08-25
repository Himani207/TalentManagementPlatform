import streamlit as st
from ai.gemini import ask_gemini
from utils.professional_sidebar import professional_sidebar
from utils.professional_theme import load_professional_theme
from utils.professional_db import (
    calculate_skill_score,
    calculate_promotion_score,
    calculate_career_growth,
    calculate_salary_growth,
    get_skill_gap,
    get_learning_roadmap,
    get_future_roles,
    get_certifications
)
# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="AI Career Coach",
    page_icon="🤖",
    layout="wide"
)
load_professional_theme()
# ==========================================================
# LOAD PROFILE
# ==========================================================

profile = professional_sidebar()

if not profile.get("company"):
    st.warning("Please complete your professional profile first.")
    st.switch_page("pages/edit_professional_profile.py")
    st.stop()

# ==========================================================
# SCORES
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

# ==========================================================
# HEADER
# ==========================================================

st.title("🤖 AI Career Coach")

st.caption(
    "Personalized career guidance based on your professional profile."
)
st.divider()
# ==========================================================
# OVERVIEW
# ==========================================================

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric(
        "Skill Score",
        f"{skill_score}%"
    )

with c2:
    st.metric(
        "Promotion",
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

st.divider()

# ==========================================================
# AI CAREER ADVICE
# ==========================================================

st.subheader("🎯 Personalized Career Advice")

advice = []

if experience < 2:
    advice.append(
        "Focus on building strong technical fundamentals and completing real-world projects."
    )

elif experience < 5:
    advice.append(
        "Take ownership of projects and improve leadership skills."
    )

elif experience < 10:
    advice.append(
        "Prepare for senior positions by mentoring juniors and improving architecture skills."
    )

else:
    advice.append(
        "Focus on strategic leadership and organizational impact."
    )

if leadership < 70:
    advice.append(
        "Improve communication and leadership skills."
    )

if skill_score < 80:
    advice.append(
        "Learn modern technologies such as Cloud, Docker and AI."
    )

for item in advice:
    st.success(item)

st.divider()

# ==========================================================
# CAREER GOAL
# ==========================================================

st.subheader("🎯 Your Career Goal")

st.info(
    f"""
Current Role:
{profile.get('current_role')}

Preferred Role:
{profile.get('preferred_role')}

Career Goal:
{profile.get('career_goal')}
"""
)
# ==========================================================
# SKILL GAP ANALYSIS
# ==========================================================

st.subheader("📉 Skill Gap Analysis")
missing_skills = get_skill_gap(profile)
if len(missing_skills) == 0:
    st.success(
        "Excellent! Your profile already covers most industry skills."
    )
else:
    cols = st.columns(3)
    for i, skill in enumerate(missing_skills):
        with cols[i % 3]:
            st.warning(skill)
st.divider()

# ==========================================================
# PROMOTION PLAN
# ==========================================================

st.subheader("🚀 Promotion Strategy")

st.metric(
    "Promotion Readiness",
    f"{promotion_score}%"
)

st.progress(promotion_score / 100)

if promotion_score >= 85:

    st.success(
        "You are ready for promotion."
    )

elif promotion_score >= 70:

    st.info(
        "You are close to promotion. Continue improving leadership."
    )

else:

    st.warning(
        "Focus on certifications, leadership and business impact."
    )

st.divider()

# ==========================================================
# LEARNING ROADMAP
# ==========================================================

st.subheader("📚 Personalized Learning Roadmap")
roadmap = get_learning_roadmap(profile)
for item in roadmap:
    st.write(
        f"✅ {item['skill']} ({item['duration']}) - {item['priority']} Priority"
    )
st.divider()

# ==========================================================
# SALARY GROWTH STRATEGY
# ==========================================================

st.subheader("💰 Salary Growth Strategy")

st.metric(
    "Expected Salary Growth",
    f"+{salary_growth}%"
)

st.progress(min(salary_growth, 100) / 100)
salary_tips = []
if skill_score < 80:
    salary_tips.append("Learn advanced technical skills.")
if leadership < 70:
    salary_tips.append("Improve leadership abilities.")
if promotion_score < 80:
    salary_tips.append("Take ownership of high-impact projects.")
for cert in get_certifications(profile):
    salary_tips.append(f"Complete {cert}")
for tip in salary_tips:
    st.write(f"✔ {tip}")
st.divider()
# ==========================================================
# CAREER SWITCH SUGGESTIONS
# ==========================================================

st.subheader("🔄 Career Switch Suggestions")
career_options = get_future_roles(profile)
for role in career_options:
    st.success(f"💼 {role}")
st.divider()
# CERTIFICATIONAS
st.subheader("📜 Recommended Certifications")
for cert in get_certifications(profile):
    st.success(cert)
# ==========================================================
# LEADERSHIP RECOMMENDATIONS
# ==========================================================

st.subheader("👥 Leadership Recommendations")

leadership_tips = []

if leadership < 60:
    leadership_tips = [
        "Improve communication skills.",
        "Take ownership of projects.",
        "Mentor junior developers."
    ]

elif leadership < 80:

    leadership_tips = [
        "Lead cross-functional teams.",
        "Improve strategic thinking.",
        "Handle client communication."
    ]
else:

    leadership_tips = [
        "Drive organizational initiatives.",
        "Mentor engineering managers.",
        "Build high-performing teams."
    ]
for tip in leadership_tips:

    st.info(tip)

st.divider()
# ==========================================================
# ASK AI CAREER COACH
#===========================================================
if "career_chat" not in st.session_state:
    st.session_state.career_chat = {}
st.subheader("💬 Ask AI Career Coach")
question = st.text_input(
    "Ask your career question"
)
if st.button(
    "🤖 Get AI Advice",
    use_container_width=True
):

    if not question.strip():
        st.warning("Please enter a question.")

    else:
        with st.spinner("AI is analyzing your profile..."):
            prompt = f"""
You are an expert AI Career Coach.

Professional Profile

Name: {profile.get('full_name')}

Current Role: {profile.get('current_role')}

Company: {profile.get('company')}

Experience: {profile.get('experience')} years

Technical Skills:
{profile.get('technical_skills')}

Career Goal:
{profile.get('career_goal')}

Preferred Role:
{profile.get('preferred_role')}

Leadership Score:
{leadership}

Skill Score:
{skill_score}

Promotion Readiness:
{promotion_score}

Career Growth:
{career_growth}

Expected Salary Growth:
{salary_growth}

User Question:
{question}

Provide personalized career guidance.

Include:
1. Career advice
2. Skills to improve
3. Certifications
4. Next career steps
5. Estimated timeline

Keep the answer professional, practical and easy to understand.
"""  
            cache_key = f"{profile['email']}::{question.strip().lower()}"
            if cache_key in st.session_state.career_chat:
                response = st.session_state.career_chat[question]
            else:
                response = ask_gemini(prompt)
                st.session_state.career_chat[question] = response
            st.success(response)
# ==========================================================
# DAILY CAREER TIPS
# ==========================================================

st.divider()
st.subheader("📅 Daily Career Tips")
tips = [

    "Spend at least 30 minutes learning a new skill.",

    "Read one technical article every day.",

    "Contribute to GitHub regularly.",

    "Practice communication and presentation skills.",

    "Update your resume after every major achievement."

]

for tip in tips:

    st.write(f"✅ {tip}")

# ==========================================================
# PERSONALIZED ACTION PLAN
# ==========================================================

st.divider()

st.subheader("🎯 Your Action Plan")

actions = []

if skill_score < 80:

    actions.append("Improve technical skills.")

if promotion_score < 80:

    actions.append("Increase leadership experience.")

if salary_growth < 20:

    actions.append("Complete advanced certifications.")

if experience < 5:

    actions.append("Lead at least one major project.")

actions.append("Review career goals every 3 months.")

for action in actions:

    st.success(action)

# ==========================================================
# PROFILE SUMMARY
# ==========================================================

st.divider()

st.subheader("📊 Career Snapshot")

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "Experience",
        f"{experience} Years"
    )

with c2:

    st.metric(
        "Leadership",
        f"{leadership}%"
    )

with c3:

    st.metric(
        "Skills",
        len(skills)
    )

# ==========================================================
# QUICK NAVIGATION
# ==========================================================

st.divider()

col1, col2, col3 = st.columns(3)

with col1:

    if st.button(
        "👤 My Profile",
        use_container_width=True
    ):

        st.switch_page(
            "pages/professional_profile.py"
        )

with col2:

    if st.button(
        "💼 Job Matching",
        use_container_width=True
    ):

        st.switch_page(
            "pages/professional_job_matching.py"
        )

with col3:

    if st.button(
        "📊 Career Analytics",
        use_container_width=True
    ):

        st.switch_page(
            "pages/career_analytics.py"
        )

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "TalentSphere Elevate • AI Career Coach for Working Professionals 🚀"
)