import streamlit as st
from ai.skill_gap import skill_gap

st.title("📊 AI Skill Gap Analysis")

current = st.text_area(
    "Current Skills"
)

target = st.text_input(
    "Target Career"
)

if st.button("Analyze"):

    with st.spinner("Analyzing..."):

        answer = skill_gap(
            current,
            target
        )

        st.markdown(answer)