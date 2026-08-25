import streamlit as st

from utils.session import logout

from utils.school_db import (
    create_student_table,
    create_report_table,
    create_learning_progress_table,
    create_certificate_table,
    create_notification_table,
    get_student_profile,
    calculate_profile_completion,
    calculate_ai_readiness,
    get_career_match,
    get_learning_progress,
    get_certificates,
)

# ==========================================================
# CREATE TABLES
# ==========================================================

create_student_table()
create_report_table()
create_learning_progress_table()
create_certificate_table()
create_notification_table()

# ==========================================================
# LOGIN CHECK
# ==========================================================

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.switch_page("pages/login.py")
    st.stop()

email = st.session_state.email

# ==========================================================
# GET STUDENT DATA
# ==========================================================

student = get_student_profile(email)

if student is None:
    st.error("Student profile not found.")
    st.stop()

# ==========================================================
# DYNAMIC DATA
# ==========================================================

profile_completion = calculate_profile_completion(email)

ai_readiness = calculate_ai_readiness(email)

career_result = get_career_match(email)

learning = get_learning_progress(email)

certificates = get_certificates(email)

learning_progress = learning.get(
    "progress_percentage",
    0
)

career_name = career_result.get(
    "career",
    "Not Selected"
)

career_match = career_result.get(
    "match",
    0
)

certificate_count = len(certificates)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="AI Tools",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CSS
# ==========================================================

try:
    with open("assets/style.css", "r", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
except:
    pass

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

    # Only add these if the files exist
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
# HEADER
# ==========================================================

left, right = st.columns([6, 1])

with left:

    st.markdown(
        """
        <div class="dashboard-title">
            🤖 <span>AI Career Tools</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with right:

    if st.button(
        "🚪 Logout",
        key="top_logout"
    ):
        logout()
        st.switch_page("app.py")

# ==========================================================
# WELCOME
# ==========================================================

student_name = st.session_state.get(
    "name",
    "Student"
)

st.markdown(
    f"""
    <div class="welcome-card">
      <h2>
         Hello, {student_name} 👋
      </h2>
      <p>
        Use AI-powered tools to understand your career,
        improve your skills and plan your learning journey.
      </p>

    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# ==========================================================
# AI READINESS OVERVIEW
# ==========================================================

st.subheader("🤖 Your AI Career Readiness")

m1, m2, m3, m4 = st.columns(4)

with m1:

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

with m2:

    st.markdown(
        f"""
        <div class="metric-card">
          <h3>🎯</h3>
          <h2>{career_match}%</h2>
          <p>Career Match</p>

        </div>
        """,
        unsafe_allow_html=True
    )

with m3:

    st.markdown(
        f"""
        <div class="metric-card">
          <h3>📚</h3>
          <h2>{learning_progress}%</h2>
          <p>Learning Progress</p>

        </div>
        """,
        unsafe_allow_html=True
    )

with m4:

    st.markdown(
        f"""
        <div class="metric-card">
          <h3>🏅</h3>
          <h2>{certificate_count}</h2>
          <p>Certificates</p>

        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================================
# CAREER RECOMMENDATION
# ==========================================================

st.write("")
st.subheader("🎯 AI Career Recommendation")

career_col1, career_col2 = st.columns([2, 1])

with career_col1:

    st.markdown(
        f"""
        <div class="action-card">
          <h1>💼</h1>
          <h2>{career_name}</h2>
          <p>
            Based on your current profile, interests
            and favourite subject.
          </p>
          <h3>
            Career Match: {career_match}%
          </h3>

        </div>
        """,
        unsafe_allow_html=True
    )

with career_col2:

    st.metric(
        "Profile Completion",
        f"{profile_completion}%"
    )

    st.progress(
        min(profile_completion, 100) / 100
    )

# ==========================================================
# AI TOOLS
# ==========================================================

st.write("")
st.subheader("🧠 AI-Powered Tools")

a1, a2, a3 = st.columns(3)

# ----------------------------------------------------------
# CAREER RECOMMENDATION
# ----------------------------------------------------------

with a1:

    st.markdown(
        """
        <div class="action-card">
          <h1>🎯</h1>
          <h3>Career Recommendation</h3>
          <p>
            Discover careers that match your
            interests, subjects and goals.
          </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "Explore Careers",
        key="ai_career",
        use_container_width=True
    ):

        st.switch_page(
            "pages/school_career.py"
        )

# ----------------------------------------------------------
# LEARNING ROADMAP
# ----------------------------------------------------------

with a2:

    st.markdown(
        """
        <div class="action-card">
          <h1>🗺️</h1>
          <h3>AI Learning Roadmap</h3>
          <p>
            Follow a personalized learning path
            based on your career goal.
          </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "View Roadmap",
        key="ai_roadmap",
        use_container_width=True
    ):

        st.switch_page(
            "pages/school_roadmap.py"
        )

# ----------------------------------------------------------
# AI CHATBOT
# ----------------------------------------------------------

with a3:

    st.markdown(
        """
        <div class="action-card">
          <h1>💬</h1>
          <h3>AI Career Chatbot</h3>
          <p>
            Ask questions about careers,
            subjects, skills and opportunities.
          </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "Ask AI",
        key="ai_chatbot",
        use_container_width=True
    ):

        st.switch_page(
            "pages/chatbot.py"
        )

# ==========================================================
# PERSONALIZED AI INSIGHTS
# ==========================================================

st.write("")
st.subheader("💡 Personalized AI Insights")

insight1, insight2 = st.columns(2)

with insight1:

    if profile_completion < 50:

        st.warning(
            "👤 Complete your student profile to get "
            "better AI career recommendations."
        )

    elif profile_completion < 80:

        st.info(
            "📋 Your profile is partially complete. "
            "Add more interests and goals for better recommendations."
        )

    else:

        st.success(
            "✅ Your profile is well completed. "
            "AI recommendations can be more personalized."
        )

with insight2:

    if learning_progress < 30:

        st.warning(
            "📚 Start your learning roadmap to improve "
            "your career preparation."
        )

    elif learning_progress < 70:

        st.info(
            "📈 You are making progress. "
            "Continue completing your learning topics."
        )

    else:

        st.success(
            "🚀 Excellent learning progress! "
            "Keep building your skills."
        )

# ==========================================================
# AI READINESS
# ==========================================================

st.write("")
st.subheader("📈 AI Readiness Progress")

st.progress(
    min(ai_readiness, 100) / 100
)

if ai_readiness >= 80:

    st.success(
        "🌟 Excellent! You are highly prepared "
        "for your future career journey."
    )

elif ai_readiness >= 60:

    st.info(
        "👍 Good progress! Continue improving your "
        "skills and completing your roadmap."
    )

elif ai_readiness >= 40:

    st.warning(
        "📚 You are getting started. Focus on your "
        "learning roadmap and skill assessment."
    )

else:

    st.warning(
        "🚀 Start building your profile, skills and "
        "learning progress to improve your readiness."
    )

# ==========================================================
# STUDENT INFORMATION USED BY AI
# ==========================================================

st.write("")
st.subheader("🧑‍🎓 AI Profile Context")

c1, c2, c3 = st.columns(3)

with c1:

    st.info(
        f"🏫 Class: {student.get('class') or 'Not selected'}"
    )

with c2:

    st.info(
        f"📚 Favourite Subject: "
        f"{student.get('subject') or 'Not selected'}"
    )

with c3:

    st.info(
        f"🎯 Dream Career: "
        f"{student.get('career') or 'Not selected'}"
    )

# ==========================================================
# INTERESTS
# ==========================================================

interests = student.get(
    "interests",
    ""
)

st.write("")

if interests:

    st.subheader("💡 Your Interests")

    interest_list = [
        item.strip()
        for item in interests.split(",")
        if item.strip()
    ]

    cols = st.columns(
        min(len(interest_list), 4)
    )

    for index, interest in enumerate(interest_list):

        with cols[index % len(cols)]:

            st.info(
                f"⭐ {interest}"
            )

else:

    st.info(
        "Add your interests to your Student Profile "
        "to receive more personalized AI recommendations."
    )