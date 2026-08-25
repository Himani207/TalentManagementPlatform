import streamlit as st
from pathlib import Path
from utils.auth import register_user

st.set_page_config(
    page_title="Parent & Teacher Registration",
    page_icon="🎓",
    layout="centered"
)

# -------------------------
# LOAD CSS
# -------------------------
css_file = Path(__file__).parent.parent / "assets" / "style.css"

if css_file.exists():
    with open(css_file) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# -------------------------
# HEADER
# -------------------------
st.markdown("""
<div class="glass-card">

<h1 style="text-align:center;">
🎓 TalentSphere Elevate
</h1>

<h3 style="text-align:center;">
Parent & Teacher Registration
</h3>

<p style="text-align:center;">
Join the AI Powered Career Development Platform
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# -------------------------
# REGISTRATION FORM
# -------------------------
with st.container():

    st.subheader("Create Your Account")

    full_name = st.text_input("👤 Full Name")

    email = st.text_input("📧 Email Address")

    password = st.text_input(
        "🔑 Create Password",
        type="password"
    )

    role = st.selectbox(
        "Select Account Type",
        [
            "Parent",
            "Teacher"
        ]
    )

    st.write("")

    if st.button(
        "🚀 Create Account",
        use_container_width=True
    ):

        if (
            full_name.strip() == ""
            or email.strip() == ""
            or password.strip() == ""
        ):

            st.warning("Please complete all fields.")

        else:

            success = register_user(
                full_name,
                email,
                password,
                role
            )

            if success:

                st.success(
                    "✅ Registration successful! Please login."
                )

            else:

                st.error(
                    "❌ Email already registered."
                )

# -------------------------
# FOOTER
# -------------------------
st.markdown("""
<hr>

<div style="text-align:center">

<h4>🚀 TalentSphere Elevate</h4>

<p>AI Powered Career Development Platform</p>

<p>Made with ❤️ using Streamlit</p>

</div>
""", unsafe_allow_html=True)