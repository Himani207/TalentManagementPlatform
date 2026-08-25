import streamlit as st
from utils.coding_db import get_xp
import utils.coding_db as coding_db
coding_db.create_saved_code_table()
# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Coding Practice",
    page_icon="💻",
    layout="wide"
)
coding_db.create_coding_tables()

# ==========================================================
# LOGIN CHECK
# ==========================================================

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.switch_page("pages/login.py")

email = st.session_state.email

# ==========================================================
# LOAD DATABASE
# ==========================================================
questions = coding_db.get_questions()

if not questions:
    coding_db.insert_questions()
    questions = coding_db.get_questions()
total_questions = len(questions)

total_solved = coding_db.solved_count(email)
xp = get_xp(email)

level = xp // 100 + 1

easy_total = coding_db.difficulty_count("Easy")
medium_total = coding_db.difficulty_count("Medium")
hard_total = coding_db.difficulty_count("Hard")

easy_solved = coding_db.solved_by_difficulty(email, "Easy")
medium_solved = coding_db.solved_by_difficulty(email, "Medium")
hard_solved = coding_db.solved_by_difficulty(email, "Hard")

# ==========================================================
# HEADER
# ==========================================================

st.title("💻 Coding Practice")

st.caption(
    "Solve coding problems, track your progress, and prepare for technical interviews."
)

st.divider()

# ==========================================================
# DASHBOARD METRICS
# ==========================================================

m1, m2, m3, m4, m5, m6 = st.columns(6)
with m1:
    st.metric(
        "Solved",
        f"{total_solved}/{total_questions}"
    )
with m2:
    st.metric(
        "⭐ XP",
        xp
    )

with m3:
    st.metric(
        "🏅 Level",
        level
    )

with m4:
    st.metric(
        "Easy",
        f"{easy_solved}/{easy_total}"
    )

with m5:
    st.metric(
        "Medium",
        f"{medium_solved}/{medium_total}"
    )

with m6:
    st.metric(
        "Hard",
        f"{hard_solved}/{hard_total}"
    )


st.divider()

# ==========================================================
# SEARCH BAR
# ==========================================================

search = st.text_input(
    "🔍 Search Coding Question",
    placeholder="Example: Two Sum"
)

# ==========================================================
# FILTERS
# ==========================================================

c1, c2 = st.columns(2)

with c1:

    difficulty = st.selectbox(
        "Difficulty",
        [
            "All",
            "Easy",
            "Medium",
            "Hard"
        ]
    )

with c2:

    topic = st.selectbox(
        "Topic",
        [
            "All",
            "Arrays",
            "Strings",
            "Linked List",
            "Stack",
            "Queue",
            "Trees",
            "Graphs",
            "DP",
            "Backtracking"
        ]
    )
# ==========================================================
# LOAD FILTERED QUESTIONS
# ==========================================================
all_questions = coding_db.get_questions()

questions = coding_db.get_filtered_questions(
    difficulty,
    topic
)

# ==========================================================
# SEARCH FILTER
# ==========================================================

if search:

    questions = [

        q

        for q in questions

        if search.lower() in q["title"].lower()

    ]

st.divider()

st.subheader("📚 Coding Questions")
# ==========================================================
# QUESTION CARDS
# ==========================================================

if not questions:

    st.info("No coding questions found.")

else:

    for q in questions:

        question_solved = coding_db.is_solved(
            email,
            q["id"]
        )

        with st.container(border=True):

            left, right = st.columns([5, 1])

            # -----------------------------------------
            # LEFT SIDE
            # -----------------------------------------

            with left:

                st.subheader(q["title"])

                # Difficulty Badge
                if q["difficulty"] == "Easy":
                    st.success("🟢 Easy")

                elif q["difficulty"] == "Medium":
                    st.warning("🟡 Medium")

                else:
                    st.error("🔴 Hard")

                st.write(f"**📂 Topic:** {q['topic']}")
                st.caption(q["description"])

            # -----------------------------------------
            # RIGHT SIDE
            # -----------------------------------------
            with right:

                if question_solved:
                    st.success("✅ Solved")

                if st.button(
                    "💻 Open Problem",
                    key=f"open_{q['id']}",
                    use_container_width=True
                ):
                    st.session_state.question_id = q["id"]
                    st.switch_page("pages/coding_problem.py")
# ==========================================================
# PROGRESS OVERVIEW
# ==========================================================

st.subheader("📈 Progress Overview")

progress = (
    total_solved / total_questions
    if total_questions > 0 else 0
)

st.progress(progress)

st.info(
    f"You have solved **{total_solved}** out of **{total_questions}** coding problems."
)

st.divider()

# ==========================================================
# DIFFICULTY PROGRESS
# ==========================================================

st.subheader("🎯 Difficulty-wise Progress")

c1, c2, c3 = st.columns(3)

with c1:

    st.write("🟢 Easy")

    easy_progress = (
        easy_solved / easy_total
        if easy_total > 0 else 0
    )

    st.progress(easy_progress)

    st.caption(f"{easy_solved} / {easy_total} Solved")


with c2:

    st.write("🟡 Medium")

    medium_progress = (
        medium_solved / medium_total
        if medium_total > 0 else 0
    )

    st.progress(medium_progress)

    st.caption(f"{medium_solved} / {medium_total} Solved")


with c3:

    st.write("🔴 Hard")

    hard_progress = (
        hard_solved / hard_total
        if hard_total > 0 else 0
    )

    st.progress(hard_progress)

    st.caption(f"{hard_solved} / {hard_total} Solved")

st.divider()

# ==========================================================
# DAILY CHALLENGE
# ==========================================================
st.subheader("🔥 Daily Challenge")

daily = None

for q in all_questions:
    if not coding_db.is_solved(email, q["id"]):
        daily = q
        break

if daily:

    st.success(f"""
### {daily["title"]}

📚 **Topic:** {daily["topic"]}

🎯 **Difficulty:** {daily["difficulty"]}

📝 {daily["description"]}
""")

    if st.button(
        "🚀 Solve Daily Challenge",
        use_container_width=True
    ):
        st.session_state.question_id = daily["id"]
        st.switch_page("pages/coding_problem.py")

else:

    st.success(
        "🏆 You have completed all coding challenges!"
    )

st.divider()

# ==========================================================
# AI RECOMMENDATIONS
# ==========================================================

st.subheader("🤖 AI Learning Recommendations")

if easy_solved < easy_total:

    st.info("""
### Recommended Next Step

✔ Finish all Easy problems.

Focus on:

• Arrays

• Strings

• Linked Lists
""")

elif medium_solved < medium_total:

    st.info("""
### Recommended Next Step

✔ Move to Medium level.

Practice:

• Trees

• Graphs

• Dynamic Programming
""")

elif hard_solved < hard_total:

    st.info("""
### Recommended Next Step

Excellent progress!

Now practice:

• Hard Graphs

• DP

• Backtracking

to prepare for FAANG interviews.
""")

else:

    st.success("""
### Congratulations 🎉

You have completed every coding problem.

Keep revising and participate in weekly contests.
""")

st.divider()
# ==========================================================
# PLACEMENT READINESS
# ==========================================================

st.subheader("🎯 Placement Readiness")

placement_score = int(progress * 100)

c1, c2 = st.columns([1, 2])

with c1:
    st.metric(
        "Readiness Score",
        f"{placement_score}%"
    )

with c2:

    if placement_score < 25:

        st.error("""
🚨 Beginner Level

Focus on solving Easy coding problems and strengthening programming fundamentals.
""")

    elif placement_score < 50:

        st.warning("""
📚 Developing

You are making good progress.

Continue solving Easy and Medium questions consistently.
""")

    elif placement_score < 75:

        st.info("""
💼 Placement Ready

You have a solid foundation.

Practice Graphs, Trees, and Dynamic Programming to improve further.
""")

    elif placement_score < 100:

        st.success("""
🌟 Interview Ready

Excellent work!

Continue solving Hard problems and participate in coding contests.
""")

    else:

        st.balloons()

        st.success("""
🏆 Outstanding!

You have solved every coding problem.

You are highly prepared for technical interviews.
""")

st.divider()

# ==========================================================
# ACHIEVEMENTS
# ==========================================================

st.subheader("🏆 Achievements")

b1, b2 = st.columns(2)

with b1:

    if total_solved >= 5:
        st.success("🥉 Beginner Coder")

    if total_solved >= 10:
        st.success("🏅 Rising Programmer")

    if total_solved >= 20:
        st.success("🥈 Consistent Solver")

    if total_solved >= 30:
        st.success("🥇 Coding Expert")

with b2:

    if easy_solved == easy_total and easy_total > 0:
        st.success("🟢 Easy Master")

    if medium_solved == medium_total and medium_total > 0:
        st.success("🟡 Medium Master")

    if hard_solved == hard_total and hard_total > 0:
        st.success("🔴 Hard Master")

    if total_questions > 0 and total_solved == total_questions:
        st.success("👑 Coding Champion")

st.divider()

# ==========================================================
# OVERALL SUMMARY
# ==========================================================

st.subheader("📊 Performance Summary")

summary1, summary2, summary3 = st.columns(3)

with summary1:
    st.metric(
        "Questions Solved",
        total_solved
    )

with summary2:
    st.metric(
        "Remaining",
        total_questions - total_solved
    )

with summary3:
    st.metric(
        "Completion",
        f"{placement_score}%"
    )

st.divider()

# ==========================================================
# MOTIVATION
# ==========================================================

if placement_score < 40:

    st.info(
        "💡 Consistency is more important than speed. Solve at least 2 problems every day."
    )

elif placement_score < 70:

    st.info(
        "🚀 Great progress! Start practicing Medium-level interview questions regularly."
    )

elif placement_score < 90:

    st.success(
        "🔥 You're very close to being interview-ready. Keep challenging yourself with Hard problems."
    )

else:

    st.success(
        "🎉 Fantastic work! Maintain your skills through contests, mock interviews, and revision."
    )

st.divider()

# ==========================================================
# FOOTER
# ==========================================================

st.caption(
    "Talent Management Platform• AI-Powered Coding Practice • Track Progress • Build Placement Readiness"
)