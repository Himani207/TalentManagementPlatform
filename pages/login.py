import streamlit as st
from utils.auth import login_user
from utils.session import create_session

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Talent Management Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================================
# LOAD CSS
# ==========================================================

def load_css():
    try:
        with open("assets/style.css", "r", encoding="utf-8") as css:
            st.markdown(
                f"<style>{css.read()}</style>",
                unsafe_allow_html=True
            )
    except FileNotFoundError:
        pass


load_css()
# ==========================================================
# DEFAULT ROLE FROM LANDING PAGE
# ==========================================================

selected_role = st.session_state.get("selected_role", "")
roles = [
    "High School Student",
    "College Student",
    "Working Professional",
   
]

# Convert landing page names to login page names
role_mapping = {
    "High School": "High School Student",
    "College": "College Student",
    "Professional": "Working Professional",
}

default_role = role_mapping.get(selected_role, roles[0])
# ==========================================================
# HIDE STREAMLIT DEFAULT ELEMENTS
# ==========================================================
st.markdown("""
<style>

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

[data-testid="stSidebarNav"]{
display:none;
}

.block-container{
padding-top:2rem;
padding-bottom:2rem;
max-width:1300px;
}
</style>
""", unsafe_allow_html=True)
# ==========================================================
# TOP HEADER
# ==========================================================

header_left, header_right = st.columns([1.5, 2])

with header_left:
    st.markdown("## 🎓 Talent Management Platform")

with header_right:
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.caption("Career Recommendation")

    with c2:
        st.caption("Resume Analyzer")

    with c3:
        st.caption("Learning Roadmap")

    with c4:
        st.caption("AI Coach")

st.divider()

# ==========================================================
# MAIN LAYOUT
# ==========================================================

left, right = st.columns(
    [1.45,1],
    gap="large"
)

# ==========================================================
# LEFT SIDE
# ==========================================================

with left:

    st.markdown("""
                
<div class="hero-title">

Empowering Every Career Journey with AI

</div>
""", unsafe_allow_html=True)

    st.markdown("""

### AI Powered Career Development Platform

Talent Management Platform is an AI-powered platform designed for

- 🎓 High School Students
- 🏫 College Students
- 💼 Working Professionals

Our platform provides intelligent career recommendations,
ATS resume analysis, skill gap detection, interview
preparation, coding practice and personalized
learning roadmaps.

""")

    st.write("")

    a,b,c,d = st.columns(4)

    with a:
        st.metric(
            "Students",
            "12K+"
        )

    with b:
        st.metric(
            "Companies",
            "500+"
        )

    with c:
        st.metric(
            "Resume Score",
            "96%"
        )

    with d:
        st.metric(
            "Placements",
            "3200+"
        )

    st.write("")

    st.subheader("✨ Platform Features")

    f1, f2 = st.columns(2)

    with f1:

        st.success("🎯 AI Career Recommendation")

        st.success("📄 ATS Resume Analyzer")

        st.success("💻 Coding Practice")

        st.success("🎤 Interview Preparation")

        st.success("📊 Progress Dashboard")

    with f2:

        st.info("🧠 Skill Gap Analysis")

        st.info("🗺 Learning Roadmap")

        st.info("🤖 AI Career Coach")

        st.info("📚 Course Suggestions")

        st.info("🏆 Placement Preparation")

# ==========================================================
# RIGHT SIDE
# ==========================================================

with right:

    st.markdown("""
<div class="login-heading">

<h2>Welcome Back 👋</h2>

<p>
Sign in to continue your career journey.
</p>

</div>
""", unsafe_allow_html=True)

    with st.container(border=True):

        st.subheader("🔐 Login")

        email = st.text_input(
            "Email Address",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )
        role = st.selectbox(
            "Login As",
            roles,
            index=roles.index(default_role)
        )


        remember = st.checkbox(
            "Remember Me"
        )

        st.write("")

        login = st.button(
            "🚀 Login",
            use_container_width=True
        )

        st.write("")

        c1,c2 = st.columns(2)

        with c1:

            register = st.button(
                "📝 Register",
                use_container_width=True
            )

        with c2:

            forgot = st.button(
                "🔑 Forgot Password",
                use_container_width=True
            )

        if register:
            st.switch_page("pages/register.py")
        # --------------------------------------------------
        # Forgot Password
        # --------------------------------------------------

        if forgot:
            st.info("Forgot Password feature will be available soon.")

        # --------------------------------------------------
        # LOGIN
        # --------------------------------------------------

        if login:

            if email.strip() == "" or password.strip() == "":

                st.warning("Please enter your email and password.")

            else:

                user = login_user(email.strip(), password)

                if user:
                    db_role = user["role"].strip()
                    if db_role != role:
                        st.error(
                            f"This account is registered as {db_role}"
                        )
                    else:
                      create_session(
                          user["name"],
                          user["email"],
                          db_role
                        )
                      st.success(
                           f"Welcome {user['name']} 👋"
                        )

                    st.success(f"Welcome {user['name']} 👋")

                    role = user["role"].strip()

                    if role == "High School Student":
                        st.switch_page("pages/school.py")

                    elif role == "College Student":
                        st.switch_page("pages/college.py")

                    elif role == "Working Professional":
                        st.switch_page("pages/professional.py")
                    else:
                        st.error(f"Unknown role: {role}")

                else:

                    st.error("❌ Invalid Email or Password")
# ==========================================================
# FEATURE SECTION
# ==========================================================

st.write("")
st.write("")
st.markdown("---")

st.markdown(
    "<h2 style='text-align:center;margin-bottom:30px;'>Why Choose Talent Management Platform?</h2>",
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>🎯 Career Recommendation</h3>
        <p>
        Discover career paths that match your skills, interests, and aspirations
        through AI-powered recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <h3>🧠 Skill Gap Analysis</h3>
        <p>
        Identify missing technical and soft skills required to achieve your
        dream career and receive personalized learning suggestions.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
                
                <div class="feature-card">

               <h3>📄 Resume Analyzer</h3>
               <p>Improve your ATS score with AI-powered resume analysis and actionable recommendations.</p>
                </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <h3>🤖 AI Career Coach</h3>
        <p>
        Get instant career guidance, interview preparation tips, and learning
        recommendations anytime.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================================
# PLATFORM MODULES
# ==========================================================

st.write("")
st.write("")

st.markdown(
    "<h2 style='text-align:center;margin-bottom:30px;'>🚀 Platform Modules</h2>",
    unsafe_allow_html=True
)

col1, col2, col3, col4, col5 = st.columns(5)

modules = [
    ("🎓", "School"),
    ("🏫", "College"),
    ("💼", "Professional"),
]

columns = [col1, col2, col3, col4, col5]

for col, (icon, title) in zip(columns, modules):
    with col:
        st.markdown(f"""
                    
        <div class="module-card">
            <div class="module-icon">{icon}</div>
            <div class="module-title">{title}</div>
        </div>
        """, unsafe_allow_html=True)
# ==========================================================
# FOOTER
# ==========================================================

st.write("")
st.write("")
st.markdown("---")

st.markdown("""
<div style="text-align:center;padding:20px;">

<h3>🎓 Talent Management Platform </h3>

<p>
AI-Powered Career Development Platform
</p>

<p>
Empowering students and professionals through Artificial Intelligence.
</p>

<p style="color:gray;">
© 2026 Talent Management Platform | All Rights Reserved
</p>

</div>
""", unsafe_allow_html=True)


# Admin Login Link

st.markdown(
"""
<div style="text-align:center;">
""",
unsafe_allow_html=True
)

st.page_link(
    "pages/admin_login.py",
    label="🛡️ Admin Login"
)

st.markdown(
"""
</div>
""",
unsafe_allow_html=True
)