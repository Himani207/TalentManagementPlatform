import streamlit as st
import pandas as pd

from utils.school_db import get_all_students
from utils.session import logout


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Admin School Management",
    page_icon="🎒",
    layout="wide"
)


# ==========================================================
# ADMIN AUTH CHECK
# ==========================================================

if not st.session_state.get("admin_logged_in"):

    st.warning("Please login as admin first")

    st.switch_page(
        "pages/admin_login.py"
    )


# ==========================================================
# HEADER
# ==========================================================

col1, col2 = st.columns([5,1])


with col1:

    st.title("🎒 School Management")

    st.caption(
        "Manage registered high school students"
    )


with col2:

    if st.button("🚪 Logout"):

        logout()

        st.switch_page(
            "app.py"
        )


st.markdown("---")


# ==========================================================
# LOAD STUDENTS
# ==========================================================

try:

    students = get_all_students()

except Exception as e:

    st.error(
        f"Database Error: {e}"
    )

    students = []



# ==========================================================
# STUDENT DATA
# ==========================================================

if students:

    df = pd.DataFrame(students)


    # Metrics

    c1,c2 = st.columns(2)


    with c1:

        st.metric(
            "Total School Students",
            len(df)
        )


    with c2:

        st.metric(
            "Database Status",
            "Connected"
        )


    st.markdown("---")


    # Search

    search = st.text_input(
        "🔍 Search Student"
    )


    if search:

        df = df[
            df.astype(str)
            .apply(
                lambda row:
                row.str.contains(
                    search,
                    case=False
                ).any(),
                axis=1
            )
        ]


    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


else:

    st.info(
        "No school students found."
    )