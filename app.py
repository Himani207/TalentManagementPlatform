import streamlit as st
from database import initialize_database
st.set_page_config(
    page_title="TalentSphere Elevate",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

initialize_database()

st.switch_page("pages/login.py")