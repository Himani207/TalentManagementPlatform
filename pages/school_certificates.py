import streamlit as st
import os
import uuid
from utils.session import logout

from utils.school_db import (
    create_certificate_table,
    get_certificates,
    add_certificate,
    delete_certificate
)


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Certificates",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# LOGIN CHECK
# ==========================================================

if (
    "logged_in" not in st.session_state
    or not st.session_state.logged_in
):
    st.warning("Please login first.")
    st.switch_page("pages/login.py")
    st.stop()


email = st.session_state.email


# ==========================================================
# DATABASE
# ==========================================================

create_certificate_table()


# ==========================================================
# GET CERTIFICATES
# ==========================================================

certificates = get_certificates(email)


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("🏫 TalentSphere Elevate")
    st.caption("High School Student Portal")

    st.divider()

    st.page_link(
        "pages/school.py",
        label="🏠 Dashboard"
    )

    st.page_link(
        "pages/school_profile.py",
        label="👤 Student Profile"
    )

    st.page_link(
        "pages/school_career.py",
        label="🎯 Career Assessment"
    )

    st.page_link(
        "pages/school_roadmap.py",
        label="📚 Learning Roadmap"
    )

    st.page_link(
        "pages/school_assessment.py",
        label="📝 Skill Assessment"
    )

    st.page_link(
        "pages/school_certificates.py",
        label="🏅 Certificates"
    )

    st.page_link(
        "pages/school_notifications.py",
        label="🔔 Notifications"
    )

    st.page_link(
        "pages/school_reports.py",
        label="📊 Reports"
    )

    st.page_link(
        "pages/school_ai_tools.py",
        label="🤖 AI Tools"
    )

    st.page_link(
        "pages/chatbot.py",
        label="💬 AI Chatbot"
    )

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):
        logout()
        st.switch_page("app.py")


# ==========================================================
# HEADER
# ==========================================================

st.title("🏅 My Certificates")

st.write(
    "View and manage your academic, technical, "
    "and professional certificates."
)

st.divider()


# ==========================================================
# SUMMARY
# ==========================================================

total_certificates = len(certificates)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "🏅 Total Certificates",
        total_certificates
    )

with col2:

    completed_count = sum(
        1
        for certificate in certificates
        if certificate.get("status") == "Completed"
    )

    st.metric(
        "✅ Completed",
        completed_count
    )

with col3:

    in_progress_count = sum(
        1
        for certificate in certificates
        if certificate.get("status") == "In Progress"
    )

    st.metric(
        "📚 In Progress",
        in_progress_count
    )


st.write("")
st.divider()


# ==========================================================
# ADD CERTIFICATE
# ==========================================================
st.subheader("➕ Add Certificate")
with st.form("add_certificate_form"):

    col1, col2 = st.columns(2)

    with col1:

        certificate_name = st.text_input(
            "Certificate Name",
            placeholder="Example: Python Basics"
        )

        provider = st.text_input(
            "Provider / Organization",
            placeholder="Example: Coursera"
        )

        issue_date = st.date_input(
            "Issue Date"
        )

    with col2:

        certificate_file = st.file_uploader(
            "Upload Certificate",
            type=["png", "jpg", "jpeg", "pdf"],
            help="Upload your certificate image or PDF."
        )

        status = st.selectbox(
            "Status",
            [
                "Completed",
                "In Progress"
            ]
        )

    submitted = st.form_submit_button(
        "💾 Add Certificate",
        use_container_width=True
    )
# ==========================================================
# SAVE CERTIFICATE
# ==========================================================
if submitted:

    if not certificate_name.strip():

        st.error(
            "⚠️ Please enter the certificate name."
        )

    elif certificate_file is None:

        st.error(
            "⚠️ Please upload your certificate."
        )

    else:

        # Create certificate folder
        certificate_folder = "assets/certificates"

        os.makedirs(
            certificate_folder,
            exist_ok=True
        )

        # Get file extension
        file_extension = os.path.splitext(
            certificate_file.name
        )[1].lower()

        # Create unique filename
        unique_filename = (
            f"{email.replace('@', '_').replace('.', '_')}_"
            f"{uuid.uuid4().hex}"
            f"{file_extension}"
        )

        # Complete file path
        file_path = os.path.join(
            certificate_folder,
            unique_filename
        )

        # Save uploaded certificate
        with open(file_path, "wb") as f:

            f.write(
                certificate_file.getbuffer()
            )

        # Save certificate information in database
        add_certificate(
            email=email,
            certificate_name=certificate_name.strip(),
            provider=provider.strip(),
            issue_date=str(issue_date),
            certificate_file=file_path,
            status=status
        )

        st.success(
            "✅ Certificate added successfully!"
        )

        st.rerun()
# ==========================================================
# CERTIFICATE LIST
# ==========================================================

st.write("")
st.divider()

st.subheader(
    f"📜 My Certificates ({len(certificates)})"
)


if not certificates:

    st.info(
        "🏅 No certificates have been added yet."
    )

else:

    for certificate in certificates:

        certificate_id = certificate["id"]

        certificate_name = (
            certificate.get("certificate_name")
            or "Untitled Certificate"
        )

        provider = (
            certificate.get("provider")
            or "Provider not specified"
        )

        issue_date = (
            certificate.get("issue_date")
            or "Date not specified"
        )

        status = (
            certificate.get("status")
            or "Completed"
        )

        certificate_file = (
            certificate.get("certificate_file")
            or ""
        )

        # --------------------------------------------------
        # CERTIFICATE CARD
        # --------------------------------------------------

        col1, col2 = st.columns([6, 1])

        with col1:

            st.markdown(
                f"""
                <div style="
                    padding:22px;
                    border-radius:18px;
                    border:1px solid rgba(128,128,128,0.2);
                    margin-bottom:15px;
                ">
                  <h3>🏅 {certificate_name}</h3>
                  <p>
                    <b>Provider:</b> {provider}
                  </p>
                  <p>
                    <b>Issue Date:</b> {issue_date}
                  </p>
                  <p>
                    <b>Status:</b> {status}
                  </p>

                </div>
                """,
                unsafe_allow_html=True
            )

            if certificate_file:

                file_extension = os.path.splitext(
                    certificate_file
                )[1].lower()

                if file_extension in [".png", ".jpg", ".jpeg"]:

                    st.image(
                        certificate_file,
                        caption="Certificate",
                        width=500
                    )

                elif file_extension == ".pdf":

                    with open(certificate_file, "rb") as f:

                        pdf_data = f.read()

                    st.download_button(
                        "📄 View / Download Certificate",
                        data=pdf_data,
                        file_name=os.path.basename(
                            certificate_file
                        ),
                        mime="application/pdf",
                        key=f"certificate_file_{certificate_id}"
                    )


        with col2:

            if st.button(
                "🗑️ Delete",
                key=f"delete_certificate_{certificate_id}",
                use_container_width=True
            ):

                delete_certificate(
                    certificate_id,
                    email
                )

                st.success(
                    "Certificate deleted successfully."
                )

                st.rerun()

