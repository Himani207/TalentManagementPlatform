import streamlit as st

from utils.professional_sidebar import professional_sidebar
from utils.job_application_db import (
    get_applied_jobs,
    get_saved_jobs
)

st.set_page_config(
    page_title="My Applications",
    page_icon="📋",
    layout="wide"
)

profile = professional_sidebar()

st.title("📋 My Applications")

st.divider()

applied = get_applied_jobs(profile["email"])
saved = get_saved_jobs(profile["email"])

st.subheader("🚀 Applied Jobs")

if applied:

    for job in applied:

        with st.container(border=True):

            st.write(f"### {job['role']}")
            st.write(f"🏢 {job['company']}")
            st.write(f"📍 {job['location']}")
            st.success(job["status"])

else:

    st.info("You haven't applied for any jobs yet.")

st.divider()

st.subheader("⭐ Saved Jobs")

if saved:

    for job in saved:

        with st.container(border=True):

            st.write(f"### {job['role']}")
            st.write(f"🏢 {job['company']}")
            st.write(f"📍 {job['location']}")

else:

    st.info("No saved jobs.")
    