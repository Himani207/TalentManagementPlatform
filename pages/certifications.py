import streamlit as st

from utils.professional_sidebar import professional_sidebar
from utils.professional_db import get_certifications
from utils.professional_theme import load_professional_theme
# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Recommended Certifications",
    page_icon="📜",
    layout="wide"
)
load_professional_theme()
# ==========================================================
# LOAD PROFILE
# ==========================================================

profile = professional_sidebar()

if profile is None:

    st.warning(
        "Please complete your professional profile first."
    )

    st.switch_page(
        "pages/edit_professional_profile.py"
    )

    st.stop()

# ==========================================================
# PROFILE DATA
# ==========================================================

experience = int(profile.get("experience", 0))

current_role = profile.get(
    "current_role",
    "Not Added"
)

preferred_role = profile.get(
    "preferred_role",
    "Not Added"
)

career_goal = profile.get(
    "career_goal",
    "Not Added"
)

company = profile.get(
    "company",
    "Not Added"
)

skills = [

    skill.strip()

    for skill in profile.get(
        "technical_skills",
        ""
    ).split(",")

    if skill.strip()

]

# ==========================================================
# LOAD DYNAMIC CERTIFICATIONS
# ==========================================================

certifications = get_certifications(profile)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

.cert-card{

background:white;
padding:25px;
border-radius:18px;
border:1px solid #E5E7EB;
box-shadow:0 5px 15px rgba(0,0,0,.06);
margin-bottom:20px;

}

.metric-card{

background:white;
padding:18px;
border-radius:16px;
border:1px solid #E5E7EB;
text-align:center;
box-shadow:0 4px 12px rgba(0,0,0,.05);

}

</style>
""",
unsafe_allow_html=True)

# ==========================================================
# HEADER
# ==========================================================

st.title("📜 Recommended Certifications")

st.caption(
    "Personalized certification recommendations based on your professional profile."
)

st.divider()

# ==========================================================
# PROFILE SUMMARY
# ==========================================================

st.subheader("👤 Professional Profile")

c1, c2, c3, c4 = st.columns(4)

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
        "Company",
        company
    )

with c4:

    st.metric(
        "Career Goal",
        preferred_role
    )

# ==========================================================
# TECHNICAL SKILLS
# ==========================================================

st.divider()

st.subheader("💻 Your Technical Skills")

if skills:

    cols = st.columns(4)

    for i, skill in enumerate(skills):

        with cols[i % 4]:

            st.info(skill)

else:

    st.warning(
        "No technical skills added. Add skills to receive better certification recommendations."
    )

# ==========================================================
# CERTIFICATION READINESS
# ==========================================================

st.divider()

st.subheader("📊 Certification Readiness")

readiness = min(len(certifications) * 20, 100)

c1, c2 = st.columns([1,3])

with c1:

    st.metric(
        "Readiness",
        f"{readiness}%"
    )

with c2:

    st.progress(
        readiness / 100
    )

st.caption(
    "Your readiness score is calculated from your profile completeness, technical skills, and recommended certifications."
)
# ==========================================================
# CERTIFICATION SECTION STARTS HERE
# ==========================================================
st.divider()
st.subheader("🎯 Recommended Certifications")
# ==========================================================
# DYNAMIC CERTIFICATION CARDS
# ==========================================================

if certifications:

    for cert in certifications:

        # --------------------------------------------------
        # Difficulty
        # --------------------------------------------------

        if experience < 2:
            difficulty = "Beginner"
            duration = "1 - 2 Months"

        elif experience < 5:
            difficulty = "Intermediate"
            duration = "2 - 3 Months"

        else:
            difficulty = "Advanced"
            duration = "3 - 6 Months"

        # --------------------------------------------------
        # Priority
        # --------------------------------------------------

        if cert in certifications[:2]:
            priority = "⭐⭐⭐ High"

        elif cert in certifications[2:4]:
            priority = "⭐⭐ Medium"

        else:
            priority = "⭐ Low"

        # --------------------------------------------------
        # Recommendation Reason
        # --------------------------------------------------

        cert_lower = cert.lower()

        if "aws" in cert_lower or "azure" in cert_lower or "cloud" in cert_lower:

            reason = (
                "Recommended because Cloud Computing is one of the most in-demand skills."
            )

        elif "docker" in cert_lower or "kubernetes" in cert_lower:

            reason = (
                "Containerization and DevOps skills are highly valued by employers."
            )

        elif "python" in cert_lower:

            reason = (
                "Strengthens programming and automation skills."
            )

        elif "data" in cert_lower:

            reason = (
                "Excellent for analytics, AI, and data-driven careers."
            )

        elif "ai" in cert_lower or "machine learning" in cert_lower:

            reason = (
                "AI skills significantly improve future career opportunities."
            )

        elif "security" in cert_lower:

            reason = (
                "Cybersecurity professionals are in high demand worldwide."
            )

        else:

            reason = (
                f"Recommended based on your role as {current_role} and your career goal."
            )

        # --------------------------------------------------
        # CARD
        # --------------------------------------------------

        with st.container(border=True):

            st.subheader(f"📘 {cert}")

            c1, c2 = st.columns([3, 1])

            with c1:

                st.write(
                    f"**Recommendation:** {reason}"
                )

                st.write(
                    f"**Estimated Duration:** {duration}"
                )

                st.write(
                    f"**Difficulty:** {difficulty}"
                )

            with c2:

                st.metric(
                    "Priority",
                    priority
                )

                st.success("Recommended")

else:

    st.info(
        "No certification recommendations available. Please update your professional profile."
    )

st.divider()
# ==========================================================
# DYNAMIC LEARNING STRATEGY
# ==========================================================

st.subheader("🚀 Personalized Certification Roadmap")

roadmap = []

if experience < 2:

    roadmap = [
        "Complete one beginner certification.",
        "Build 2-3 portfolio projects.",
        "Practice coding daily.",
        "Upload certificates to LinkedIn.",
        "Prepare for technical interviews."
    ]

elif experience < 5:

    roadmap = [
        "Complete one cloud certification.",
        "Learn System Design.",
        "Earn a DevOps certification.",
        "Lead a project at work.",
        "Strengthen leadership skills."
    ]

else:

    roadmap = [
        "Complete advanced cloud certification.",
        "Earn architecture certification.",
        "Mentor junior professionals.",
        "Improve business and leadership skills.",
        "Prepare for senior management roles."
    ]

for step in roadmap:

    st.write(f"✅ {step}")

# ==========================================================
# CERTIFICATION TIMELINE
# ==========================================================

st.divider()

st.subheader("📅 Suggested Learning Timeline")

timeline = []

for i, cert in enumerate(certifications):

    timeline.append({
        "Month": f"Month {i+1}",
        "Certification": cert
    })

if timeline:

    st.table(timeline)

# ==========================================================
# PERSONALIZED NEXT STEPS
# ==========================================================

st.divider()

st.subheader("🎯 Recommended Next Steps")

next_steps = []

if len(skills) < 5:

    next_steps.append(
        "Expand your technical skill set."
    )

if experience < 3:

    next_steps.append(
        "Gain more practical project experience."
    )

if "cloud" not in profile.get(
    "technical_skills",
    ""
).lower():

    next_steps.append(
        "Learn Cloud Computing."
    )

if "docker" not in profile.get(
    "technical_skills",
    ""
).lower():

    next_steps.append(
        "Learn Docker and containerization."
    )

if "leadership" not in profile.get(
    "soft_skills",
    ""
).lower():

    next_steps.append(
        "Improve leadership and communication skills."
    )

next_steps.append(
    "Update your resume after every certification."
)

next_steps.append(
    "Apply your learning by building real-world projects."
)

for step in next_steps:

    st.success(step)

# ==========================================================
# PROFESSIONAL TIP
# ==========================================================

st.divider()

st.subheader("💡 Career Tip")

if experience < 2:

    st.info(
        "Focus on building a strong technical foundation before pursuing advanced certifications."
    )

elif experience < 5:

    st.info(
        "Choose certifications that align with your preferred career role and help you qualify for promotions."
    )

else:

    st.info(
        "Advanced certifications and leadership training will have the greatest impact on your career growth."
    )

# ==========================================================
# QUICK ACTIONS
# ==========================================================

st.divider()

st.subheader("⚡ Quick Actions")

c1, c2, c3 = st.columns(3)

with c1:

    if st.button(
        "👤 My Profile",
        use_container_width=True
    ):

        st.switch_page(
            "pages/professional_profile.py"
        )

with c2:

    if st.button(
        "📊 Career Analytics",
        use_container_width=True
    ):

        st.switch_page(
            "pages/career_analytics.py"
        )

with c3:

    if st.button(
        "🤖 AI Career Coach",
        use_container_width=True
    ):

        st.switch_page(
            "pages/ai_career_coach.py"
        )

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "TalentSphere Elevate • AI Powered Professional Growth Platform 🚀"
)
