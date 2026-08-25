import streamlit as st
from utils.professional_sidebar import professional_sidebar
from utils.professional_db import generate_industry_analysis
from utils.professional_theme import load_professional_theme
# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Industry Trends",
    page_icon="📈",
    layout="wide"
)
load_professional_theme()
# ==========================================================
# LOAD PROFILE
# ==========================================================

profile = professional_sidebar()

# ==========================================================
# TITLE
# ==========================================================

st.title("📈 AI Industry Trends")
st.caption("Personalized market insights based on your profile.")

st.divider()

# ==========================================================
# PROFILE SUMMARY
# ==========================================================

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Current Role", profile.get("current_role", "-"))

with c2:
    st.metric("Experience", f"{profile.get('experience',0)} Years")

with c3:
    st.metric("Career Goal", profile.get("preferred_role", "-"))

st.divider()
# ==========================================================
# GENERATE REPORT
# ==========================================================

if "industry_report" not in st.session_state:
    st.session_state.industry_report = ""

if st.button("🚀 Generate Industry Report", use_container_width=True):

    with st.spinner("Analyzing latest industry trends..."):

        st.session_state.industry_report = generate_industry_analysis(profile)

if st.session_state.industry_report:

    st.success("Analysis Complete")

    st.markdown(st.session_state.industry_report)