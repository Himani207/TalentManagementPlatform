import streamlit as st
from datetime import datetime

from utils.session import logout
from utils.school_db import (
    create_student_table,
    create_report_table,
    create_learning_progress_table,
    create_certificate_table,
    create_notification_table,
    get_student_profile,
    get_notifications,
    mark_notification_read,
    generate_student_notifications,
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Notifications | TalentSphere Elevate",
    page_icon="🔔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# DATABASE
# ==========================================================

create_student_table()
create_report_table()
create_learning_progress_table()
create_certificate_table()
create_notification_table()

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
# STUDENT PROFILE
# ==========================================================

student = get_student_profile(email)

if student is None:
    st.error("Student profile not found.")
    st.stop()

student_name = st.session_state.get(
    "name",
    email.split("@")[0].title()
)


# ==========================================================
# GENERATE DYNAMIC NOTIFICATIONS
# ==========================================================

generate_student_notifications(email)

# ==========================================================
# LOAD NOTIFICATIONS
# ==========================================================

notifications = get_notifications(email)

if notifications is None:
    notifications = []


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def is_notification_read(notification):
    value = notification.get("is_read", False)

    if isinstance(value, str):
        return value.lower() in (
            "1",
            "true",
            "yes",
            "read",
        )

    return bool(value)


def get_notification_type(notification):
    return str(
        notification.get("type", "General")
    ).strip() or "General"


def get_notification_icon(notification_type):
    icons = {
        "career": "🎯",
        "assessment": "📝",
        "learning": "📚",
        "course": "🎓",
        "certificate": "🏆",
        "achievement": "🏅",
        "ai": "🤖",
        "academic": "📖",
        "reminder": "⏰",
        "system": "⚙️",
        "general": "🔔",
    }

    return icons.get(
        notification_type.lower(),
        "🔔"
    )


def get_priority(notification):
    priority = str(
        notification.get("priority", "Normal")
    ).strip()

    if not priority:
        priority = "Normal"

    return priority


def format_date(value):
    if not value:
        return "Recently"

    try:
        if isinstance(value, datetime):
            dt = value

        else:
            value = str(value)

            formats = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d %H:%M",
                "%Y-%m-%d",
                "%d-%m-%Y %H:%M:%S",
                "%d-%m-%Y %H:%M",
            ]

            dt = None

            for fmt in formats:
                try:
                    dt = datetime.strptime(
                        value,
                        fmt
                    )
                    break

                except ValueError:
                    continue

            if dt is None:
                return value

        return dt.strftime(
            "%d %b %Y • %I:%M %p"
        )

    except Exception:
        return str(value)


# ==========================================================
# CALCULATE METRICS
# ==========================================================

total_notifications = len(notifications)

unread_notifications = sum(
    1
    for notification in notifications
    if not is_notification_read(notification)
)

read_notifications = (
    total_notifications
    - unread_notifications
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
    <style>

    .notification-hero {
        padding: 30px 34px;
        border-radius: 24px;
        margin-bottom: 28px;
        border: 1px solid rgba(128,128,128,0.16);
        background:
            linear-gradient(
                135deg,
                rgba(99,102,241,0.15),
                rgba(168,85,247,0.10)
            );
    }

    .notification-hero h1 {
        margin: 0;
        font-size: 32px;
        font-weight: 750;
    }

    .notification-hero p {
        margin-top: 8px;
        margin-bottom: 0;
        opacity: 0.72;
        font-size: 15px;
    }

    .metric-card {
        padding: 22px;
        border-radius: 20px;
        border: 1px solid rgba(128,128,128,0.16);
        background: rgba(255,255,255,0.04);
        min-height: 145px;
        transition: 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(99,102,241,0.35);
    }

    .metric-icon {
        font-size: 25px;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 30px;
        font-weight: 750;
        margin: 0;
    }

    .metric-label {
        margin-top: 5px;
        opacity: 0.65;
        font-size: 13px;
    }

    .notification-card {
        padding: 20px 22px;
        border-radius: 18px;
        margin-bottom: 14px;
        border: 1px solid rgba(128,128,128,0.16);
        background: rgba(255,255,255,0.035);
        transition: 0.2s ease;
    }

    .notification-card:hover {
        transform: translateY(-2px);
        border-color: rgba(99,102,241,0.35);
        box-shadow: 0 10px 30px rgba(0,0,0,0.06);
    }

    .notification-unread {
        border-left: 4px solid #6366f1;
        background: rgba(99,102,241,0.07);
    }

    .notification-title {
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .notification-message {
        font-size: 14px;
        line-height: 1.6;
        opacity: 0.78;
        margin-bottom: 12px;
    }

    .notification-meta {
        font-size: 12px;
        opacity: 0.58;
    }

    .new-badge {
        display: inline-block;
        padding: 4px 9px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 650;
        background: rgba(99,102,241,0.14);
        color: #6366f1;
    }

    .read-badge {
        display: inline-block;
        padding: 4px 9px;
        border-radius: 999px;
        font-size: 11px;
        opacity: 0.65;
        background: rgba(128,128,128,0.12);
    }

    .category-card {
        padding: 18px;
        border-radius: 17px;
        border: 1px solid rgba(128,128,128,0.16);
        background: rgba(255,255,255,0.035);
        text-align: center;
    }

    .category-number {
        font-size: 25px;
        font-weight: 750;
    }

    .category-name {
        font-size: 13px;
        opacity: 0.65;
        margin-top: 4px;
    }

    .empty-state {
        text-align: center;
        padding: 55px 20px;
        border-radius: 22px;
        border: 1px dashed rgba(128,128,128,0.25);
        background: rgba(128,128,128,0.025);
    }

    .empty-state-icon {
        font-size: 48px;
    }

    .empty-state h3 {
        margin-top: 10px;
    }

    .empty-state p {
        opacity: 0.6;
    }

    </style>
    """,
    unsafe_allow_html=True
)

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
# HERO
# ==========================================================

st.markdown(
    f"""
    <div class="notification-hero">
      <h1>🔔 Notifications</h1>
      <p>
        Welcome back, {student_name} 👋
      </p>
      <p>
        Stay updated with your learning progress,
        assessments, achievements and career opportunities.
      </p>

    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# METRICS
# ==========================================================

st.subheader("📊 Notification Overview")

m1, m2, m3 = st.columns(3)

with m1:

    st.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-icon">🔔</div>
          <div class="metric-value">
            {total_notifications}
          </div>
          <div class="metric-label">
            Total Notifications
          </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with m2:

    st.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-icon">📩</div>
          <div class="metric-value">
            {unread_notifications}
          </div>
          <div class="metric-label">
            Unread Notifications
          </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with m3:

    st.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-icon">✅</div>
          <div class="metric-value">
            {read_notifications}
          </div>
          <div class="metric-label">
            Read Notifications
          </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================================
# FILTERS
# ==========================================================

st.write("")

st.subheader("🔎 Find Notifications")

filter_col, category_col, search_col = st.columns(
    [1.2, 1.5, 3]
)

with filter_col:

    notification_filter = st.selectbox(
        "Status",
        [
            "All",
            "Unread",
            "Read"
        ]
    )

with category_col:

    available_categories = sorted(
        list(
            set(
                get_notification_type(n)
                for n in notifications
            )
        )
    )

    category_options = [
        "All Categories"
    ] + available_categories

    selected_category = st.selectbox(
        "Category",
        category_options
    )

with search_col:

    search = st.text_input(
        "Search",
        placeholder="🔍 Search notifications..."
    )

# ==========================================================
# FILTER NOTIFICATIONS
# ==========================================================

filtered_notifications = []

for notification in notifications:

    read_status = is_notification_read(
        notification
    )

    notification_type = get_notification_type(
        notification
    )

    # Status filter

    if (
        notification_filter == "Unread"
        and read_status
    ):
        continue

    if (
        notification_filter == "Read"
        and not read_status
    ):
        continue

    # Category filter

    if (
        selected_category != "All Categories"
        and notification_type != selected_category
    ):
        continue

    # Search filter

    if search:

        search_text = (
            str(
                notification.get(
                    "title",
                    ""
                )
            )
            + " "
            + str(
                notification.get(
                    "message",
                    ""
                )
            )
            + " "
            + notification_type
        ).lower()

        if search.lower() not in search_text:
            continue

    filtered_notifications.append(
        notification
    )

# ==========================================================
# RESULT COUNT
# ==========================================================

st.caption(
    f"Showing {len(filtered_notifications)} "
    f"of {total_notifications} notifications"
)

# ==========================================================
# NOTIFICATION LIST
# ==========================================================

st.write("")

st.subheader("📬 Your Notifications")

if not filtered_notifications:

    if notifications:

        st.markdown(
            """
            <div class="empty-state">
              <div class="empty-state-icon">
                🔍
              </div>
              <h3>
                No matching notifications
              </h3>
              <p>
                Try changing your filters or
                search for something else.
              </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="empty-state">
              <div class="empty-state-icon">🎉</div>
              <h3>
                You're all caught up!
              </h3>
              <p>
                New learning opportunities,
                achievements and important updates
                will appear here.
              </p>

            </div>
            """,
            unsafe_allow_html=True
        )

else:

    for index, notification in enumerate(
        filtered_notifications
    ):

        title = notification.get(
            "title",
            "Notification"
        )

        message = notification.get(
            "message",
            ""
        )

        notification_type = get_notification_type(
            notification
        )

        priority = get_priority(
            notification
        )

        created_at = notification.get(
            "created_at",
            ""
        )

        read_status = is_notification_read(
            notification
        )

        icon = get_notification_icon(
            notification_type
        )

        if read_status:

            badge = (
                '<span class="read-badge">'
                '✓ Read'
                '</span>'
            )

            card_class = "notification-card"

        else:

            badge = (
                '<span class="new-badge">'
                '● New'
                '</span>'
            )

            card_class = (
                "notification-card "
                "notification-unread"
            )

        # --------------------------------------------------
        # NOTIFICATION CARD
        # --------------------------------------------------
        st.markdown(
            f"""
            <div class="{card_class}">
              <div style="
                display:flex;
                justify-content:space-between;
                align-items:flex-start;
                gap:15px;
               ">
                <div style="
                  display:flex;
                  gap:13px;
                  align-items:flex-start;
                ">
                  <div style="
                    font-size:26px;
                  ">
                    {icon}
                  </div>
                  <div>
                    <div class="notification-title">
                    {title}
                    </div>
                    <div class="notification-meta">
                      {notification_type}
                      &nbsp; • &nbsp;
                      {priority}
                    </div>
                </div>
                <div>{badge}</div>
              </div>
              <div class="notification-message">{message}</div>
              <div class="notification-meta">🕒 {format_date(created_at)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        # --------------------------------------------------
        # MARK AS READ
        # --------------------------------------------------

        if not read_status:

            if st.button(
                "✓ Mark as Read",
                key=f"read_{index}",
                use_container_width=False
            ):

                notification_id = notification.get(
                    "id"
                )

                if notification_id is not None:

                    try:

                        mark_notification_read(
                            notification_id
                        )

                        st.success(
                            "Notification marked as read."
                        )

                        st.rerun()

                    except Exception as error:

                        st.error(
                            f"Unable to update notification: {error}"
                        )

                else:

                    st.warning(
                        "Notification ID not found."
                    )

# ==========================================================
# CATEGORY SUMMARY
# ==========================================================

st.write("")
st.divider()

st.subheader("📌 Notification Categories")

if notifications:

    notification_types = {}

    for notification in notifications:

        notification_type = get_notification_type(
            notification
        )

        notification_types[
            notification_type
        ] = (
            notification_types.get(
                notification_type,
                0
            ) + 1
        )

    category_items = list(
        notification_types.items()
    )

    category_columns = st.columns(
        min(
            len(category_items),
            4
        )
    )

    for index, (
        notification_type,
        count
    ) in enumerate(category_items):

        with category_columns[
            index % len(category_columns)
        ]:

            icon = get_notification_icon(
                notification_type
            )

            st.markdown(
                f"""
                <div class="category-card">
                  <div style="
                    font-size:25px;
                  ">
                    {icon}
                  </div>
                  <div class="category-number">
                    {count}
                  </div>
                  <div class="category-name">
                    {notification_type}
                  </div>

                </div>
                """,
                unsafe_allow_html=True
            )

else:

    st.info(
        "Notification categories will appear "
        "when notifications are available."
    )

# ==========================================================
# QUICK ACTIONS
# ==========================================================

st.write("")
st.divider()

st.subheader("🚀 Continue Your Journey")

q1, q2, q3 = st.columns(3)

with q1:

    if st.button(
        "🎯 Career Assessment",
        use_container_width=True
    ):

        st.switch_page(
            "pages/school_career.py"
        )

with q2:

    if st.button(
        "📚 Learning Roadmap",
        use_container_width=True
    ):

        st.switch_page(
            "pages/school_roadmap.py"
        )

with q3:

    if st.button(
        "📊 Student Report",
        use_container_width=True
    ):

        st.switch_page(
            "pages/school_reports.py"
        )

# ==========================================================
# REFRESH
# ==========================================================

st.write("")

refresh_col1, refresh_col2 = st.columns(
    [1, 5]
)

with refresh_col1:

    if st.button(
        "🔄 Refresh",
        use_container_width=True
    ):

        st.rerun()

with refresh_col2:

    st.caption(
        "Notifications are loaded dynamically "
        "from your student account."
    )
