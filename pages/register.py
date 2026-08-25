import streamlit as st
from utils.auth import register_user

st.set_page_config(
    page_title="Student Registration",
    page_icon="📝"
)

st.title("📝 Student Registration")

full_name = st.text_input("Full Name")

email = st.text_input("Email")

password = st.text_input("Password", type="password")

role = st.selectbox(
    "Register As",
    [
        "High School Student",
        "College Student",
        "Working Professional"
    ]
)

if st.button("Register"):

    if not full_name or not email or not password:
        st.warning("Please fill all fields.")
    else:

        if register_user(
            full_name,
            email,
            password,
            role
        ):
            st.success("✅ Registration Successful")

        else:
            st.error("❌ Email already exists")