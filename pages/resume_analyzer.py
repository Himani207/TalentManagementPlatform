import streamlit as st
from ai.resume_ai import analyze_resume
from utils.pdf_report import create_report

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Analyzer")

st.write("Upload your Resume (PDF)")

uploaded_file = st.file_uploader(
    "Choose Resume",
    type=["pdf"]
)
if "resume_result" not in st.session_state:
    st.session_state.resume_result = ""

if uploaded_file:

    st.success("Resume Uploaded Successfully")

    if st.button("Analyze Resume"):

        with st.spinner("Analyzing Resume..."):

            st.session_state.resume_result = analyze_resume(uploaded_file)

if st.session_state.resume_result:

    st.success("Analysis Completed ✅")

    st.markdown(st.session_state.resume_result)

    pdf_file = create_report(st.session_state.resume_result)

    with open(pdf_file, "rb") as f:

        st.download_button(
            label="📄 Download PDF Report",
            data=f,
            file_name="AI_Report.pdf",
            mime="application/pdf"
        )