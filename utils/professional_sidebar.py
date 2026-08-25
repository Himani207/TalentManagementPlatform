import streamlit as st
from utils.session import logout
from utils.professional_db import get_profile


def professional_sidebar():

    # ==========================================================
    # LOGIN CHECK
    # ==========================================================

    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.warning("Please login first.")
        st.switch_page("pages/login.py")
        st.stop()

    email = st.session_state.email

    # ==========================================================
    # LOAD PROFILE
    # ==========================================================

    profile = get_profile(email)

    # If profile doesn't exist yet,
    # create an empty profile dictionary.
    if profile is None:

        profile = {
            "email": email,
            "full_name": "Professional",
            "company": "",
            "current_role": "",
            "location": ""
        }

    # ==========================================================
    # SIDEBAR
    # ==========================================================

    with st.sidebar:

        st.title("💼 TalentSphere Elevate")
        st.caption("Working Professional Portal")

        st.divider()

        st.write(f"**{profile.get('full_name', 'Professional')}**")
        st.caption(profile.get("current_role", ""))
        st.caption(profile.get("company", ""))

        st.divider()

        st.page_link(
            "pages/professional.py",
            label="🏠 Dashboard"
        )

        st.page_link(
            "pages/professional_profile.py",
            label="👤 My Profile"
        )

        st.page_link(
            "pages/edit_professional_profile.py",
            label="✏ Edit Profile"
        )

        st.page_link(
            "pages/resume_analyzer.py",
            label="📄 Resume Analyzer"
        )

        st.page_link(
            "pages/career_analytics.py",
            label="📊 Career Analytics"
        )
        st.page_link(
            "pages/salary_insights.py",
            label="Salary Insights",
            icon="💰"
        )
        st.page_link(
            "pages/interview_preparation.py",
            label="🎯 Interview Preparation"
        )

        st.page_link(
            "pages/professional_job_matching.py",
            label="💼 AI Career Opportunity Matcher"
        )
        st.page_link(
            "pages/my_applications.py",
            label="📋 My Applications"
        )
        st.page_link(
            "pages/ai_career_coach.py",
            label="🤖 AI Career Coach"
        )
        st.page_link(
            "pages/promotion_readiness.py",
            label="🚀 Promotion Readiness"
        )
        st.page_link(
            "pages/industry_trends.py",
            label="📈 Industry Trends"
        )

        st.page_link(
            "pages/certifications.py",
            label="🏆 Certifications"
        )

        st.divider()

        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.switch_page("app.py")

    return profile