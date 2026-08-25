import streamlit as st
import pandas as pd

from utils.college_db import get_all_college_students


st.set_page_config(
    page_title="Admin College Management",
    page_icon="🎓",
    layout="wide"
)


if not st.session_state.get("admin_logged_in"):

    st.switch_page("pages/admin_login.py")


st.title("🎓 College Management")


students = get_all_college_students()


if students:

    df = pd.DataFrame(students)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No college students found.")