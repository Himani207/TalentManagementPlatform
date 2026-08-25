import streamlit as st
import pandas as pd

from utils.professional_db import get_all_professionals


st.set_page_config(
    page_title="Admin Professional Management",
    page_icon="💼",
    layout="wide"
)


if not st.session_state.get("admin_logged_in"):

    st.switch_page("pages/admin_login.py")


st.title("💼 Professional Management")


professionals = get_all_professionals()


if professionals:

    df = pd.DataFrame(professionals)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No professional records found.")