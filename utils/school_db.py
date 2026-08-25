import sqlite3
from datetime import datetime
DB_NAME = "talentsphere.db"
# ---------------------------------------
# Database Connection
# ---------------------------------------
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# ---------------------------------------
# Create Student Profile Table
# ---------------------------------------
# ---------------------------------------
# Create Student Profile Table
# ---------------------------------------
def create_student_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_profile (

            email TEXT PRIMARY KEY,

            parent_email TEXT,

            age INTEGER,

            class_name TEXT,

            school_name TEXT,

            interests TEXT,

            favourite_subject TEXT,

            dream_career TEXT,

            short_goal TEXT,

            overall_percentage REAL DEFAULT 0,

            recent_exam_score REAL DEFAULT 0,

            strong_subjects TEXT,

            weak_subjects TEXT,

            academic_achievements TEXT,

            attendance_percentage REAL DEFAULT 0,

            academic_goal TEXT

        )
    """)

    conn.commit()
    conn.close()
#===================================================
# save profile
#====================================================
def save_profile(
    email,
    parent_email,
    age,
    class_name,
    school,
    interests,
    favorite_subject,
    dream_career,
    goals,
    overall_percentage,
    recent_exam_score,
    strong_subjects,
    weak_subjects,
    academic_achievements,
    attendance_percentage,
    academic_goal
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT email
        FROM student_profile
        WHERE email=?
        """,
        (email,)
    )

    existing = cursor.fetchone()

    if existing:

        cursor.execute(
            """
            UPDATE student_profile
            SET
                parent_email=?,
                age=?,
                class_name=?,
                school_name=?,
                interests=?,
                favourite_subject=?,
                dream_career=?,
                short_goal=?,
                overall_percentage=?,
                recent_exam_score=?,
                strong_subjects=?,
                weak_subjects=?,
                academic_achievements=?,
                attendance_percentage=?,
                academic_goal=?
            WHERE email=?
            """,
            (
                parent_email,
                age,
                class_name,
                school,
                interests,
                favorite_subject,
                dream_career,
                goals,
                overall_percentage,
                recent_exam_score,
                strong_subjects,
                weak_subjects,
                academic_achievements,
                attendance_percentage,
                academic_goal,
                email
            )
        )

    else:

        cursor.execute(
            """
            INSERT INTO student_profile (
                email,
                parent_email,
                age,
                class_name,
                school_name,
                interests,
                favourite_subject,
                dream_career,
                short_goal,
                overall_percentage,
                recent_exam_score,
                strong_subjects,
                weak_subjects,
                academic_achievements,
                attendance_percentage,
                academic_goal
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                email,
                parent_email,
                age,
                class_name,
                school,
                interests,
                favorite_subject,
                dream_career,
                goals,
                overall_percentage,
                recent_exam_score,
                strong_subjects,
                weak_subjects,
                academic_achievements,
                attendance_percentage,
                academic_goal
            )
        )

    conn.commit()
    conn.close() 
# ---------------------------------------
# Get Student Profile
# ---------------------------------------
def get_student_profile(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            email,
            parent_email,
            age,
            class_name,
            school_name,
            interests,
            favourite_subject,
            dream_career,
            short_goal,
            overall_percentage,
            recent_exam_score,
            strong_subjects,
            weak_subjects,
            academic_achievements,
            attendance_percentage,
            academic_goal
        FROM student_profile
        WHERE email=?
        """,
        (email,),
    )

    row = cursor.fetchone()

    conn.close()

    if row:

        return {
            "email": row["email"],
            "parent_email": row["parent_email"],
            "age": row["age"],
            "class": row["class_name"],
            "school": row["school_name"],
            "interests": row["interests"] if row["interests"] else "",
            "subject": row["favourite_subject"],
            "career": row["dream_career"],
            "goal": row["short_goal"],
            "overall_percentage": row["overall_percentage"] or 0,
            "recent_exam_score": row["recent_exam_score"] or 0,
            "strong_subjects": row["strong_subjects"] or "",
            "weak_subjects": row["weak_subjects"] or "",
            "academic_achievements": row["academic_achievements"] or "",
            "attendance_percentage": row["attendance_percentage"] or 0,
            "academic_goal": row["academic_goal"] or ""
        }
        

    return None
# ---------------------------------------
# Update Student Profile
# ---------------------------------------

def update_profile(
    email,
    parent_email,
    age,
    class_name,
    school,
    interests,
    favorite_subject,
    dream_career,
    goals,
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE student_profile
        SET
            parent_email=?,
            age=?,
            class_name=?,
            school_name=?,
            interests=?,
            favourite_subject=?,
            dream_career=?,
            short_goal=?
        WHERE email=?
        """,
        (
            parent_email,
            age,
            class_name,
            school,
            interests,
            favorite_subject,
            dream_career,
            goals,
            email,
        ),
    )

    conn.commit()

    updated = cursor.rowcount > 0

    conn.close()

    return updated
# ---------------------------------------
# Calculate Profile Completion
# ---------------------------------------

def calculate_profile_completion(email):

    profile = get_student_profile(email)

    if profile is None:
        return 0

    fields = [
        "parent_email",
        "age",
        "class",
        "school",
        "interests",
        "subject",
        "career",
        "goal",
    ]

    completed = 0

    for field in fields:

        value = profile.get(field)

        if value is None:
            continue

        if isinstance(value, str):

            if value.strip() != "":
                completed += 1

        else:

            if value != 0:
                completed += 1

    completion = int((completed / len(fields)) * 100)

    return completion
# ---------------------------------------
# Get Total Students
# ---------------------------------------

def get_total_students():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM student_profile
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total
# ---------------------------------------
# Get All Students
# ---------------------------------------

def get_all_students():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            email,
            parent_email,
            age,
            class_name,
            school_name,
            interests,
            favourite_subject,
            dream_career,
            short_goal
        FROM student_profile
        ORDER BY class_name ASC, email ASC
    """)

    students = cursor.fetchall()

    conn.close()

    student_list = []

    for student in students:

        student_list.append({

            "email": student["email"],

            "parent_email": student["parent_email"] or "",

            "age": student["age"] or 0,

            "class": student["class_name"] or "",

            "school": student["school_name"] or "",

            "interests": student["interests"] or "",

            "subject": student["favourite_subject"] or "",

            "career": student["dream_career"] or "",

            "goal": student["short_goal"] or ""

        })

    return student_list
# ---------------------------------------
# Create Student Report Table
# ---------------------------------------

def create_report_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_reports (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            email TEXT UNIQUE,

            profile_completion INTEGER DEFAULT 0,

            assessment_score INTEGER DEFAULT 0,

            learning_progress INTEGER DEFAULT 0,

            ai_readiness INTEGER DEFAULT 0,

            career_match INTEGER DEFAULT 0,

            certificates INTEGER DEFAULT 0,

            study_hours INTEGER DEFAULT 0,

            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
# ---------------------------------------
# Save Assessment Score
# ---------------------------------------

def save_assessment_score(email, score):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT email
        FROM student_reports
        WHERE email=?
    """, (email,))

    report = cursor.fetchone()

    if report:

        cursor.execute("""
            UPDATE student_reports
            SET
                assessment_score=?,
                last_updated=CURRENT_TIMESTAMP
            WHERE email=?
        """, (
            score,
            email
        ))

    else:

        cursor.execute("""
            INSERT INTO student_reports(
                email,
                assessment_score
            )
            VALUES(?,?)
        """, (
            email,
            score
        ))

    conn.commit()
    conn.close()

    return True
# ---------------------------------------
# Get Latest Assessment Score
# ---------------------------------------

def get_latest_assessment(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT assessment_score
        FROM student_reports
        WHERE email=?
    """, (email,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row["assessment_score"]

    return 0
# ---------------------------------------
# Create Skill Assessment Result Table
# ---------------------------------------

def create_skill_assessment_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS skill_assessment_results (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            email TEXT NOT NULL,

            skill TEXT NOT NULL,

            score INTEGER DEFAULT 0,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    conn.commit()
    conn.close()


# ---------------------------------------
# Save Skill-Wise Assessment Results
# ---------------------------------------

def save_skill_assessment_results(email, skill_scores):

    conn = get_connection()
    cursor = conn.cursor()

    # Remove previous skill results
    # so the latest assessment becomes active
    cursor.execute("""
        DELETE FROM skill_assessment_results
        WHERE email=?
    """, (email,))

    # Save latest skill scores
    for skill, score in skill_scores.items():

        cursor.execute("""
            INSERT INTO skill_assessment_results(
                email,
                skill,
                score
            )
            VALUES(?,?,?)
        """, (
            email,
            skill,
            int(score)
        ))

    conn.commit()
    conn.close()

    return True


# ---------------------------------------
# Get Skill-Wise Assessment Results
# ---------------------------------------

def get_skill_assessment_results(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            skill,
            score,
            created_at
        FROM skill_assessment_results
        WHERE email=?
        ORDER BY id ASC
    """, (email,))

    rows = cursor.fetchall()

    conn.close()

    skill_scores = {}

    for row in rows:

        skill_scores[row["skill"]] = row["score"]

    return skill_scores
# ---------------------------------------
# Create Learning Progress Table
# ---------------------------------------

def create_learning_progress_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning_progress (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            email TEXT UNIQUE,

            total_topics INTEGER DEFAULT 0,

            completed_topics INTEGER DEFAULT 0,

            progress_percentage INTEGER DEFAULT 0,

            current_level TEXT DEFAULT 'Beginner',

            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    conn.commit()
    conn.close()
# ---------------------------------------
# Update Learning Progress
# ---------------------------------------

def update_learning_progress(email, completed_topics, total_topics):

    if total_topics <= 0:
        total_topics = 1

    progress = int((completed_topics / total_topics) * 100)

    if progress >= 80:
        level = "Advanced"

    elif progress >= 50:
        level = "Intermediate"

    else:
        level = "Beginner"

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT email
        FROM learning_progress
        WHERE email=?
    """, (email,))

    existing = cursor.fetchone()

    if existing:

        cursor.execute("""
            UPDATE learning_progress
            SET
                completed_topics=?,
                total_topics=?,
                progress_percentage=?,
                current_level=?,
                last_updated=CURRENT_TIMESTAMP
            WHERE email=?
        """, (
            completed_topics,
            total_topics,
            progress,
            level,
            email
        ))

    else:

        cursor.execute("""
            INSERT INTO learning_progress(
                email,
                total_topics,
                completed_topics,
                progress_percentage,
                current_level
            )
            VALUES(?,?,?,?,?)
        """, (
            email,
            total_topics,
            completed_topics,
            progress,
            level
        ))

    conn.commit()
    conn.close()

    return progress
# ---------------------------------------
# Get Learning Progress
# ---------------------------------------

def get_learning_progress(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            total_topics,
            completed_topics,
            progress_percentage,
            current_level
        FROM learning_progress
        WHERE email=?
    """, (email,))

    row = cursor.fetchone()

    conn.close()

    if row:

        return {
            "total_topics": row["total_topics"],
            "completed_topics": row["completed_topics"],
            "progress_percentage": row["progress_percentage"],
            "current_level": row["current_level"]
        }

    return {
        "total_topics": 0,
        "completed_topics": 0,
        "progress_percentage": 0,
        "current_level": "Beginner"
    }
# ---------------------------------------
# Create Certificate Table
#-----------------------------------------
def create_certificate_table():

    conn = get_connection()
    cursor = conn.cursor()

    # Create table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_certificates (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            email TEXT NOT NULL,

            certificate_name TEXT NOT NULL,

            provider TEXT,

            issue_date TEXT,

            certificate_file TEXT,

            status TEXT DEFAULT 'Completed',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    # --------------------------------------------------
    # Migration for old database
    # --------------------------------------------------

    cursor.execute("""
        PRAGMA table_info(student_certificates)
    """)

    columns = [
        row["name"]
        for row in cursor.fetchall()
    ]

    # Add certificate_file if old table doesn't have it
    if "certificate_file" not in columns:

        cursor.execute("""
            ALTER TABLE student_certificates
            ADD COLUMN certificate_file TEXT
        """)

    conn.commit()
    conn.close()
# ---------------------------------------
# Get Student Certificates
# ---------------------------------------
def get_certificates(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            certificate_name,
            provider,
            issue_date,
            certificate_file,
            status
        FROM student_certificates
        WHERE email=?
        ORDER BY issue_date DESC
    """, (email,))

    rows = cursor.fetchall()

    conn.close()

    certificates = []

    for row in rows:

        certificates.append({
            "id": row["id"],
            "certificate_name": row["certificate_name"],
            "provider": row["provider"],
            "issue_date": row["issue_date"],
            "certificate_file": row["certificate_file"],
            "status": row["status"]
        })

    return certificates
# ---------------------------------------
# Add Student Certificate
# ---------------------------------------
def add_certificate(
    email,
    certificate_name,
    provider,
    issue_date,
    certificate_file,
    status
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO student_certificates
        (
            email,
            certificate_name,
            provider,
            issue_date,
            certificate_file,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        email,
        certificate_name,
        provider,
        issue_date,
        certificate_file,
        status
    ))

    conn.commit()
    conn.close()
# ---------------------------------------
# Delete Student Certificate
# ---------------------------------------

def delete_certificate(certificate_id, email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM student_certificates
        WHERE id = ?
        AND email = ?
    """, (
        certificate_id,
        email
    ))

    conn.commit()
    conn.close()
# ---------------------------------------
# Calculate AI Readiness
# ---------------------------------------

def calculate_ai_readiness(email):

    # Profile completion
    profile_score = calculate_profile_completion(email)

    # Latest assessment score_assessment()
    assessment_score = get_latest_assessment(email)

    # Learning progress
    learning = get_learning_progress(email)
    learning_score = learning["progress_percentage"]

    # Certificates
    certificates = get_certificates(email)
    certificate_count = len(certificates)

    # Certificate score
    # Maximum contribution = 10 points
    certificate_score = min(certificate_count * 2, 10)

    # Calculate weighted score
    ai_score = (
        (profile_score * 0.20) +
        (assessment_score * 0.40) +
        (learning_score * 0.30) +
        (certificate_score * 0.10)
    )

    # Keep score between 0 and 100
    ai_score = max(0, min(100, int(ai_score)))

    return ai_score
# ---------------------------------------
# Get Career Match
# ---------------------------------------

def get_career_match(email):

    profile = get_student_profile(email)

    if not profile:
        return {
            "career": "Not Available",
            "match": 0
        }

    career = profile.get("career", "")
    interests = profile.get("interests", "")
    subject = profile.get("subject", "")

    if not career:
        return {
            "career": "Not Selected",
            "match": 0
        }

    # Convert interests into a list
    interest_list = [
        item.strip().lower()
        for item in interests.split(",")
        if item.strip()
    ]

    subject = subject.lower()

    # Career-related keywords
    career_keywords = {

        "Software Engineer": [
            "programming",
            "technology",
            "computer science",
            "problem solving"
        ],

        "AI Engineer": [
            "programming",
            "artificial intelligence",
            "mathematics",
            "technology",
            "research"
        ],

        "Data Scientist": [
            "programming",
            "mathematics",
            "research",
            "technology"
        ],

        "Robotics Engineer": [
            "robotics",
            "programming",
            "mathematics",
            "science",
            "technology"
        ],

        "Doctor": [
            "science",
            "biology",
            "research"
        ],

        "Scientist": [
            "science",
            "research",
            "mathematics",
            "technology"
        ],

        "Teacher": [
            "communication",
            "creativity",
            "mathematics",
            "science"
        ],

        "Business Entrepreneur": [
            "business",
            "communication",
            "creativity",
            "leadership"
        ],

        "IAS Officer": [
            "communication",
            "leadership",
            "social science",
            "research"
        ]
    }

    keywords = career_keywords.get(career, [])

    if not keywords:
        return {
            "career": career,
            "match": 50
        }

    matched = 0

    # Match interests
    for keyword in keywords:

        if keyword in interest_list:
            matched += 1

    # Match favorite subject
    for keyword in keywords:

        if keyword in subject:
            matched += 1

    total_possible = len(keywords) + 1

    match = int(
        (matched / total_possible) * 100
    )

    # Keep score between 0 and 100
    match = max(0, min(100, match))

    return {
        "career": career,
        "match": match
    }

# ==========================================================
# NOTIFICATION SYSTEM
# ==========================================================
# ==========================================================
# CREATE NOTIFICATION TABLE
# ==========================================================

def create_notification_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            email TEXT NOT NULL,

            title TEXT NOT NULL,

            message TEXT NOT NULL,

            type TEXT DEFAULT 'General',

            priority TEXT DEFAULT 'Normal',

            is_read INTEGER DEFAULT 0,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
    """)

    conn.commit()
    conn.close()


# ==========================================================
# CREATE OPPORTUNITIES TABLE
# ==========================================================

def create_opportunity_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS school_opportunities (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,

            description TEXT NOT NULL,

            opportunity_type TEXT NOT NULL,

            link TEXT,

            priority TEXT DEFAULT 'Normal',

            target_class TEXT,

            target_interest TEXT,

            deadline TEXT,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
    """)

    conn.commit()
    conn.close()


# ==========================================================
# ADD NOTIFICATION FOR ONE STUDENT
# ==========================================================

def add_notification(
    email,
    title,
    message,
    notification_type="General",
    priority="Normal"
):

    create_notification_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO notifications (
            email,
            title,
            message,
            type,
            priority,
            is_read,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        email,
        title,
        message,
        notification_type,
        priority,
        0,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return True


# ==========================================================
# ADD NOTIFICATION TO ALL STUDENTS
# ==========================================================

def add_notification_to_all_students(
    title,
    message,
    notification_type="General",
    priority="Normal"
):

    create_notification_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT email
        FROM student_profile
    """)

    students = cursor.fetchall()

    created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    for student in students:

        student_email = student["email"]

        cursor.execute("""
            INSERT INTO notifications (
                email,
                title,
                message,
                type,
                priority,
                is_read,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            student_email,
            title,
            message,
            notification_type,
            priority,
            0,
            created_at
        ))

    conn.commit()
    conn.close()

    return True


# ==========================================================
# ADD SCHOOL OPPORTUNITY
# ==========================================================
# This is the important dynamic function.
#
# When an admin adds a scholarship/hackathon:
#
# 1. Opportunity is saved.
# 2. Students are checked.
# 3. Matching students automatically receive notification.
#
# If target_class is empty -> all classes.
# If target_interest is empty -> all interests.
# ==========================================================

def add_school_opportunity(
    title,
    description,
    opportunity_type,
    link="",
    priority="Normal",
    target_class="",
    target_interest="",
    deadline=""
):

    create_opportunity_table()
    create_notification_table()

    conn = get_connection()
    cursor = conn.cursor()

    # ------------------------------------------
    # Save opportunity
    # ------------------------------------------

    cursor.execute("""
        INSERT INTO school_opportunities (
            title,
            description,
            opportunity_type,
            link,
            priority,
            target_class,
            target_interest,
            deadline
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        description,
        opportunity_type,
        link,
        priority,
        target_class,
        target_interest,
        deadline
    ))

    opportunity_id = cursor.lastrowid

    # ------------------------------------------
    # Get students
    # ------------------------------------------

    cursor.execute("""
        SELECT
            email,
            class_name,
            interests
        FROM student_profile
    """)

    students = cursor.fetchall()

    created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # ------------------------------------------
    # Create notification for matching students
    # ------------------------------------------

    for student in students:

        student_email = student["email"]

        student_class = (
            student["class_name"] or ""
        ).strip().lower()

        student_interests = (
            student["interests"] or ""
        ).lower()

        # --------------------------------------
        # Class matching
        # --------------------------------------

        class_match = True

        if target_class.strip():

            class_match = (
                student_class
                == target_class.strip().lower()
            )

        # --------------------------------------
        # Interest matching
        # --------------------------------------

        interest_match = True

        if target_interest.strip():

            interest_match = (
                target_interest.strip().lower()
                in student_interests
            )

        # --------------------------------------
        # Only notify matching students
        # --------------------------------------

        if class_match and interest_match:

            notification_title = (
                f"🎯 {opportunity_type}: {title}"
            )

            notification_message = description

            if deadline:

                notification_message += (
                    f"\n\n📅 Deadline: {deadline}"
                )

            if link:

                notification_message += (
                    f"\n\n🔗 Open Opportunity: {link}"
                )

            cursor.execute("""
                INSERT INTO notifications (
                    email,
                    title,
                    message,
                    type,
                    priority,
                    is_read,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                student_email,
                notification_title,
                notification_message,
                opportunity_type,
                priority,
                0,
                created_at
            ))

    conn.commit()
    conn.close()

    return opportunity_id


# ==========================================================
# GET ALL OPPORTUNITIES
# ==========================================================

def get_school_opportunities():

    create_opportunity_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            description,
            opportunity_type,
            link,
            priority,
            target_class,
            target_interest,
            deadline,
            created_at
        FROM school_opportunities
        ORDER BY datetime(created_at) DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    opportunities = []

    for row in rows:

        opportunities.append({

            "id": row["id"],

            "title": row["title"],

            "description": row["description"],

            "type": row["opportunity_type"],

            "link": row["link"] or "",

            "priority": row["priority"] or "Normal",

            "target_class": row["target_class"] or "",

            "target_interest": row["target_interest"] or "",

            "deadline": row["deadline"] or "",

            "created_at": row["created_at"]

        })

    return opportunities


# ==========================================================
# GET STUDENT NOTIFICATIONS
# ==========================================================

def get_notifications(email):

    create_notification_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            email,
            title,
            message,
            type,
            priority,
            is_read,
            created_at
        FROM notifications
        WHERE email = ?
        ORDER BY datetime(created_at) DESC
    """, (email,))

    rows = cursor.fetchall()

    conn.close()

    notifications = []

    for row in rows:

        notifications.append({

            "id": row["id"],

            "email": row["email"],

            "title": row["title"],

            "message": row["message"],

            "type": row["type"],

            "priority": row["priority"],

            "is_read": row["is_read"],

            "created_at": row["created_at"]

        })

    return notifications
# ==========================================================
# GENERATE DYNAMIC STUDENT NOTIFICATIONS
# ==========================================================

def generate_student_notifications(email):

    create_notification_table()

    profile = get_student_profile(email)

    if not profile:
        return

    conn = get_connection()
    cursor = conn.cursor()

    # ------------------------------------------------------
    # Helper: Check whether notification already exists
    # ------------------------------------------------------

    def notification_exists(title, message):

        cursor.execute(
            """
            SELECT id
            FROM notifications
            WHERE email=?
            AND title=?
            AND message=?
            LIMIT 1
            """,
            (
                email,
                title,
                message
            )
        )

        return cursor.fetchone() is not None

    # ------------------------------------------------------
    # Helper: Create notification only once
    # ------------------------------------------------------

    def create_if_not_exists(
        title,
        message,
        notification_type="General",
        priority="Normal"
    ):

        if not notification_exists(
            title,
            message
        ):

            cursor.execute(
                """
                INSERT INTO notifications (
                    email,
                    title,
                    message,
                    type,
                    priority,
                    is_read,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    email,
                    title,
                    message,
                    notification_type,
                    priority,
                    0,
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                )
            )

    # ======================================================
    # 1. PROFILE NOTIFICATION
    # ======================================================

    completion = calculate_profile_completion(email)

    if completion < 100:

        title = "Complete Your Student Profile"

        message = (
            f"Your profile is {completion}% complete. "
            "Complete your profile to receive better "
            "career recommendations and learning suggestions."
        )

        create_if_not_exists(
            title,
            message,
            "Academic",
            "Normal"
        )

    else:

        title = "Profile Completed 🎉"

        message = (
            "Your student profile is 100% complete. "
            "You are ready for personalized career and "
            "learning recommendations."
        )

        create_if_not_exists(
            title,
            message,
            "Achievement",
            "Normal"
        )

    # ======================================================
    # 2. LOW ATTENDANCE NOTIFICATION
    # ======================================================

    attendance = float(
        profile.get(
            "attendance_percentage",
            0
        ) or 0
    )

    if attendance > 0 and attendance < 75:

        title = "Low Attendance Alert"

        message = (
            f"Your current attendance is {attendance}%. "
            "Try to improve your attendance to stay on "
            "track academically."
        )

        create_if_not_exists(
            title,
            message,
            "Academic",
            "High"
        )

    elif attendance >= 75:

        title = "Good Attendance 👍"

        message = (
            f"Your attendance is {attendance}%. "
            "Keep maintaining your regular attendance."
        )

        create_if_not_exists(
            title,
            message,
            "Academic",
            "Normal"
        )

    # ======================================================
    # 3. EXAM SCORE NOTIFICATION
    # ======================================================

    exam_score = float(
        profile.get(
            "recent_exam_score",
            0
        ) or 0
    )

    if exam_score > 0:

        if exam_score >= 90:

            title = "Excellent Exam Performance 🏆"

            message = (
                f"You scored {exam_score}% in your recent exam. "
                "Excellent work! Keep maintaining this performance."
            )

            create_if_not_exists(
                title,
                message,
                "Achievement",
                "Normal"
            )

        elif exam_score < 50:

            title = "Improve Your Exam Performance"

            message = (
                f"Your recent exam score is {exam_score}%. "
                "Consider focusing more on your weak subjects "
                "and following your learning roadmap."
            )

            create_if_not_exists(
                title,
                message,
                "Assessment",
                "High"
            )

    # ======================================================
    # 4. WEAK SUBJECT NOTIFICATION
    # ======================================================

    weak_subjects = str(
        profile.get(
            "weak_subjects",
            ""
        ) or ""
    ).strip()

    if weak_subjects:

        title = "Focus on Your Weak Subjects"

        message = (
            f"You identified {weak_subjects} as subjects "
            "needing improvement. Practice these subjects "
            "regularly to improve your academic performance."
        )

        create_if_not_exists(
            title,
            message,
            "Academic",
            "Normal"
        )

    # ======================================================
    # 5. STRONG SUBJECT / ACHIEVEMENT
    # ======================================================

    strong_subjects = str(
        profile.get(
            "strong_subjects",
            ""
        ) or ""
    ).strip()

    if strong_subjects:

        title = "Your Strong Subjects 💪"

        message = (
            f"You are strong in {strong_subjects}. "
            "Consider exploring career paths related "
            "to these subjects."
        )

        create_if_not_exists(
            title,
            message,
            "Career",
            "Normal"
        )

    # ======================================================
    # 6. CAREER NOTIFICATION
    # ======================================================

    career = str(
        profile.get(
            "career",
            ""
        ) or ""
    ).strip()

    if career:

        title = "Career Goal Saved 🎯"

        message = (
            f"Your dream career is {career}. "
            "Explore the Career Assessment and Learning "
            "Roadmap to prepare for this career."
        )

        create_if_not_exists(
            title,
            message,
            "Career",
            "Normal"
        )

    # ======================================================
    # 7. ACADEMIC GOAL NOTIFICATION
    # ======================================================

    academic_goal = str(
        profile.get(
            "academic_goal",
            ""
        ) or ""
    ).strip()

    if academic_goal:

        title = "Academic Goal Reminder 📚"

        message = (
            f"Your academic goal is: {academic_goal}. "
            "Stay consistent with your studies to achieve it."
        )

        create_if_not_exists(
            title,
            message,
            "Academic",
            "Normal"
        )

    # ======================================================
    # 8. CAREER MATCH
    # ======================================================

    career_match = get_career_match(email)

    match_score = career_match.get(
        "match",
        0
    )

    matched_career = career_match.get(
        "career",
        ""
    )

    if matched_career and match_score >= 70:

        title = "Strong Career Match 🎯"

        message = (
            f"Your profile currently has a {match_score}% "
            f"match with {matched_career}. "
            "Explore the career assessment for more details."
        )

        create_if_not_exists(
            title,
            message,
            "Career",
            "High"
        )

    # ======================================================
    # SAVE ALL GENERATED NOTIFICATIONS
    # ======================================================

    conn.commit()
    conn.close()


# ==========================================================
# GET UNREAD NOTIFICATION COUNT
# ==========================================================

def get_unread_notification_count(email):

    create_notification_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM notifications
        WHERE email=?
        AND is_read=0
    """, (email,))

    count = cursor.fetchone()[0]

    conn.close()

    return count


# ==========================================================
# MARK NOTIFICATION AS READ
# ==========================================================

def mark_notification_read(notification_id):

    create_notification_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE notifications
        SET is_read=1
        WHERE id=?
    """, (notification_id,))

    conn.commit()
    conn.close()

    return True


# ==========================================================
# MARK ALL NOTIFICATIONS AS READ
# ==========================================================

def mark_all_notifications_read(email):

    create_notification_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE notifications
        SET is_read=1
        WHERE email=?
    """, (email,))

    conn.commit()
    conn.close()

    return True


# ==========================================================
# DELETE NOTIFICATION
# ==========================================================

def delete_notification(notification_id):

    create_notification_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM notifications
        WHERE id=?
    """, (notification_id,))

    conn.commit()
    conn.close()

    return True


# ==========================================================
# DELETE ALL NOTIFICATIONS FOR STUDENT
# ==========================================================

def delete_student_notifications(email):

    create_notification_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM notifications
        WHERE email=?
    """, (email,))

    conn.commit()
    conn.close()

    return True



def create_notification_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            type TEXT DEFAULT 'General',
            priority TEXT DEFAULT 'Normal',
            is_read INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()
    conn.close()


# ==========================================================
# ADD NOTIFICATION
# ==========================================================

def add_notification(
    email,
    title,
    message,
    notification_type="General",
    priority="Normal"
):

    create_notification_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO notifications (
            email,
            title,
            message,
            type,
            priority,
            is_read,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            email,
            title,
            message,
            notification_type,
            priority,
            0,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    conn.commit()
    conn.close()


# ==========================================================
# ADD NOTIFICATION TO ALL STUDENTS
# ==========================================================

def add_notification_to_all_students(
    title,
    message,
    notification_type="General",
    priority="Normal"
):

    create_notification_table()

    conn = get_connection()
    cursor = conn.cursor()

    # Get all registered students
    cursor.execute(
        """
        SELECT email
        FROM student_profile
        """
    )

    students = cursor.fetchall()

    created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    for student in students:

        student_email = student[0]

        cursor.execute(
            """
            INSERT INTO notifications (
                email,
                title,
                message,
                type,
                priority,
                is_read,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                student_email,
                title,
                message,
                notification_type,
                priority,
                0,
                created_at
            )
        )

    conn.commit()
    conn.close()


# ==========================================================
# GET STUDENT NOTIFICATIONS
# ==========================================================

def get_notifications(email):

    create_notification_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            email,
            title,
            message,
            type,
            priority,
            is_read,
            created_at
        FROM notifications
        WHERE email = ?
        ORDER BY datetime(created_at) DESC
        """,
        (email,)
    )

    rows = cursor.fetchall()

    conn.close()

    notifications = []

    for row in rows:

        notifications.append(
            {
                "id": row[0],
                "email": row[1],
                "title": row[2],
                "message": row[3],
                "type": row[4],
                "priority": row[5],
                "is_read": row[6],
                "created_at": row[7]
            }
        )

    return notifications


# ==========================================================
# MARK NOTIFICATION AS READ
# ==========================================================

def mark_notification_read(notification_id):

    create_notification_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE notifications
        SET is_read = 1
        WHERE id = ?
        """,
        (notification_id,)
    )

    conn.commit()
    conn.close()


# ==========================================================
# MARK ALL NOTIFICATIONS AS READ
# ==========================================================

def mark_all_notifications_read(email):

    create_notification_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE notifications
        SET is_read = 1
        WHERE email = ?
        """,
        (email,)
    )

    conn.commit()
    conn.close()


# ==========================================================
# DELETE NOTIFICATION
# ==========================================================

def delete_notification(notification_id):

    create_notification_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM notifications
        WHERE id = ?
        """,
        (notification_id,)
    )

    conn.commit()
    conn.close()


# ==========================================================
# DELETE ALL NOTIFICATIONS FOR STUDENT
# ==========================================================

def delete_student_notifications(email):

    create_notification_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM notifications
        WHERE email = ?
        """,
        (email,)
    )

    conn.commit()
    conn.close()


# ---------------------------------------
# Get Complete Student Report
# ---------------------------------------

def get_student_report(email):

    # Student Profile
    profile = get_student_profile(email)

    if not profile:
        return None

    # Profile Completion
    profile_completion = calculate_profile_completion(email)

    # Latest Assessment
    assessment = get_latest_assessment(email)

    # Learning Progress
    learning = get_learning_progress(email)

    # Certificates
    certificates = get_certificates(email)

    # Notifications
    notifications = get_notifications(email)

    # AI Readiness
    ai_readiness = calculate_ai_readiness(email)

    # Career Match
    career = get_career_match(email)

    # Build complete report
    report = {

        # -------------------------
        # Student Information
        # -------------------------

        "student": {
            "email": profile.get("email"),
            "parent_email": profile.get("parent_email"),
            "age": profile.get("age"),
            "class": profile.get("class"),
            "school": profile.get("school"),
            "interests": profile.get("interests"),
            "favorite_subject": profile.get("subject"),
            "dream_career": profile.get("career"),
            "goal": profile.get("goal")
        },

        # -------------------------
        # Profile
        # -------------------------

        "profile_completion": profile_completion,

        # -------------------------
        # Assessment
        # -------------------------

        "assessment": assessment,

        # -------------------------
        # Learning
        # -------------------------

        "learning": learning,

        # -------------------------
        # Certificates
        # -------------------------

        "certificates": certificates,

        "certificate_count": len(certificates),

        # -------------------------
        # AI Readiness
        # -------------------------

        "ai_readiness": ai_readiness,

        # -------------------------
        # Career
        # -------------------------

        "career_match": career,

        # -------------------------
        # Notifications
        # -------------------------

        "notifications": notifications,

        "notification_count": len(notifications),

        "unread_notifications": sum(
            1
            for notification in notifications
            if not notification["is_read"]
        )
    }

    return report