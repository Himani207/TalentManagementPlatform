import streamlit as st

from utils.session import logout

from utils.school_db import (
    create_student_table,
    create_report_table,
    create_learning_progress_table,
    create_certificate_table,
    create_notification_table,
    get_student_profile,
    get_student_report,
)


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Student Report",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================================
# CREATE REQUIRED TABLES
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
# GET STUDENT REPORT
# ==========================================================

student_profile = get_student_profile(email)

if student_profile is None:
    st.error("Student profile not found.")
    st.stop()


report = get_student_report(email)

if report is None:
    st.warning("No student report available.")
    st.stop()


# ==========================================================
# EXTRACT DATA
# ==========================================================

student_data = report.get("student", {})

profile_completion = report.get(
    "profile_completion",
    0
)

assessment_score = report.get(
    "assessment",
    0
)

learning = report.get(
    "learning",
    {}
)

learning_progress = learning.get(
    "progress_percentage",
    0
)

learning_level = learning.get(
    "current_level",
    "Beginner"
)

total_topics = learning.get(
    "total_topics",
    0
)

completed_topics = learning.get(
    "completed_topics",
    0
)

certificates = report.get(
    "certificates",
    []
)

certificate_count = report.get(
    "certificate_count",
    len(certificates)
)

ai_readiness = report.get(
    "ai_readiness",
    0
)

career_match_data = report.get(
    "career_match",
    {}
)

career_name = career_match_data.get(
    "career",
    "Not Selected"
)

career_match = career_match_data.get(
    "match",
    0
)

notifications = report.get(
    "notifications",
    []
)

notification_count = report.get(
    "notification_count",
    len(notifications)
)

unread_notifications = report.get(
    "unread_notifications",
    0
)


# ==========================================================
# STUDENT NAME
# ==========================================================

student_name = st.session_state.get(
    "name",
    email.split("@")[0].title()
)


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
    <style>

    .report-header {
        padding: 30px;
        border-radius: 20px;
         margin-bottom: 25px;
        background: linear-gradient(
            135deg,
            rgba(102, 126, 234, 0.18),
            rgba(118, 75, 162, 0.12)
        );
        border: 1px solid rgba(128, 128, 128, 0.18);
    }

    .report-header h1 {
        margin-bottom: 8px;
    }

    .report-header p {
        margin-bottom: 0;
        font-size: 16px;
         opacity: 0.8;
    }

    .metric-card {
        padding: 22px;
        border-radius: 18px;
        text-align: center;
        min-height: 150px;
        border: 1px solid rgba(128, 128, 128, 0.18);
        background: rgba(255, 255, 255, 0.05);
    }

    .metric-card h1 {
        margin: 5px;
    }
    .metric-card h3 {
        margin: 5px;
    }

    .metric-card p {
        margin-top: 8px;
        opacity: 0.7;
    }

    .report-card {
        padding: 22px;
        border-radius: 18px;
        min-height: 150px;
        border: 1px solid rgba(128, 128, 128, 0.18);
        background: rgba(255, 255, 255, 0.05);
    }
    .report-card h3 {
        margin-bottom: 10px;
    }

    .certificate-card {
        padding: 20px;
        border-radius: 16px;
        margin-bottom: 15px;
        border: 1px solid rgba(128, 128, 128, 0.18);
        background: rgba(255, 255, 255, 0.05);
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================================
# LOAD EXISTING CSS
# ==========================================================

try:

    with open(
        "assets/style.css",
        "r",
        encoding="utf-8"
    ) as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

except FileNotFoundError:
    pass


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("🏫 TalentSphere Elevate")

    st.caption(
        "High School Student Portal"
    )

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
        <div class="report-header">
          <h1>
            📊 Student Report
          </h1>
          <p>
            Your academic, learning and career
            development overview.
          </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with right:

    if st.button(
        "🚪 Logout",
        key="top_logout",
        use_container_width=True
    ):

        logout()

        st.switch_page("app.py")


# ==========================================================
# STUDENT WELCOME
# ==========================================================

st.markdown(
    f"""
    <div class="report-card">
      <h2>
        👋 Welcome, {student_name}
      </h2>
      <p>
        Here is your latest TalentSphere Elevate
        progress report.
      </p>
      <p>
        <b>Email:</b> {email}
      </p>

    </div>
    """,
    unsafe_allow_html=True
)


st.write("")


# ==========================================================
# STUDENT INFORMATION
# ==========================================================

st.subheader("👤 Student Information")

info1, info2, info3, info4 = st.columns(4)


with info1:

    st.info(
        f"🎓 Class: "
        f"{student_data.get('class') or 'Not selected'}"
    )


with info2:

    st.info(
        f"🏫 School: "
        f"{student_data.get('school') or 'Not added'}"
    )


with info3:

    st.info(
        f"📚 Subject: "
        f"{student_data.get('favorite_subject') or 'Not selected'}"
    )


with info4:

    st.info(
        f"🎯 Career: "
        f"{student_data.get('dream_career') or 'Not selected'}"
    )


# ==========================================================
# OVERALL PERFORMANCE
# ==========================================================

st.write("")

st.subheader("📈 Overall Performance")

m1, m2, m3, m4 = st.columns(4)


with m1:

    st.markdown(
        f"""
        <div class="metric-card">
          <h3>👤</h3>
          <h1>{profile_completion}%</h1>
          <p>Profile Completion</p>

        </div>
        """,
        unsafe_allow_html=True
    )


with m2:

    st.markdown(
        f"""
        <div class="metric-card">
          <h3>📝</h3>
          <h1>{assessment_score}%</h1>
          <p>Assessment Score</p>

        </div>
        """,
        unsafe_allow_html=True
    )


with m3:

    st.markdown(
        f"""
        <div class="metric-card">
          <h3>📚</h3>
          <h1>{learning_progress}%</h1>
          <p>Learning Progress</p>

        </div>
        """,
        unsafe_allow_html=True
    )


with m4:

    st.markdown(
        f"""
        <div class="metric-card">
          <h3>🤖</h3>
          <h1>{ai_readiness}%</h1>
          <p>AI Readiness</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# DEVELOPMENT PROGRESS
# ==========================================================

st.write("")

st.subheader("📊 Development Progress")

p1, p2, p3 = st.columns(3)


with p1:

    st.write("👤 Profile")

    st.write(
        f"**{profile_completion}% Complete**"
    )

    st.progress(
        min(max(profile_completion, 0), 100) / 100
    )


with p2:

    st.write("📚 Learning")

    st.write(
        f"**{learning_progress}% Complete**"
    )

    st.progress(
        min(max(learning_progress, 0), 100) / 100
    )

    st.caption(
        f"Level: {learning_level}"
    )


with p3:

    st.write("🤖 AI Readiness")

    st.write(
        f"**{ai_readiness}%**"
    )

    st.progress(
        min(max(ai_readiness, 0), 100) / 100
    )


# ==========================================================
# CAREER ANALYSIS
# ==========================================================

st.write("")

st.subheader("🎯 Career Analysis")

career1, career2 = st.columns([2, 1])


with career1:

    st.markdown(
        f"""
        <div class="report-card">
          <h1>💼</h1>
          <h2>
            {career_name}
          </h2>
          <p>
            Your current career direction
            based on your student profile.
          </p>
          <h3>
            Career Match: {career_match}%
          </h3>

        </div>
        """,
        unsafe_allow_html=True
    )


with career2:

    st.metric(
        "Career Match",
        f"{career_match}%"
    )

    st.progress(
        min(max(career_match, 0), 100) / 100
    )

    if career_match >= 80:

        st.success(
            "🌟 Excellent career compatibility!"
        )

    elif career_match >= 60:

        st.info(
            "👍 Good career compatibility."
        )

    elif career_match > 0:

        st.warning(
            "📚 Explore more skills to improve your match."
        )

    else:

        st.info(
            "Complete your profile to calculate your match."
        )


# ==========================================================
# LEARNING REPORT
# ==========================================================

st.write("")

st.subheader("📚 Learning Report")

l1, l2, l3, l4 = st.columns(4)


with l1:

    st.metric(
        "Total Topics",
        total_topics
    )


with l2:

    st.metric(
        "Completed Topics",
        completed_topics
    )


with l3:

    st.metric(
        "Progress",
        f"{learning_progress}%"
    )


with l4:

    st.metric(
        "Current Level",
        learning_level
    )


# ==========================================================
# LEARNING PROGRESS BAR
# ==========================================================

st.write("")

st.write(
    f"### 📚 Learning Progress: {learning_progress}%"
)

st.progress(
    min(max(learning_progress, 0), 100) / 100
)


if total_topics > 0:

    remaining_topics = max(
        total_topics - completed_topics,
        0
    )

    st.caption(
        f"{completed_topics} topics completed "
        f"• {remaining_topics} topics remaining"
    )

else:

    st.caption(
        "No learning topics have been added yet."
    )


# ==========================================================
# CERTIFICATES
# ==========================================================

st.write("")

st.subheader(
    f"🏅 Certificates ({certificate_count})"
)

if certificates:

    for certificate in certificates:

        certificate_name = certificate.get(
            "certificate_name",
            "Certificate"
        )

        provider = certificate.get(
            "provider",
            "Unknown Provider"
        )

        issue_date = certificate.get(
            "issue_date",
            "Not available"
        )

        status = certificate.get(
            "status",
            "Completed"
        )

        certificate_link = certificate.get(
            "certificate_link",
            ""
        )

        st.markdown(
            f"""
            <div class="certificate-card">
              <h3>🏅 {certificate_name}</h3>
              <p>
                <b>Provider:</b> {provider}
              </p>
              <p>
                <b>Issue Date:</b> {issue_date}
              </p>
              <p>
                <b>Status:</b> {status}
              </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        if certificate_link:

            st.link_button(
                "🔗 View Certificate",
                certificate_link
            )

else:

    st.info(
        "🏅 No certificates have been added yet."
    )


# ==========================================================
# NOTIFICATIONS
# ==========================================================

st.write("")

st.subheader("🔔 Notification Summary")

n1, n2 = st.columns(2)


with n1:

    st.metric(
        "Total Notifications",
        notification_count
    )


with n2:

    st.metric(
        "Unread Notifications",
        unread_notifications
    )


# ==========================================================
# INTERESTS & GOALS
# ==========================================================

st.write("")

st.subheader("💡 Interests & Goals")

interest_col, goal_col = st.columns(2)


with interest_col:

    interests = student_data.get(
        "interests",
        ""
    )

    st.markdown(
        f"""
        <div class="report-card">
          <h3>💡 Your Interests</h3>
          <p>
            {interests if interests else "No interests added yet."}
          </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with goal_col:

    goal = student_data.get(
        "goal",
        ""
    )

    st.markdown(
        f"""
        <div class="report-card">
          <h3>🎯 Short-Term Goal</h3>
          <p>
            {goal if goal else "No short-term goal added yet."}
          </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# AI READINESS ANALYSIS
# ==========================================================

st.write("")

st.subheader("🤖 AI Readiness Analysis")

r1, r2 = st.columns([1, 2])


with r1:

    st.metric(
        "AI Readiness",
        f"{ai_readiness}%"
    )

    st.progress(
        min(max(ai_readiness, 0), 100) / 100
    )


with r2:

    if ai_readiness >= 80:

        st.success(
            "🌟 Excellent! Your career preparation "
            "and learning progress are strong."
        )

    elif ai_readiness >= 60:

        st.info(
            "👍 Good progress! Continue your learning "
            "roadmap and complete more assessments."
        )

    elif ai_readiness >= 40:

        st.warning(
            "📚 You are making progress. Focus on "
            "learning activities, assessments and certificates."
        )

    else:

        st.warning(
            "🚀 Start by completing your profile, "
            "learning topics and assessments."
        )


# ==========================================================
# REPORT SUMMARY
# ==========================================================

st.write("")

st.subheader("📝 Report Summary")

summary_points = []

summary_points.append(
    f"Profile completion: {profile_completion}%"
)

summary_points.append(
    f"Assessment score: {assessment_score}%"
)

summary_points.append(
    f"Learning progress: {learning_progress}%"
)

summary_points.append(
    f"AI readiness: {ai_readiness}%"
)

summary_points.append(
    f"Career match: {career_match}%"
)

summary_points.append(
    f"Certificates earned: {certificate_count}"
)

for point in summary_points:

    st.write(
        f"✅ {point}"
    )


# ==========================================================
# PERSONALIZED RECOMMENDATION
# ==========================================================

st.write("")

st.subheader("💡 Personalized Recommendation")


recommendations = []


if profile_completion < 100:

    recommendations.append(
        "Complete your student profile for a more accurate career recommendation."
    )


if assessment_score < 60:

    recommendations.append(
        "Take the career/skill assessment again and explore different subjects."
    )


if learning_progress < 50:

    recommendations.append(
        "Complete more topics from your learning roadmap."
    )


if certificate_count == 0:

    recommendations.append(
        "Complete relevant courses and add certificates to your profile."
    )


if career_match < 60:

    recommendations.append(
        "Explore skills related to your selected career to improve your career match."
    )


if not recommendations:

    recommendations.append(
        "🌟 Excellent work! Keep learning and building skills toward your career goal."
    )


for recommendation in recommendations:

    st.info(
        f"💡 {recommendation}"
    )


# ==========================================================
# GENERATE REPORT
# ==========================================================

st.write("")

st.subheader("📄 Generate Report")


report_text = f"""
TALENTSPHERE ELEVATE
STUDENT DEVELOPMENT REPORT
========================================

Student Name: {student_name}
Email: {email}

ACADEMIC INFORMATION
----------------------------------------
Class: {student_data.get('class') or 'Not selected'}
School: {student_data.get('school') or 'Not added'}
Favourite Subject: {student_data.get('favorite_subject') or 'Not selected'}

CAREER INFORMATION
----------------------------------------
Dream Career: {student_data.get('dream_career') or 'Not selected'}
Career Match: {career_match}%

PERFORMANCE
----------------------------------------
Profile Completion: {profile_completion}%
Assessment Score: {assessment_score}%
Learning Progress: {learning_progress}%
Learning Level: {learning_level}
AI Readiness: {ai_readiness}%

LEARNING
----------------------------------------
Total Topics: {total_topics}
Completed Topics: {completed_topics}

CERTIFICATES
----------------------------------------
Certificates: {certificate_count}

NOTIFICATIONS
----------------------------------------
Total Notifications: {notification_count}
Unread Notifications: {unread_notifications}

INTERESTS
----------------------------------------
{student_data.get('interests') or 'No interests added'}

SHORT-TERM GOAL
----------------------------------------
{student_data.get('goal') or 'No goal added'}

CAREER RECOMMENDATION
----------------------------------------
{career_name}

Generated by TalentSphere Elevate
"""


st.download_button(
    label="📥 Download Student Report",
    data=report_text,
    file_name=f"{student_name}_student_report.txt",
    mime="text/plain",
    use_container_width=True
)


# ==========================================================
# REFRESH REPORT
# ==========================================================

st.write("")

if st.button(
    "🔄 Refresh Report",
    use_container_width=True
):

    st.cache_data.clear()
    st.rerun()