import streamlit as st
from ai.career_ai import recommend_career
st.set_page_config(page_title="AI Career Recommendation")

st.title(" AI Career Recommendation")

category = st.selectbox(
    "Category",
    [
        "High School Student",
        "College Student",
        "Working Professional"
    ]
)

skills = st.text_area(
    "Your Skills",
    placeholder="Python, HTML, SQL..."
)

interests = st.text_area(
    "Your Interests",
    placeholder="AI, Web Development..."
)

if st.button("Generate Recommendation"):

    with st.spinner("Thinking..."):

        result = recommend_career(
            category,
            skills,
            interests
        )

        st.markdown(result)