import streamlit as st
def create_session(name, email, role):

    st.session_state.logged_in = True

    st.session_state.name = name

    st.session_state.email = email
    st.session_state.role = role

def logout():

    st.session_state.logged_in = False

    st.session_state.name = ""

    st.session_state.email = ""

    st.session_state.role = ""


def is_logged_in():

    return st.session_state.logged_in