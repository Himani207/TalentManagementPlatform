import streamlit as st
from utils.college_db import save_profile, get_profile


st.set_page_config(
    page_title="Edit Profile",
    page_icon="✏️",
    layout="wide"
)


if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("pages/login.py")


email = st.session_state.email

profile = get_profile(email)


st.title("✏️ Edit Profile")


with st.form("profile_form"):

    full_name = st.text_input(
        "Full Name",
        value=profile["full_name"] if profile else ""
    )


    phone = st.text_input(
        "Phone Number",
        value=profile["phone"] if profile else ""
    )


    location = st.text_input(
        "Location",
        value=profile["location"] if profile else ""
    )


    college = st.text_input(
        "College Name",
        value=profile["college"] if profile else ""
    )


    degree = st.text_input(
        "Degree",
        value=profile["degree"] if profile else ""
    )


    department = st.text_input(
        "Branch",
        value=profile["department"] if profile else ""
    )


    year = st.selectbox(
        "Year",
        [
            "1st Year",
            "2nd Year",
            "3rd Year",
            "4th Year"
        ]
    )


    skills = st.text_area(
        "Skills",
        value=profile["skills"] if profile else ""
    )
    cgpa = st.text_input(
        "CGPA",
        value=profile["cgpa"] if profile else ""
    )
    projects = st.text_area(
        "Projects",
        value=profile["projects"] if profile else "",
        placeholder="Project name, description, technologies"
    )
    certifications = st.text_area(
        "Certifications",
        value=profile["certifications"] if profile else "",
        placeholder="Python, AWS, SQL"
    )


    career_goals = st.text_area(
        "Career Goals",
        value=profile["career_goals"] if profile else ""
    )


    ai_insights = st.text_area(
        "AI Career Insights",
        value=profile["ai_insights"] if profile else ""
    )


    about = st.text_area(
        "About",
        value=profile["about"] if profile else ""
    )


    submit = st.form_submit_button(
        "💾 Save Profile"
    )


    if submit:

        save_profile(
            email,
            full_name,
            college,
            degree,
            department,
            year,
            phone,
            location,
            skills,
            about,
            cgpa,
            projects,
            certifications,
            career_goals,
            ai_insights
        )


        st.success("Profile Updated Successfully!")

        st.switch_page("pages/profile.py")