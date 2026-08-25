import streamlit as st

from utils.session import logout

from utils.school_db import (
    create_student_table,
    create_report_table,
    create_learning_progress_table,
    create_certificate_table,
    create_notification_table,
    get_student_profile,
    get_learning_progress,
    get_certificates,
    get_notifications,
    calculate_profile_completion,
    calculate_ai_readiness,
    get_career_match,
    get_student_report,
)

# ==========================================================
# LOGIN CHECK
# ==========================================================

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.switch_page("pages/login.py")
    st.stop()
email = st.session_state.email

create_student_table()
create_report_table()
create_learning_progress_table()
create_certificate_table()
create_notification_table()


# ==========================================================
# GET STUDENT DATA
# ==========================================================

student_profile = get_student_profile(email)

if student_profile is None:

    student_profile = {
        "email": email,
        "parent_email": "",
        "age": 15,
        "class": "10",
        "school": "",
        "interests": "",
        "subject": "",
        "career": "",
        "goal": ""
    }

# ==========================================================
# DYNAMIC DASHBOARD DATA
# ==========================================================

profile_completion = calculate_profile_completion(email)

ai_readiness = calculate_ai_readiness(email)

career_result = get_career_match(email)

learning = get_learning_progress(email)

certificates = get_certificates(email)

notifications = get_notifications(email)

report = get_student_report(email)
# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="High School Dashboard",
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

    st.title("🏫 TalentSphere Elevate")
    st.caption("High School Student Portal")

    st.divider()

    st.page_link(
        "pages/school.py",
        label="🏠 Dashboard"
    )

    st.page_link(
        "pages/school_profile.py",
        label="👤 Student Profile"
    )

    st.page_link(
        "pages/school_career.py",
        label="🎯 Career Assessment"
    )

    st.page_link(
        "pages/school_roadmap.py",
        label="📚 Learning Roadmap"
    )

    st.page_link(
        "pages/school_assessment.py",
        label="📝 Skill Assessment"
    )
    st.page_link(
        "pages/school_certificates.py",
        label="🏅 Certificates"
    )

    st.page_link(
        "pages/school_notifications.py",
        label="🔔 Notifications"
    )

    st.page_link(
        "pages/school_reports.py",
        label="📊 Reports"
    )

    st.page_link(
        "pages/school_ai_tools.py",
        label="🤖 AI Tools"
    )

    st.page_link(
        "pages/chatbot.py",
        label="💬 AI Chatbot"
    )

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):
        logout()
        st.switch_page("app.py")
# ==========================================================
# TOP HEADER
# ==========================================================
left, right = st.columns([6, 1])

with left:

    st.markdown(
        """
        <div class="dashboard-title">
            🎓 <span>TalentSphere Elevate</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with right:

    if st.button("🚪 Logout"):
        logout()
        st.switch_page("app.py")

st.write("")
# ==========================================================
# DYNAMIC SEARCH
# ==========================================================


# All High School Dashboard features
dashboard_features = [
    {
        "name": "Student Profile",
        "description": "View and update your personal student information",
        "keywords": ["profile", "student", "personal", "information"],
        "page": "pages/school_profile.py",
        "icon": "👤"
    },
    {
        "name": "Career Assessment",
        "description": "Discover careers based on your interests and subjects",
        "keywords": ["career", "assessment", "interest", "future", "job"],
        "page": "pages/school_career.py",
        "icon": "🎯"
    },
    {
        "name": "Learning Roadmap",
        "description": "Follow your personalized learning journey",
        "keywords": ["learning", "roadmap", "study", "course", "learn"],
        "page": "pages/school_roadmap.py",
        "icon": "📚"
    },
    {
        "name": "Skill Assessment",
        "description": "Test your knowledge and evaluate your skills",
        "keywords": ["skill", "assessment", "test", "quiz", "knowledge"],
        "page": "pages/school_assessment.py",
        "icon": "📝"
    },
    {
        "name": "Notifications",
        "description": "View important updates and opportunities",
        "keywords": ["notification", "updates", "alerts", "opportunities"],
        "page": "pages/school_notifications.py",
        "icon": "🔔"
    },
    {
        "name": "Reports",
        "description": "View your complete academic and career report",
        "keywords": ["report", "progress", "performance", "score", "results"],
        "page": "pages/school_reports.py",
        "icon": "📊"
    },
    {
        "name": "AI Tools",
        "description": "Use AI-powered tools for career guidance",
        "keywords": ["ai", "artificial intelligence", "tools", "guidance"],
        "page": "pages/school_ai_tools.py",
        "icon": "🤖"
    },
    {
        "name": "AI Chatbot",
        "description": "Ask questions and get AI career guidance",
        "keywords": ["chatbot", "chat", "ai", "question", "help"],
        "page": "pages/chatbot.py",
        "icon": "💬"
    }
]

search = st.text_input(
    "",
    placeholder="🔍 Search features, career, roadmap, assessment...",
    key="school_dashboard_search"
)

# ==========================================================
# SEARCH RESULTS
# ==========================================================
# ==========================================================
# SEARCH RESULTS
# ==========================================================

if search:

    query = search.lower().strip()

    results = []

    for item in dashboard_features:

        searchable_text = (
            item["name"].lower()
            + " "
            + item["description"].lower()
            + " "
            + " ".join(item["keywords"]).lower()
        )

        if query in searchable_text:
            results.append(item)

    # ======================================================
    # RESULTS FOUND
    # ======================================================

    if results:
        


        st.markdown("### 🔎 Search Results")
        for index, item in enumerate(results):

            if st.button(
                f'{item["icon"]}  {item["name"]}\n\n{item["description"]}',
                key=f"search_result_{index}",
                use_container_width=True
            ):
                st.switch_page(item["page"])
    # ======================================================
    # NO RESULTS
    # ======================================================

    else:

        st.warning(
            f"❌ No feature found for **'{search}'**"
        )

        st.caption(
            "Try searching for: career, roadmap, assessment, "
            "profile, report, AI, chatbot, or notifications."
        )
# ==========================================================
# WELCOME
# ==========================================================

student_name = st.session_state.get(
    "name",
    student_profile.get("email", "Student").split("@")[0].title()
)

st.markdown(
    f"""
    <div class="welcome-card">
        <h2>Welcome, {student_name} 👋</h2>
        <p> Explore your career, improve your skills,and build your future with AI.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)    
# ==========================================================
# HIGH SCHOOL METRICS
# ==========================================================

st.subheader("📊 Student Overview")

m1, m2, m3, m4 = st.columns(4)

with m1:

    st.markdown(
        f"""
        <div class="metric-card">

        <h3>🎯</h3>

        <h2>{career_result['match']}%</h2>

        <p>Career Match</p>

        </div>
        """,
        unsafe_allow_html=True
    )

with m2:

    learning_percentage = learning.get(
        "progress_percentage",
        0
    )

    st.markdown(
        f"""
        <div class="metric-card">

        <h3>📚</h3>

        <h2>{learning_percentage}%</h2>

        <p>Learning Progress</p>

        </div>
        """,
        unsafe_allow_html=True
    )

with m3:

    st.markdown(
        f"""
        <div class="metric-card">

        <h3>🤖</h3>

        <h2>{ai_readiness}%</h2>

        <p>AI Readiness</p>

        </div>
        """,
        unsafe_allow_html=True
    )

with m4:

    st.markdown(
        f"""
        <div class="metric-card">
          <h3>🏅</h3>
          <h2>{len(certificates)}</h2>
          <p>Certificates</p>

        </div>
        """,
        unsafe_allow_html=True
    )
# ==========================================================
# HIGH SCHOOL CAREER ACTIONS
# ==========================================================

st.subheader("🚀 Explore Your Career")

c1, c2, c3 = st.columns(3, gap="large")

with c1:

    st.markdown(
        """
        <div class="action-card">

        <h1>🎯</h1>

        <h3>Career Assessment</h3>

        <p>
        Discover careers that match your interests.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "Take Assessment",
        key="career_assessment",
        use_container_width=True
    ):
        st.switch_page(
            "pages/school_career.py"
        )


    st.markdown(
        """
        <div class="action-card">

        <h1>📚</h1>

        <h3>Learning Roadmap</h3>

        <p>
        Follow your personalized learning journey.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "View Roadmap",
        key="school_roadmap",
        use_container_width=True
    ):
        st.switch_page(
            "pages/school_roadmap.py"
        )


with c2:

    st.markdown(
        """
        <div class="action-card">
          <h1>📝</h1>
          <h3>Skill Assessment</h3>
          <p>Test your knowledge and improve your skills.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "Start Assessment",
        key="school_assessment",
        use_container_width=True
    ):
        st.switch_page(
            "pages/school_assessment.py"
        )


    st.markdown(
        """
        <div class="action-card">
          <h1>🔔</h1>
          <h3>Notifications</h3>
          <p>Scholarships, competitions and opportunities.</p>

        </div>
        """,
        unsafe_allow_html=True
    )


    if st.button(
        "View Notifications",
        key="school_notifications",
        use_container_width=True
    ):
        st.switch_page(
            "pages/school_notifications.py"
        )


with c3:

    st.markdown(
        """
        <div class="action-card">
          <h1>🤖</h1>
          <h3>AI Tools</h3>
          <p>Get AI-powered career guidance.</p>

        </div>
        """,
        unsafe_allow_html=True
    )


    if st.button(
        "Open AI Tools",
        key="school_ai_tools",
        use_container_width=True
    ):
        st.switch_page(
            "pages/school_ai_tools.py"
        )


    st.markdown(
        """
        <div class="action-card">
          <h1>📊</h1>
          <h3>Student Report</h3>
          <p>View your complete academic and career report.</p>

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "View Report",
        key="school_report",
        use_container_width=True
    ):
        st.switch_page(
            "pages/school_reports.py"
        )
# ==========================================================
# PROGRESS OVERVIEW
# ==========================================================

st.write("")

st.subheader("📈 My Progress")

p1, p2, p3 = st.columns(3)

with p1:

    st.markdown(
        f"""
        <div class="small-progress-card">

        <span>👤 Profile</span>

        <h3>{profile_completion}%</h3>

        <p>Profile Completion</p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(
        min(profile_completion, 100) / 100
    )


with p2:

    st.markdown(
        f"""
        <div class="small-progress-card">

        <span>📚 Learning</span>

        <h3>{learning_percentage}%</h3>

        <p>Learning Progress</p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(
        min(learning_percentage, 100) / 100
    )


with p3:

    st.markdown(
        f"""
        <div class="small-progress-card">

        <span>🤖 AI Readiness</span>

        <h3>{ai_readiness}%</h3>

        <p>Career Preparation</p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(
        min(ai_readiness, 100) / 100
    )
#=========================================================
# AI TOOLS
# ==========================================================
# ==========================================================
# AI TOOLS
# ==========================================================

st.write("")
st.subheader("🤖 AI Career Tools")

a1, a2, a3 = st.columns(3)

with a1:

    if st.button(
        "🎯 Career Recommendation",
        use_container_width=True
    ):
        st.switch_page(
            "pages/career_recommendation.py"
        )

with a2:

    if st.button(
        "🗺 AI Learning Roadmap",
        use_container_width=True
    ):
        st.switch_page(
            "pages/learning_roadmap.py"
        )

with a3:

    if st.button(
        "💬 AI Career Chatbot",
        use_container_width=True
    ):
        st.switch_page(
            "pages/chatbot.py"
        )