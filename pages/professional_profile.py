import streamlit as st
from utils.professional_sidebar import professional_sidebar
from utils.professional_theme import load_professional_theme
from utils.professional_db import get_profile
# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="My Profile",
    page_icon="👤",
    layout="wide"
)
load_professional_theme()
# ==========================================================
# LOAD SIDEBAR & PROFILE
# ==========================================================
profile = professional_sidebar()

if profile:
    profile = get_profile(profile["email"])
else:
    st.warning("Profile not found")
    st.stop()
# ==========================================================
# PROFILE COMPLETION
# ==========================================================

fields = [
    "full_name",
    "phone",
    "location",
    "company",
    "current_role",
    "experience",
    "technical_skills",
    "soft_skills",
    "career_goal",
    "preferred_role",
    "leadership",
    "work_experience",
    "achievements",
    "certifications",
    "linkedin",
    "github"
]

filled = sum(
    1 for field in fields
    if profile.get(field)
)

completion = int((filled / len(fields)) * 100)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

.profile-card{
background:white;
padding:25px;
border-radius:18px;
border:1px solid #E5E7EB;
box-shadow:0 4px 12px rgba(0,0,0,.05);
margin-bottom:20px;
}

.profile-banner{
height:180px;
border-radius:20px;
background:linear-gradient(135deg,#2563EB,#7C3AED);
margin-bottom:25px;
}

.avatar{
width:120px;
height:120px;
border-radius:50%;
background:white;
display:flex;
align-items:center;
justify-content:center;
font-size:60px;
margin-top:-70px;
border:5px solid white;
box-shadow:0 5px 15px rgba(0,0,0,.15);
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# BANNER
# ==========================================================

st.markdown(
"""
<div class="profile-banner"></div>
""",
unsafe_allow_html=True
)

# ==========================================================
# HEADER
# ==========================================================

c1, c2 = st.columns([1,4])

with c1:

    st.markdown(
    """
    <div class="avatar">
    💼
    </div>
    """,
    unsafe_allow_html=True
    )

with c2:

    st.markdown(
    f"""
    <div class="profile-card">

    <h1 style="margin-bottom:0;">
    {profile.get("full_name","Professional")}
    </h1>

    <h3 style="color:#6B7280;">
    {profile.get("current_role","Professional")}
    </h3>

    <p>
    🏢 {profile.get("company","Not Provided")}
    </p>

    <p>
    📍 {profile.get("location","Not Provided")}
    </p>

    <p>
    🕒 {profile.get("experience",0)} Years Experience
    </p>

    </div>
    """,
    unsafe_allow_html=True
    )

st.markdown("### 📊 Profile Completion")

st.progress(completion / 100)

st.caption(f"{completion}% Completed")

# ==========================================================
# ACTION BUTTONS
# ==========================================================

b1, b2 = st.columns(2)

with b1:

    if st.button(
        "✏ Edit Profile",
        use_container_width=True
    ):
        st.switch_page(
            "pages/edit_professional_profile.py"
        )

with b2:

    if st.button(
        "📄 Resume Analyzer",
        use_container_width=True
    ):
        st.switch_page(
            "pages/resume_analyzer.py"
        )

# ==========================================================
# PROFESSIONAL INFORMATION
# ==========================================================

st.markdown(
'<div class="profile-card">',
unsafe_allow_html=True
)

st.subheader("👤 Professional Information")

left, right = st.columns(2)

with left:

    st.text_input(
        "Full Name",
        value=profile.get("full_name",""),
        disabled=True
    )

    st.text_input(
        "Phone",
        value=profile.get("phone",""),
        disabled=True
    )

    st.text_input(
        "Company",
        value=profile.get("company",""),
        disabled=True
    )

    st.text_input(
        "Location",
        value=profile.get("location",""),
        disabled=True
    )

with right:

    st.text_input(
        "Current Role",
        value=profile.get("current_role",""),
        disabled=True
    )

    st.text_input(
        "Experience",
        value=f"{profile.get('experience',0)} Years",
        disabled=True
    )

    st.text_input(
        "Leadership Score",
        value=f"{profile.get('leadership',0)}%",
        disabled=True
    )

    st.text_input(
        "Email",
        value=profile.get("email",""),
        disabled=True
    )

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# CAREER INFORMATION
# ==========================================================

st.markdown(
'<div class="profile-card">',
unsafe_allow_html=True
)

st.subheader("🎯 Career Information")

c1, c2 = st.columns(2)

with c1:

    st.info(
        profile.get(
            "career_goal",
            "Not Added"
        )
    )

with c2:

    st.info(
        profile.get(
            "preferred_role",
            "Not Added"
        )
    )
st.markdown("</div>", unsafe_allow_html=True)
# ==========================================================
# TECHNICAL SKILLS
# ==========================================================

st.markdown('<div class="profile-card">', unsafe_allow_html=True)

st.subheader("💻 Technical Skills")

technical_skills = [
    skill.strip()
    for skill in (profile.get("technical_skills") or "").split(",")
    if skill.strip()
]

if technical_skills:

    cols = st.columns(4)

    for i, skill in enumerate(technical_skills):

        with cols[i % 4]:
            st.success(skill)

else:

    st.info("No technical skills added.")

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# SOFT SKILLS
# ==========================================================

st.markdown('<div class="profile-card">', unsafe_allow_html=True)

st.subheader("🤝 Soft Skills")
soft_skills = [
    skill.strip()
    for skill in (profile.get("soft_skills") or "").split(",")
    if skill.strip()
]
if soft_skills:
    cols = st.columns(3)

    for i, skill in enumerate(soft_skills):

        with cols[i % 3]:
            st.info(skill)

else:

    st.info("No soft skills added.")

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# WORK EXPERIENCE
# ==========================================================

st.markdown('<div class="profile-card">', unsafe_allow_html=True)
st.subheader("🏢 Work Experience")
work_experience = profile.get("work_experience") or ""
if work_experience:
    st.write(work_experience)
else:
    st.warning("No work experience added.")
st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# ACHIEVEMENTS
# ==========================================================

st.markdown('<div class="profile-card">', unsafe_allow_html=True)

st.subheader("🏆 Achievements")

achievements = [
    item.strip()
    for item in (profile.get("achievements") or "").split(",")
    if item.strip()
]

if achievements:

    for achievement in achievements:
        st.success(f"🏅 {achievement}")

else:

    st.info("No achievements added.")

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# CERTIFICATIONS
# ==========================================================

st.markdown('<div class="profile-card">', unsafe_allow_html=True)

st.subheader("📜 Certifications")

certifications = [
    cert.strip()
    for cert in (profile.get("certifications") or "").split(",")
    if cert.strip()
]

if certifications:

    for cert in certifications:
        st.info(f"📘 {cert}")

else:

    st.info("No certifications added.")

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# PROFESSIONAL LINKS
# ==========================================================

st.markdown('<div class="profile-card">', unsafe_allow_html=True)

st.subheader("🔗 Professional Links")

c1, c2 = st.columns(2)

with c1:

    linkedin = profile.get("linkedin", "")

    if linkedin:

        st.markdown(f"**LinkedIn**  \n{linkedin}")

    else:

        st.caption("LinkedIn profile not added.")

with c2:

    github = profile.get("github", "")

    if github:

        st.markdown(f"**GitHub**  \n{github}")

    else:

        st.caption("GitHub profile not added.")

st.markdown("</div>", unsafe_allow_html=True)
# ==========================================================
# AI CAREER INSIGHTS
# ==========================================================

st.markdown('<div class="profile-card">', unsafe_allow_html=True)

st.subheader("🤖 AI Career Insights")

insights = []

if int(profile.get("experience", 0)) < 3:
    insights.append(
        "Gain more hands-on project experience to accelerate career growth."
    )

if int(profile.get("leadership", 0)) < 70:
    insights.append(
        "Improve leadership and communication skills."
    )
if len(technical_skills) < 5:
    insights.append(
        "Improve your technical skills by learning more industry-relevant technologies."
    )
if not insights:

    insights.append(
        "Excellent profile! Keep learning and expanding your expertise."
    )

for insight in insights:

    st.success(insight)

st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "TalentSphere Elevate • AI Powered Career Development Platform"
)