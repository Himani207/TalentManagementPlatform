import streamlit as st
import re

from utils.auth import register_user


st.set_page_config(
    page_title="Student Registration",
    page_icon="📝"
)

st.title("📝 Student Registration")

full_name = st.text_input("Full Name")

email = st.text_input("Email")

password = st.text_input(
    "Password",
    type="password"
)

role = st.selectbox(
    "Register As",
    [
        "High School Student",
        "College Student",
        "Working Professional"
    ]
)


if st.button("Register"):

    # Empty field check
    if not full_name or not email or not password:
        st.warning("⚠️ Please fill all fields.")

    else:

        # Email validation
        email_pattern = (
            r"^[a-zA-Z0-9._%+-]+"
            r"@[a-zA-Z0-9.-]+"
            r"\.[a-zA-Z]{2,}$"
        )

        # Password validation
        password_pattern = (
            r"^(?=.*[a-z])"
            r"(?=.*[A-Z])"
            r"(?=.*\d)"
            r"(?=.*[@$!%*?&])"
            r".{8,}$"
        )

        # Check email
        if not re.match(email_pattern, email):

            st.error(
                "❌ Please enter a valid email address."
            )

        # Check password
        elif not re.match(password_pattern, password):

            st.error(
                "❌ Password must contain:\n\n"
                "• At least 8 characters\n"
                "• One uppercase letter (A-Z)\n"
                "• One lowercase letter (a-z)\n"
                "• One number (0-9)\n"
                "• One special character (@ $ ! % * ? &)"
            )

        # Register user
        else:

            if register_user(
                full_name.strip(),
                email.strip(),
                password,
                role
            ):

                st.success(
                    "✅ Registration Successful"
                )

            else:

                st.error(
                    "❌ Email already exists"
                )