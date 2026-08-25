import streamlit as st
from ai.roadmap_ai import roadmap

st.title("📚 AI Learning Roadmap")

goal = st.text_input(
    "Career Goal"
)

if st.button("Generate Roadmap"):

    with st.spinner("Generating..."):

        answer = roadmap(goal)

        st.markdown(answer)