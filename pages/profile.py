import streamlit as st
from utils.session import logout
from utils.college_db import get_profile



# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="My Profile",
    page_icon="👤",
    layout="wide"
)


# ==========================================================
# LOGIN CHECK
# ==========================================================

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.switch_page("pages/login.py")


# ==========================================================
# GET LOGGED IN USER PROFILE
# ==========================================================

email = st.session_state.email
profile = get_profile(email)
if profile is None:
    st.warning("Profile not found. Please complete your profile first.")
    st.page_link("pages/edit_profile.py", label="✏ Complete Profile")
    st.stop()
# ==========================================================
# LOAD CSS
# ==========================================================

def load_css():
    with open("assets/style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()
st.markdown("""
<div class="profile-banner"></div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1,4])
with col1:
    st.markdown("""
    <div class="profile-avatar">
        👤
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(
        f"""
        <div style="
        background:white;
        padding:30px;
        border-radius:18px;
        box-shadow:0 8px 30px rgba(0,0,0,.08);
        ">
        <h1 style="margin:0;color:#222;">
            {profile["full_name"]}
        </h1>
        <h3 style="color:#6b7280;margin-top:10px;">
            {profile["degree"]} Student • {profile["department"]}
        </h3>
        <p>📍 {profile["location"]}</p>

        <p>🏫 {profile["college"]}</p>
        </div>
        """,unsafe_allow_html=True)
    c1, c2 = st.columns(2)
with c1:
    if st.button(
        "✏ Edit Profile",
        use_container_width=True
    ):
        st.switch_page("pages/edit_profile.py")


with c2:

    if st.button(
        "📄 Download Resume",
        use_container_width=True
    ):
        st.switch_page("pages/resume_builder.py")

   
# personal info
st.subheader("👤Personal Information")

c1, c2 = st.columns(2)

with c1:

    st.text_input(
        "Full Name",
        value=profile["full_name"] if profile else "",
        disabled=True
    )


    st.text_input(
        "Email",
        value=email,
        disabled=True
    )


    st.text_input(
        "Phone",
        value=profile["phone"] if profile else "",
        disabled=True
    )


with c2:

    st.text_input(
        "Location",
        value=profile["location"] if profile else "",
        disabled=True
    )
#Academic info
st.subheader("🎓 Academic Information")

c1, c2 = st.columns(2)

with c1:
    st.text_input(
    "College",
    value=profile["college"] if profile else "",
    disabled=True
)
    
    st.text_input(
    "Degree",
    value=profile["degree"] if profile else "",
    disabled=True
)

with c2:
    st.text_input(
    "Branch",
    value=profile["department"] if profile else "",
    disabled=True
)
    st.text_input(
    "CGPA",
    value=profile["cgpa"] if profile else "",
    disabled=True
)
   

#skills
st.subheader("💻 Technical Skills")
skills = []

if profile and profile["skills"]:
    skills = profile["skills"].split(",")

cols = st.columns(4)

for i, skill in enumerate(skills):

    with cols[i % 4]:
        st.success(skill)
#projects
st.subheader("🚀 Projects")

if profile and profile["projects"]:

    st.info(
        profile["projects"]
    )

else:

    st.warning(
        "No projects added yet."
    )
#certifications
st.subheader("📜 Certifications")

if profile and profile["certifications"]:

    for cert in profile["certifications"].split(","):
        st.success(cert.strip())

else:
    st.warning("No certifications added.")
#career goals
st.subheader("🎯 Career Goals")

st.write(
    profile["career_goals"]
    if profile else
    "No career goal added."
)
#AI insights
st.subheader("🤖 AI Career Insights")
if profile and profile["ai_insights"]:

    for insight in profile["ai_insights"].split(","):
        st.success(insight.strip())

else:
    st.info("Generate AI insights after profile analysis.")
