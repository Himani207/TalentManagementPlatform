import streamlit as st

from utils.session import logout

from utils.school_db import (
    create_student_table,
    create_learning_progress_table,
    get_student_profile,
    get_learning_progress,
    update_learning_progress
)


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Learning Roadmap",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# CREATE TABLES
# ==========================================================

create_student_table()
create_learning_progress_table()


# ==========================================================
# LOGIN CHECK
# ==========================================================

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.switch_page("pages/login.py")
    st.stop()


email = st.session_state.email


# ==========================================================
# GET STUDENT PROFILE
# ==========================================================

student = get_student_profile(email)

if not student:
    student = {
        "email": email,
        "age": "",
        "class": "",
        "school": "",
        "interests": "",
        "subject": "",
        "career": "",
        "goal": ""
    }


student_name = st.session_state.get(
    "name",
    email.split("@")[0].title()
)

student_class = student.get("class", "")
subject = student.get("subject", "")
interests = student.get("interests", "")
career = student.get("career", "")
goal = student.get("goal", "")


# ==========================================================
# LEARNING PROGRESS
# ==========================================================

learning = get_learning_progress(email)

progress = learning.get(
    "progress_percentage",
    0
)

completed_topics = learning.get(
    "completed_topics",
    0
)

total_topics = learning.get(
    "total_topics",
    0
)

current_level = learning.get(
    "current_level",
    "Beginner"
)


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
    <style>

    .roadmap-header {
        padding: 28px;
        border-radius: 20px;
        margin-bottom: 25px;
        background: linear-gradient(
            135deg,
            rgba(102,126,234,0.18),
            rgba(118,75,162,0.12)
        );
        border: 1px solid rgba(128,128,128,0.18);
    }

    .roadmap-header h1 {
        margin-bottom: 8px;
    }

    .roadmap-header p {
        font-size: 16px;
        opacity: 0.8;
    }

    .roadmap-card {
        padding: 22px;
        border-radius: 18px;
        margin-bottom: 18px;
        border: 1px solid rgba(128,128,128,0.18);
        background: rgba(255,255,255,0.05);
    }

    .roadmap-card h3 {
        margin-bottom: 8px;
    }

    .video-card {
        padding: 18px;
        border-radius: 16px;
        border: 1px solid rgba(128,128,128,0.18);
        margin-bottom: 15px;
    }

    .metric-card {
        padding: 20px;
        border-radius: 18px;
        text-align: center;
        border: 1px solid rgba(128,128,128,0.18);
        background: rgba(255,255,255,0.05);
    }

    </style>
    """,
    unsafe_allow_html=True
)


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

    # Only add pages that actually exist
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
        f"""
        <div class="roadmap-header">
          <h1>📚 Learning Roadmap</h1>
          <p>Welcome, {student_name} 👋</p>
          <p>Follow your personalized learning journey based on your interests and career goals.</p>

        </div>
        """,
        unsafe_allow_html=True
    )


with right:

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):
        logout()
        st.switch_page("app.py")


# ==========================================================
# STUDENT PROFILE SUMMARY
# ==========================================================

st.subheader("🎯 Your Learning Profile")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown(
        f"""
        <div class="metric-card">
          <h3>🏫</h3>
          <h4>Class</h4>
          <p>{student_class or "Not selected"}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


with c2:

    st.markdown(
        f"""
        <div class="metric-card">
          <h3>📚</h3>
          <h4>Subject</h4>
          <p>{subject or "Not selected"}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


with c3:

    st.markdown(
        f"""
        <div class="metric-card">
          <h3>🎯</h3>
          <h4>Career</h4>
          <p>{career or "Not selected"}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


with c4:

    st.markdown(
        f"""
        <div class="metric-card">
          <h3>📈</h3>
          <h4>Level</h4>
          <p>{current_level}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# PROGRESS
# ==========================================================

st.write("")

st.subheader("📈 Your Roadmap Progress")

st.progress(
    min(progress, 100) / 100
)

st.write(
    f"**{progress}% completed** • "
    f"{completed_topics} of {total_topics} topics completed"
)


# ==========================================================
# DYNAMIC ROADMAP DATA
# ==========================================================

roadmap = []


# ==========================================================
# COMPUTER / PROGRAMMING CAREER
# ==========================================================

if (
    "software" in career.lower()
    or "engineer" in career.lower()
    or "program" in interests.lower()
    or "computer" in interests.lower()
    or "coding" in interests.lower()
):

    roadmap = [

        {
            "title": "Python Fundamentals",
            "description": "Learn variables, data types, conditions, loops and functions.",
            "subject": "Programming",
            "duration": "2 weeks",
            "video": "https://www.youtube.com/watch?v=rfscVS0vtbw",
            "video_name": "Learn Python - Full Course for Beginners"
        },

        {
            "title": "Problem Solving",
            "description": "Practice logical thinking and basic programming problems.",
            "subject": "Programming",
            "duration": "2 weeks",
            "video": "https://www.youtube.com/results?search_query=python+problem+solving+beginners",
            "video_name": "Python Problem Solving"
        },

        {
            "title": "Data Structures Basics",
            "description": "Understand arrays, lists, stacks, queues and dictionaries.",
            "subject": "Computer Science",
            "duration": "3 weeks",
            "video": "https://www.youtube.com/results?search_query=data+structures+for+beginners",
            "video_name": "Data Structures for Beginners"
        },

        {
            "title": "Web Development",
            "description": "Learn HTML, CSS and basic JavaScript.",
            "subject": "Web Development",
            "duration": "3 weeks",
            "video": "https://www.youtube.com/results?search_query=HTML+CSS+JavaScript+for+beginners",
            "video_name": "HTML CSS JavaScript"
        },

        {
            "title": "Build a Project",
            "description": "Create a small website or Python project.",
            "subject": "Project",
            "duration": "2 weeks",
            "video": "https://www.youtube.com/results?search_query=beginner+Python+project",
            "video_name": "Python Beginner Project"
        }

    ]


# ==========================================================
# BIOLOGY / MEDICAL CAREER
# ==========================================================

elif (
    "doctor" in career.lower()
    or "medical" in career.lower()
    or "biology" in interests.lower()
):

    roadmap = [

        {
            "title": "Cell Biology",
            "description": "Learn cells, organelles and cellular organization.",
            "subject": "Biology",
            "duration": "2 weeks",
            "video": "https://www.youtube.com/results?search_query=Khan+Academy+high+school+biology+cells",
            "video_name": "High School Biology - Cells"
        },

        {
            "title": "Human Biology",
            "description": "Understand major systems of the human body.",
            "subject": "Biology",
            "duration": "3 weeks",
            "video": "https://www.youtube.com/results?search_query=Khan+Academy+human+biology",
            "video_name": "Human Biology"
        },

        {
            "title": "Genetics",
            "description": "Learn DNA, genes, inheritance and variation.",
            "subject": "Biology",
            "duration": "3 weeks",
            "video": "https://www.youtube.com/results?search_query=Khan+Academy+genetics",
            "video_name": "Genetics"
        },

        {
            "title": "Ecology",
            "description": "Study ecosystems, biodiversity and environmental systems.",
            "subject": "Biology",
            "duration": "2 weeks",
            "video": "https://www.youtube.com/results?search_query=Khan+Academy+high+school+biology+ecology",
            "video_name": "High School Biology - Ecology"
        },

        {
            "title": "Science Practice",
            "description": "Solve biology questions and practice scientific reasoning.",
            "subject": "Science",
            "duration": "2 weeks",
            "video": "https://www.youtube.com/results?search_query=biology+practice+questions+high+school",
            "video_name": "Biology Practice"
        }

    ]


# ==========================================================
# SCIENCE CAREER
# ==========================================================

elif (
    "science" in subject.lower()
    or "scientist" in career.lower()
    or "research" in interests.lower()
):

    roadmap = [

        {
            "title": "Scientific Method",
            "description": "Learn observation, hypothesis, experiments and conclusions.",
            "subject": "Science",
            "duration": "1 week",
            "video": "https://www.youtube.com/results?search_query=scientific+method+for+students",
            "video_name": "Scientific Method"
        },

        {
            "title": "Physics Fundamentals",
            "description": "Learn motion, force, energy and basic physics.",
            "subject": "Physics",
            "duration": "3 weeks",
            "video": "https://www.youtube.com/results?search_query=high+school+physics+basics",
            "video_name": "High School Physics"
        },

        {
            "title": "Chemistry Fundamentals",
            "description": "Learn atoms, elements, reactions and chemical bonding.",
            "subject": "Chemistry",
            "duration": "3 weeks",
            "video": "https://www.youtube.com/results?search_query=high+school+chemistry+basics",
            "video_name": "High School Chemistry"
        },

        {
            "title": "Research Skills",
            "description": "Learn how to investigate questions and present findings.",
            "subject": "Research",
            "duration": "2 weeks",
            "video": "https://www.youtube.com/results?search_query=research+skills+for+students",
            "video_name": "Research Skills"
        }

    ]


# ==========================================================
# DEFAULT ACADEMIC ROADMAP
# ==========================================================

else:

    roadmap = [

        {
            "title": "Mathematics Foundation",
            "description": "Strengthen algebra, geometry and problem-solving skills.",
            "subject": "Mathematics",
            "duration": "3 weeks",
            "video": "https://www.youtube.com/results?search_query=high+school+mathematics+basics",
            "video_name": "High School Mathematics"
        },

        {
            "title": "Science Foundation",
            "description": "Review important concepts from physics, chemistry and biology.",
            "subject": "Science",
            "duration": "3 weeks",
            "video": "https://www.youtube.com/results?search_query=high+school+science+basics",
            "video_name": "High School Science"
        },

        {
            "title": "Communication Skills",
            "description": "Improve English communication, vocabulary and presentation.",
            "subject": "English",
            "duration": "2 weeks",
            "video": "https://www.youtube.com/results?search_query=English+communication+skills+students",
            "video_name": "Communication Skills"
        },

        {
            "title": "Digital Skills",
            "description": "Learn computer fundamentals, internet safety and productivity tools.",
            "subject": "Technology",
            "duration": "2 weeks",
            "video": "https://www.youtube.com/results?search_query=computer+basics+for+students",
            "video_name": "Computer Basics"
        },

        {
            "title": "Career Exploration",
            "description": "Explore different careers and identify your strengths.",
            "subject": "Career",
            "duration": "1 week",
            "video": "https://www.youtube.com/results?search_query=career+exploration+for+high+school+students",
            "video_name": "Career Exploration"
        }

    ]


# ==========================================================
# ROADMAP
# ==========================================================

st.write("")

st.subheader("🗺 Your Personalized Roadmap")

st.caption(
    f"This roadmap is generated using your "
    f"career preference, interests and academic profile."
)


# ==========================================================
# TOPIC LOOP
# ==========================================================

for index, topic in enumerate(roadmap):

    topic_number = index + 1

    st.markdown(
        f"""
        <div class="roadmap-card">
          <h3>{topic_number}. {topic["title"]}</h3>
          <p>{topic["description"]}</p>
          <p>
            📚 <b>Area:</b> {topic["subject"]}
            &nbsp;&nbsp;&nbsp;
            ⏱ <b>Duration:</b> {topic["duration"]}
          </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    # ----------------------------------------------
    # VIDEO
    # ----------------------------------------------

    st.markdown(
        f"""
        <div class="video-card">
          <h4>🎥 Recommended Learning Video</h4>
          <p>{topic["video_name"]}</p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.link_button(
        "▶️ Watch Learning Video",
        topic["video"],
        use_container_width=True
    )

    # ----------------------------------------------
    # COMPLETION
    # ----------------------------------------------

    completed = st.checkbox(
        "✅ Mark topic as completed",
        key=f"topic_{index}"
    )

    st.divider()


# ==========================================================
# UPDATE PROGRESS
# ==========================================================

st.write("")

if st.button(
    "💾 Save My Roadmap Progress",
    use_container_width=True
):

    completed_count = 0

    for index in range(len(roadmap)):

        if st.session_state.get(
            f"topic_{index}",
            False
        ):
            completed_count += 1

    total_count = len(roadmap)

    new_progress = update_learning_progress(
        email,
        completed_count,
        total_count
    )

    st.success(
        f"🎉 Progress saved! You completed "
        f"{completed_count}/{total_count} topics."
    )

    st.rerun()


# ==========================================================
# CAREER GOAL
# ==========================================================

st.write("")

st.subheader("🎯 Your Career Goal")

if career:

    st.success(
        f"Your current career goal is **{career}**."
    )

else:

    st.info(
        "Select a dream career in your Student Profile "
        "to receive a more personalized roadmap."
    )


# ==========================================================
# LEARNING TIP
# ==========================================================

st.write("")

st.subheader("💡 Learning Tip")

st.info(
    "Study one topic at a time, watch the recommended "
    "video, practice what you learned, and then mark "
    "the topic as completed."
)