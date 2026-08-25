import streamlit as st
from utils.professional_sidebar import professional_sidebar
from utils.professional_theme import load_professional_theme
from utils.professional_db import (
    calculate_promotion_readiness,
    generate_promotion_recommendation
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Promotion Readiness",
    page_icon="📈",
    layout="wide"
)
load_professional_theme()
# ==========================================================
# LOAD PROFILE
# ==========================================================

profile = professional_sidebar()
result = calculate_promotion_readiness(profile)
# ==========================================================
# CSS
# ==========================================================

st.markdown("""
<style>

.metric-card{
background:white;
padding:20px;
border-radius:15px;
border:1px solid #E5E7EB;
box-shadow:0px 4px 10px rgba(0,0,0,0.05);
text-align:center;
margin-bottom:15px;
}

.white-card{
background:white;
padding:25px;
border-radius:18px;
border:1px solid #E5E7EB;
box-shadow:0 4px 12px rgba(0,0,0,.05);
margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# HEADER
# ==========================================================

st.title("📈 Promotion Readiness")

st.caption(
    "AI evaluates your promotion readiness using your profile."
)

st.divider()

# ==========================================================
# PROMOTION SCORE
# ==========================================================

score = result["promotion_score"]

st.metric(
    "Overall Promotion Readiness",
    f"{score}%"
)

st.progress(score/100)

# ==========================================================
# SCORE BREAKDOWN
# ==========================================================

st.markdown('<div class="white-card">', unsafe_allow_html=True)

st.subheader("📊 Score Breakdown")

c1,c2,c3,c4,c5 = st.columns(5)

with c1:
    st.metric(
        "Experience",
        f"{result['experience_score']}%"
    )

with c2:
    st.metric(
        "Skills",
        f"{result['skill_score']}%"
    )

with c3:
    st.metric(
        "Leadership",
        f"{result['leadership_score']}%"
    )

with c4:
    st.metric(
        "Resume",
        f"{result['resume_score']}%"
    )

with c5:
    st.metric(
        "Certifications",
        f"{result['certification_score']}%"
    )

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# PROGRESS
# ==========================================================

st.markdown('<div class="white-card">', unsafe_allow_html=True)

st.subheader("📈 Progress")

st.write("Experience")
st.progress(result["experience_score"]/100)

st.write("Technical Skills")
st.progress(result["skill_score"]/100)

st.write("Leadership")
st.progress(result["leadership_score"]/100)

st.write("Resume")
st.progress(result["resume_score"]/100)

st.write("Certifications")
st.progress(result["certification_score"]/100)

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# READINESS STATUS
# ==========================================================

st.markdown('<div class="white-card">', unsafe_allow_html=True)

st.subheader("🏆 Promotion Status")

if score >= 90:

    st.success(
        "Excellent! You are highly ready for promotion."
    )

elif score >= 75:

    st.info(
        "Very Good! You are close to promotion."
    )

elif score >= 60:

    st.warning(
        "Average readiness. Improve a few key areas."
    )

else:

    st.error(
        "Promotion readiness is currently low."
    )

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# NEXT STEPS
# ==========================================================

st.markdown('<div class="white-card">', unsafe_allow_html=True)

st.subheader("🎯 Recommended Next Steps")

if result["experience_score"] < 80:
    st.write("✅ Gain more hands-on industry experience.")

if result["skill_score"] < 80:
    st.write("✅ Learn advanced technical skills.")

if result["leadership_score"] < 70:
    st.write("✅ Improve leadership and communication.")

if result["resume_score"] < 75:
    st.write("✅ Improve your resume using AI Resume Analyzer.")

if result["certification_score"] < 60:
    st.write("✅ Complete industry-recognized certifications.")

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# AI PROMOTION ANALYSIS
# ==========================================================

st.markdown('<div class="white-card">', unsafe_allow_html=True)

st.subheader("🤖 AI Promotion Recommendation")

if st.button(
    "Generate AI Promotion Analysis",
    use_container_width=True
):

    with st.spinner("Analyzing your profile..."):

        report = generate_promotion_recommendation(profile)

    st.markdown(report)

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "TalentSphere Elevate • AI Powered Career Development Platform"
)