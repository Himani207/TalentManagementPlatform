import streamlit as st
from utils.session import logout
from utils.college_db import get_profile
from utils.placement_db import get_placement
from utils.resume_db import get_resume_score
from utils.coding_db import get_coding_score

# ==========================================================
# LOGIN CHECK
# ==========================================================

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.switch_page("pages/login.py")
email = st.session_state.email
profile = get_profile(st.session_state.email)
placement = get_placement(email)

if placement:
    placement_score = placement["placement_score"]
else:
    placement_score = 0

# Dynamic Resume and Coding Scores
resume_score = get_resume_score(email)

coding_score = get_coding_score(email)
# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="College Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(
    """
    <style>

    /* Sidebar scroll */
    section[data-testid="stSidebar"] > div {
        height: 100vh;
        overflow-y: auto;
        padding-bottom: 2rem;
    }


    /* Sidebar width */
    section[data-testid="stSidebar"] {
        width: 300px;
    }


    /* Sidebar scrollbar */
    section[data-testid="stSidebar"] > div::-webkit-scrollbar {
        width: 8px;
    }


    section[data-testid="stSidebar"] > div::-webkit-scrollbar-thumb {
        border-radius: 10px;
    }


    /* Navigation spacing */
    div[data-testid="stSidebarNav"] {
        padding-top: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# LOAD CSS
# ==========================================================

def load_css():
    try:
        with open("assets/style.css", "r", encoding="utf-8") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    except:
        pass

load_css()

# ==========================================================
# HIDE STREAMLIT
# ==========================================================

st.markdown("""
<style>

#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}

[data-testid="stSidebarNav"]{
display:none;
}

.block-container{
padding-top:1rem;
padding-bottom:2rem;
max-width:1300px;
}

</style>
""", unsafe_allow_html=True)
# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown("# 🎓 Talent Management Platform")
    st.caption("College Portal")

    st.divider()

    st.page_link("pages/college.py", label="🏠 Dashboard")
    st.page_link("pages/profile.py", label="👤 My Profile")
    st.page_link("pages/resume_builder.py", label="📄 Resume Builder")
    st.page_link("pages/resume_analyzer.py", label="🤖 ATS Resume Analyzer")
    st.page_link("pages/coding.py", label="💻 Coding Practice")
    st.page_link("pages/mock_interview.py", label="🎤 AI Mock Interview")
    st.page_link("pages/internship.py",label="💼 Internship Experience")
    st.page_link("pages/placement_readiness.py",label="🎯 Placement Readiness")
    st.page_link("pages/skill_gap_analysis.py", label="🎯 Skill Gap Analysis")
    st.page_link("pages/learning_roadmap.py", label="🗺 Learning Roadmap")
    st.page_link("pages/career_recommendation.py", label="💼 Career Recommendation")
    st.page_link("pages/job_matching.py",label="💼 Job Matching")
    st.page_link("pages/chatbot.py", label="🤖 AI Chatbot")

    st.divider()

    if st.button("🚪 Logout", use_container_width=True):
        logout()
        st.switch_page("app.py")


# ==========================================================
# TOP HEADER
# ==========================================================

left,right = st.columns([6,1])

with left:

    st.markdown("""
    <div class="dashboard-title">
        🎓 <span>Talent Management Platform</span>
    </div>
    """, unsafe_allow_html=True)

with right:

    if st.button("🚪 Logout"):
        logout()
        st.switch_page("app.py")

st.write("")

# ==========================================================
# SEARCH BAR
# ==========================================================

search_col, profile_col = st.columns([5,1])
with search_col:

    search = st.text_input(
        "",
        placeholder="🔍 Search Dashboard...",
        key="dashboard_search"
    )
with profile_col:

    st.markdown(f"""
    <div class="profile-box">

    👤<br>
    <b>{profile["full_name"] if profile else st.session_state.name}</b>

    </div>
    """, unsafe_allow_html=True)

st.write("")
dashboard_features = [
    {
        "name":"Resume Builder",
        "page":"pages/resume_builder.py",
        "icon":"📄"
    },
    {
        "name":"ATS Resume Analyzer",
        "page":"pages/resume_analyzer.py",
        "icon":"🤖"
    },
    {
        "name":"Coding Practice",
        "page":"pages/coding.py",
        "icon":"💻"
    },
    {
        "name":"AI Mock Interview",
        "page":"pages/mock_interview.py",
        "icon":"🎤"
    },
    {
        "name":"Skill Gap Analysis",
        "page":"pages/skill_gap_analysis.py",
        "icon":"🎯"
    },
    {
        "name":"Learning Roadmap",
        "page":"pages/learning_roadmap.py",
        "icon":"🗺"
    },
    {
        "name":"Career Recommendation",
        "page":"pages/career_recommendation.py",
        "icon":"💼"
    },
    {
        "name":"AI Chatbot",
        "page":"pages/chatbot.py",
        "icon":"🤖"
    }
]
if search:

    st.subheader("🔍 Search Results")


    results = [
        item for item in dashboard_features
        if search.lower() in item["name"].lower()
    ]


    if results:

        for item in results:

            if st.button(
                f"{item['icon']} {item['name']}",
                use_container_width=True
            ):
                st.switch_page(item["page"])


    else:

        st.warning(
            "No feature found"
        )

# ==========================================================
# WELCOME
# ==========================================================
st.markdown(
f"""
<div class="hero-card">

<h1>
Welcome Back, {profile["full_name"] if profile else st.session_state.name} 👋
</h1>

<p>
Your AI-powered career growth dashboard
</p>

<div class="hero-badges">

<span>🎯 Placement Preparation</span>
<span>💻 Coding Growth</span>
<span>🤖 AI Career Support</span>

</div>

</div>
""",
unsafe_allow_html=True
)
if profile:

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info(
            f"🎓 {profile['degree']}"
        )

    with c2:
        st.info(
            f"🏫 {profile['college']}"
        )

    with c3:
        st.info(
            f"💻 {profile['department']}"
        )
# ==========================================================
# CAREER METRICS
# ==========================================================

st.subheader("📊 Career Overview")


m1,m2,m3,m4 = st.columns(4)


with m1:

    st.markdown(f"""
    <div class="metric-card">

    <h3>📄</h3>
    <h2>{resume_score}%</h2>
    <p>Resume Score</p>

    </div>
    """,unsafe_allow_html=True)
with m2:
    st.markdown("""
    <div class="metric-card">

    <h3>💻</h3>
    <h2>165</h2>
    <p>Coding Problems</p>

    </div>
    """,unsafe_allow_html=True)
with m3:

    st.markdown(f"""
    <div class="metric-card">

    <h3>🎯</h3>
    <h2>{placement_score}%</h2>
    <p>Placement Ready</p>

    </div>
    """,unsafe_allow_html=True)

with m4:
    st.markdown("""
    <div class="metric-card">

    <h3>🧠</h3>
    <h2>78%</h2>
    <p>Skill Match</p>

    </div>
    """,unsafe_allow_html=True)
st.write("")

# ==========================================================
# QUICK ACCESS
# ==========================================================
# ==========================================================
# CAREER ACTIONS
# ==========================================================

st.subheader("🚀 Career Actions")


c1, c2, c3 = st.columns(3, gap="large")


with c1:

    st.markdown("""
    <div class="action-card">

    <h1>📄</h1>

    <h3>
    Resume Builder
    </h3>

    <p>
    Create ATS-friendly resume
    </p>

    </div>
    """, unsafe_allow_html=True)


    if st.button(
        "Open Resume Builder",
        key="resume_builder",
        use_container_width=True
    ):
        st.switch_page(
            "pages/resume_builder.py"
        )



    st.markdown("""
    <div class="action-card">

    <h1>🤖</h1>

    <h3>
    ATS Resume Analyzer
    </h3>

    <p>
    Improve resume score
    </p>

    </div>
    """, unsafe_allow_html=True)


    if st.button(
        "Analyze Resume",
        key="resume_analyzer",
        use_container_width=True
    ):
        st.switch_page(
            "pages/resume_analyzer.py"
        )



with c2:

    st.markdown("""
    <div class="action-card">

    <h1>💻</h1>

    <h3>
    Coding Practice
    </h3>

    <p>
    Master DSA problems
    </p>

    </div>
    """, unsafe_allow_html=True)


    if st.button(
        "Start Coding",
        key="coding",
        use_container_width=True
    ):
        st.switch_page(
            "pages/coding.py"
        )



    st.markdown("""
    <div class="action-card">

    <h1>🎤</h1>

    <h3>
    AI Mock Interview
    </h3>

    <p>
    Practice real interviews
    </p>

    </div>
    """, unsafe_allow_html=True)
    if st.button(
        "Start Interview",
        key="mock_interview",
        use_container_width=True
    ):
        st.switch_page(
            "pages/mock_interview.py"
        )
with c3:
    st.markdown("""
    <div class="action-card">

    <h1>🎯</h1>

    <h3>
    Skill Gap Analysis
    </h3>

    <p>
    Find missing skills
    </p>

    </div>
    """, unsafe_allow_html=True)


    if st.button(
        "Analyze Skills",
        key="skill_gap",
        use_container_width=True
    ):
        st.switch_page(
            "pages/skill_gap_analysis.py"
        )
    st.markdown("""
    <div class="action-card">

    <h1>🗺</h1>

    <h3>
    Learning Roadmap
    </h3>

    <p>
    Personalized career path
    </p>

    </div>
    """, unsafe_allow_html=True)
    if st.button(
        "View Roadmap",
        key="roadmap",
        use_container_width=True
    ):
        st.switch_page(
            "pages/learning_roadmap.py"
        )
# ==========================================================
# PROGRESS OVERVIEW
# ==========================================================
st.write("")
st.subheader("📈 Progress Overview")
p1, p2, p3 = st.columns(3, gap="medium")
with p2:

    st.markdown(f"""
    <div class="small-progress-card">

    <span>📄 Resume</span>

    <h3>{resume_score}%</h3>
    <p>ATS Score</p>
    </div>
    """, unsafe_allow_html=True)
    st.progress(min(resume_score,100)/100)
    
with p1:
    coding_score = min(coding_score, 100)
    st.markdown(f"""
    <div class="small-progress-card">
    <span>💻 Coding</span>
    <h3>{coding_score}%</h3>
    <p>Coding Performance</p>

    </div>
    """, unsafe_allow_html=True)

    st.progress(coding_score / 100)
with p3:

    st.markdown(f"""
    <div class="small-progress-card">

    <span>🎯 Placement</span>

    <h3>{placement_score}%</h3>

    <p>Readiness</p>

    </div>
    """, unsafe_allow_html=True)

    st.progress(min(placement_score,100)/100)
#=========================================================
# AI TOOLS
# ==========================================================
st.write("")
st.write("")
st.subheader("🤖 AI Tools")
a1, a2, a3 = st.columns(3)
with a1:
    if st.button("AI Career Chatbot", use_container_width=True):
        st.switch_page("pages/chatbot.py")

with a2:
    if st.button("Resume Analyzer", use_container_width=True):
        st.switch_page("pages/resume_analyzer.py")

with a3:
    if st.button("Career Recommendation", use_container_width=True):
        st.switch_page("pages/career_recommendation.py")
