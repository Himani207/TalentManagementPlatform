import streamlit as st
from utils.professional_sidebar import professional_sidebar
from utils.professional_theme import load_professional_theme
from utils.professional_db import (
    get_profile,
    save_profile,
    update_profile
)
# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Edit Professional Profile",
    page_icon="✏",
    layout="wide"
)
load_professional_theme()

# ==========================================================
# LOAD SIDEBAR & PROFILE
# ==========================================================
# Login Check
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.switch_page("pages/login.py")
    st.stop()

email = st.session_state.email
profile = get_profile(email)

if profile is None:
    profile = {
        "email": email,
        "full_name": "",
        "phone": "",
        "location": "",
        "company": "",
        "current_role": "",
        "experience": 0,
        "technical_skills": "",
        "soft_skills": "",
        "career_goal": "",
        "preferred_role": "",
        "leadership": 50,
        "work_experience": "",
        "achievements": "",
        "certifications": "",
        "linkedin": "",
        "github": "",
        "resume_score": 0
    }

# Show Sidebar
professional_sidebar()
# ==========================================================
# PAGE TITLE
# ==========================================================

st.title("✏ Edit Professional Profile")
st.caption("Update your professional information")
st.divider()

# ==========================================================
# PROFESSIONAL INFORMATION
# ==========================================================

st.subheader("👤 Professional Information")

c1, c2 = st.columns(2)
with c1:

    full_name = st.text_input(
        "Full Name",
        value=profile.get("full_name", "")
    )

    phone = st.text_input(
        "Phone Number",
        value=profile.get("phone", "")
    )

    company = st.text_input(
        "Company",
        value=profile.get("company", "")
    )

    location = st.text_input(
        "Location",
        value=profile.get("location", "")
    )

with c2:

    current_role = st.text_input(
        "Current Role",
        value=profile.get("current_role", "")
    )

    experience = st.number_input(
        "Experience (Years)",
        min_value=0,
        max_value=40,
        value=int(profile.get("experience", 0))
    )
    current_salary = st.number_input(
        "Current Monthly Salary (₹)",
        min_value=0,
        step=1000,
        value=int(profile.get("current_salary", 50000)),
        help="Enter your current monthly salary in Indian Rupees."
    )

    leadership = st.slider(
        "Leadership Skill",
        0,
        100,
        int(profile.get("leadership", 50))
    )

    email = st.text_input(
        "Email",
        value=profile.get("email", ""),
        disabled=True
    )

# ==========================================================
# CAREER INFORMATION
# ==========================================================

st.divider()

st.subheader("🎯 Career Information")

career_goal = st.text_area(
    "Career Goal",
    value=profile.get("career_goal", ""),
    height=120
)

preferred_role = st.text_input(
    "Preferred Role",
    value=profile.get("preferred_role", "")
)

# ==========================================================
# TECHNICAL SKILLS
# ==========================================================

st.divider()

st.subheader("💻 Technical Skills")
technical_skills = st.text_area(
    "Technical Skills (Comma Separated)",
    value=profile.get("technical_skills", ""),
    height=120,
    placeholder="Python, SQL, Power BI, React, AWS"
)
# ==========================================================
# SOFT SKILLS
# ==========================================================
st.subheader("🤝 Soft Skills")
soft_skills = st.text_area(
    "Soft Skills (Comma Separated)",
    value=profile.get("soft_skills", ""),
    height=100,
    placeholder="Leadership, Communication, Teamwork"
)
# ==========================================================
# WORK EXPERIENCE
# ==========================================================
st.divider()
st.subheader("🏢 Work Experience")
work_experience = st.text_area(
    "Describe your work experience",
    value=profile.get("work_experience", ""),
    height=180,
    placeholder="""
Example:

Software Engineer - ABC Pvt Ltd (2023-Present)

• Developed REST APIs using Python
• Improved application performance by 30%
• Led a team of 4 developers
"""
)

# ==========================================================
# ACHIEVEMENTS
# ==========================================================

st.divider()

st.subheader("🏆 Achievements")

achievements = st.text_area(
    "Achievements (Comma Separated)",
    value=profile.get("achievements", ""),
    height=120,
    placeholder="""
Employee of the Month,
Hackathon Winner,
Patent Filed,
Best Performer
"""
)

# ==========================================================
# CERTIFICATIONS
# ==========================================================

st.divider()

st.subheader("📜 Certifications")

certifications = st.text_area(
    "Certifications (Comma Separated)",
    value=profile.get("certifications", ""),
    height=120,
    placeholder="""
AWS Certified Cloud Practitioner,
Microsoft Azure Fundamentals,
Google Data Analytics
"""
)

# ==========================================================
# PROFESSIONAL LINKS
# ==========================================================

st.divider()
st.subheader("🔗 Professional Links")
c1, c2 = st.columns(2)
with c1:

    linkedin = st.text_input(
        "LinkedIn Profile",
        value=profile.get("linkedin", ""),
        placeholder="https://www.linkedin.com/in/username"
    )

with c2:

    github = st.text_input(
        "GitHub Profile",
        value=profile.get("github", ""),
        placeholder="https://github.com/username"
    )


# ==========================================================
# PROFILE PREVIEW
# ==========================================================

st.divider()

st.subheader("👀 Profile Preview")

preview1, preview2 = st.columns(2)

with preview1:

    st.info(f"""
**Name:** {full_name}

**Current Role:** {current_role}

**Company:** {company}

**Experience:** {experience} Years
**Current Monthly Salary:** ₹{current_salary:,.0f}
**Preferred Role:** {preferred_role}
""")

with preview2:

    tech_count = len([
        s for s in technical_skills.split(",")
        if s.strip()
    ])

    cert_count = len([
        s for s in certifications.split(",")
        if s.strip()
    ])

    achievement_count = len([
        s for s in achievements.split(",")
        if s.strip()
    ])

    st.info(f"""
    **Technical Skills:** {tech_count}
    **Certifications:** {cert_count}
    **Achievements:** {achievement_count}
    **Leadership Score:** {leadership}%
    """)
# ==========================================================
# SAVE PROFILE
# ==========================================================

st.divider()

c1, c2 = st.columns(2)

with c1:

    save_btn = st.button(
        "💾 Save Profile",
        use_container_width=True,
        type="primary"
    )

with c2:

    clear_btn = st.button(
        "🔄 Reset Form",
        use_container_width=True
    )

if clear_btn:
    st.rerun()

# ==========================================================
# VALIDATION + SAVE
# ==========================================================

if save_btn:

    # ------------------------
    # Required Fields
    # ------------------------

    required_fields = [
        full_name,
        company,
        current_role,
        career_goal,
        preferred_role
    ]

    if not all(required_fields):

        st.error("Please fill all required fields.")

    else:

        profile_data = {

            "email": profile["email"],

            "full_name": full_name,
            "phone": phone,
            "location": location,

            "company": company,
            "current_role": current_role,
            "experience": experience,
            "current_salary": current_salary,

            "technical_skills": technical_skills,
            "soft_skills": soft_skills,

            "career_goal": career_goal,
            "preferred_role": preferred_role,

            "leadership": leadership,

            "work_experience": work_experience,
            "achievements": achievements,
            "certifications": certifications,

            "linkedin": linkedin,
            "github": github,
        }

        if get_profile(profile_data["email"]) is None:
            save_profile(profile_data)
        else:
            update_profile(profile_data["email"], profile_data)
        st.success("✅ Professional Profile Updated Successfully!")
        st.balloons()


# ==========================================================
# QUICK ACTIONS
# ==========================================================

st.divider()

st.subheader("🚀 Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:

    if st.button(
        "🏠 Dashboard",
        use_container_width=True
    ):
        st.switch_page(
            "pages/professional.py"
        )

with col2:

    if st.button(
        "👤 View Profile",
        use_container_width=True
    ):
        st.switch_page(
            "pages/professional_profile.py"
        )

with col3:

    if st.button(
        "📄 Resume Analyzer",
        use_container_width=True
    ):
        st.switch_page(
            "pages/resume_analyzer.py"
        )

# ==========================================================
# FOOTER
# ==========================================================
st.divider()

st.caption(
    "TalentSphere Elevate • Working Professional Module"
)