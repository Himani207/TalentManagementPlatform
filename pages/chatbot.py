import streamlit as st

from ai.chatbot import career_chat
from utils.chat_db import (
    save_chat,
    get_chat_history,
    delete_chat_history
)

st.set_page_config(
    page_title="AI Career Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 TalentSphere AI Career Chatbot")

st.write("Ask anything about careers, placements, coding, AI, internships, or resumes.")

# ----------------------------
# Login Check
# ----------------------------

if "logged_in" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

# ----------------------------
# Previous Chat History
# ----------------------------

st.sidebar.title("📜 Previous Chats")

history = get_chat_history(st.session_state.email)

if history:

    for q, a in history:

        with st.sidebar.expander(q):

            st.write(a)

else:

    st.sidebar.info("No previous chats.")

# ----------------------------
# Clear Chat
# ----------------------------

if st.sidebar.button("🗑 Clear Chat History"):

    delete_chat_history(st.session_state.email)

    st.success("Chat history deleted.")

    st.rerun()

# ----------------------------
# Chat Session
# ----------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

question = st.chat_input("Ask your career question...")

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            category = st.session_state.get(
                "category",
                "General"
            )

            answer = career_chat(
                question,
                category
            )

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    save_chat(
        st.session_state.email,
        question,
        answer
    )