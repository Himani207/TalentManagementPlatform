import streamlit as st
from pathlib import Path
def load_professional_theme():

    css = Path(
        "assets/professional_style.css"
    ).read_text()

    st.markdown(
        f"""
        <style>
        {css}
        </style>
        """,
        unsafe_allow_html=True
    )