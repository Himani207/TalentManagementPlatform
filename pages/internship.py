import streamlit as st

from utils.internship_db import (
    save_internship,
    get_internships,
    get_internship_score
)


# -----------------------------
# Page Config
# -----------------------------

st.set_page_config(
    page_title="Internship Experience",
    page_icon="💼",
    layout="wide"
)


# -----------------------------
# Login Check
# -----------------------------

if "logged_in" not in st.session_state:
    st.switch_page("pages/login.py")


email = st.session_state.email



# -----------------------------
# Header
# -----------------------------

st.title("💼 Internship Experience")

st.write(
    "Add your internship details to improve your placement readiness score."
)



# -----------------------------
# Internship Form
# -----------------------------

st.subheader("➕ Add Internship")


with st.form("internship_form"):

    col1, col2 = st.columns(2)


    with col1:

        company = st.text_input(
            "🏢 Company Name"
        )

        role = st.text_input(
            "💻 Internship Role"
        )


    with col2:

        duration = st.selectbox(
            "⏳ Duration",
            [
                "1 Month",
                "2 Months",
                "3 Months",
                "6 Months",
                "12 Months"
            ]
        )


        internship_type = st.selectbox(
            "🌐 Internship Type",
            [
                "Remote",
                "On-site",
                "Hybrid"
            ]
        )


    description = st.text_area(
        "📝 Work Description"
    )


    submit = st.form_submit_button(
        "Save Internship"
    )



if submit:

    if company and role:

        save_internship(
            email=email,
            company=company,
            role=role,
            duration=duration,
            internship_type=internship_type,
            description=description
        )


        st.success(
            "✅ Internship Added Successfully"
        )

        st.rerun()


    else:

        st.warning(
            "Please enter company and role"
        )



# -----------------------------
# Internship List
# -----------------------------

st.divider()

st.subheader("📋 My Internships")
internships = get_internships(email)
st.metric(
    "Total Internships",
    len(internships)
)



if internships:


    for internship in internships:


        with st.container():

            st.markdown(
            f"""
            ### 🏢 {internship['company']}

            **Role:** {internship['role']}

            **Duration:** {internship['duration']}

            **Type:** {internship['internship_type']}

            **Description:**

            {internship['description']}
            """
            )


            st.divider()



else:

    st.info(
        "No internship records found."
    )



# -----------------------------
# Internship Score
# -----------------------------
st.subheader("🎯 Internship Contribution")

st.caption(
    "Internship experience contributes 10% to your Placement Readiness Score."
)
score = get_internship_score(email)
col1, col2 = st.columns(2)
with col1:

    st.metric(
        "Internship Readiness",
        f"{score}%"
    )


with col2:


    if score >= 80:

        status = "Excellent 🚀"

    elif score >= 50:

        status = "Good 👍"

    else:

        status = "Need More Experience"



    st.metric(
        "Status",
        status
    )



st.progress(
    score / 100
)