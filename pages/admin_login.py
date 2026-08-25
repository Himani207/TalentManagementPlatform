import streamlit as st

from utils.admin_db import check_admin_login


st.set_page_config(
    page_title="Admin Login",
    page_icon="⚙️",
    layout="centered"
)


st.title("⚙️ Admin Login")


email = st.text_input("Email")

password = st.text_input(
    "Password",
    type="password"
)


if st.button("Login"):

    admin = check_admin_login(
        email,
        password
    )

    if admin:

        st.session_state.admin_logged_in = True
        st.session_state.name = admin["name"]
        st.session_state.email = admin["email"]

        st.success("Login Successful")

        st.switch_page(
            "pages/admin_dashboard.py"
        )

    else:

        st.error("Invalid Admin Credentials")