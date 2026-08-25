import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from PIL import Image

from utils.session import logout
from utils.school_db import get_all_students
from utils.college_db import get_all_college_students
from utils.professional_db import get_all_professionals


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="🛡️",
    layout="wide"
)


# ==========================================================
# AUTH CHECK
# ==========================================================

if not st.session_state.get("admin_logged_in"):

    st.switch_page("pages/admin_login.py")


# ==========================================================
# LOAD CSS
# ==========================================================

css_file = Path(__file__).parent.parent / "assets" / "style.css"

if css_file.exists():

    with open(css_file) as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
#==========================================================
# ADMIN SIDEBAR NAVIGATION
# ==========================================================
# ==========================================================
# ADMIN SIDEBAR (ONLY PROFILE + LOGOUT)
# ==========================================================

st.sidebar.title("🛡️ Admin Panel")

st.sidebar.success(
    st.session_state.get("name", "Admin")
)

st.sidebar.info(
    st.session_state.get("email", "")
)

st.sidebar.markdown("---")


if st.sidebar.button("🚪 Logout"):

    logout()

    st.switch_page("app.py")
# ==========================================================
# LOAD USER DATA
# ==========================================================

try:

    school_students = get_all_students()

except:

    school_students = []


try:

    college_students = get_all_college_students()

except:

    college_students = []


try:

    professionals = get_all_professionals()

except:

    professionals = []



total_school_students = len(school_students)

total_college_students = len(college_students)

total_professionals = len(professionals)



total_users = (
    total_school_students
    +
    total_college_students
    +
    total_professionals
)



# ==========================================================
# HEADER
# ==========================================================

st.title("🛡️ TalentSphere Elevate")

st.subheader(
    "Administrator Dashboard"
)


st.info(
"""
Manage students, monitor platform activity,
analyze career trends and track AI-powered
career development insights.
"""
)


st.markdown("---")



# ==========================================================
# USER OVERVIEW METRICS
# ==========================================================


c1,c2,c3,c4 = st.columns(4)


with c1:

    st.metric(
        "🎒 High School Students",
        total_school_students
    )


with c2:

    st.metric(
        "🎓 College Students",
        total_college_students
    )


with c3:

    st.metric(
        "💼 Working Professionals",
        total_professionals
    )


with c4:

    st.metric(
        "👥 Total Users",
        total_users
    )



st.markdown("---")
# ==========================================================
# ADMIN MODULE NAVIGATION CARDS
# ==========================================================

st.header("🚀 Manage Platform")


card1, card2, card3 = st.columns(3)


with card1:

    st.markdown(
    """
    <div class="white-card">

    <h2>🎒 High School</h2>

    <p>
    Manage school students,
    profiles and activities.
    </p>

    </div>
    """,
    unsafe_allow_html=True
    )


    if st.button(
        "Open School Management",
        use_container_width=True
    ):
        st.switch_page(
            "pages/admin_school.py"
        )



with card2:

    st.markdown(
    """
    <div class="white-card">

    <h2>🎓 College</h2>

    <p>
    Manage college students,
    skills and placement data.
    </p>

    </div>
    """,
    unsafe_allow_html=True
    )


    if st.button(
        "Open College Management",
        use_container_width=True
    ):
        st.switch_page(
            "pages/admin_college.py"
        )



with card3:

    st.markdown(
    """
    <div class="white-card">

    <h2>💼 Professionals</h2>

    <p>
    Manage working professionals,
    career growth and jobs.
    </p>

    </div>
    """,
    unsafe_allow_html=True
    )


    if st.button(
        "Open Professional Management",
        use_container_width=True
    ):
        st.switch_page(
            "pages/admin_professional.py"
        )

# ==========================================================
# SEARCH USERS
# ==========================================================


st.header(
    "🔍 Search Students"
)


keyword = st.text_input(
    "Search by Email"
)


all_users = (
    school_students
    +
    college_students
    +
    professionals
)



if all_users:


    user_df = pd.DataFrame(
        all_users
    )


    if keyword:


        search_df = user_df[
            user_df.astype(str)
            .apply(
                lambda row:
                row.str.contains(
                    keyword,
                    case=False
                ).any(),
                axis=1
            )
        ]


    else:

        search_df = user_df



    st.dataframe(
        search_df,
        use_container_width=True,
        hide_index=True
    )



st.markdown("---")



# ==========================================================
# REGISTRATION ANALYTICS
# ==========================================================


st.header(
    "📈 Registration Analytics"
)



registration = pd.DataFrame(
{
"Category":
[
"High School",
"College",
"Professional"
],

"Users":
[
total_school_students,
total_college_students,
total_professionals
]

}
)



fig = px.bar(
    registration,
    x="Category",
    y="Users",
    title="Platform User Distribution"
)



fig.update_layout(
    template="plotly_white",
    title_x=0.5
)



st.plotly_chart(
    fig,
    use_container_width=True
)



st.markdown("---")
# ==========================================================
# SYSTEM SUMMARY (DYNAMIC)
# ==========================================================


st.header(
    "📋 System Summary"
)


summary = pd.DataFrame(
{
"Module":
[
"🎒 High School Students",
"🎓 College Students",
"💼 Working Professionals",
"🤖 AI Services"
],

"Status":
[
f"{total_school_students} Registered",
f"{total_college_students} Registered",
f"{total_professionals} Registered",
"Online"
]

}
)

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)
# ==========================================================
# FOOTER
# ==========================================================


st.markdown(
"""
<div class="footer">

🎓 TalentSphere Elevate

<br>

AI Powered Career Development Platform

</div>
""",
unsafe_allow_html=True
)