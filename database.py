import sqlite3

DB_NAME = "talentsphere.db"


# =====================================================
# Database Connection
# =====================================================

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# =====================================================
# Create All Tables
# =====================================================

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # =====================================================
    # USERS TABLE
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        role TEXT NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # =====================================================
    # STUDENT PROFILE TABLE
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_profile(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        parent_email TEXT,
        full_name TEXT,
        phone TEXT,

        dob TEXT,

        age INTEGER,

        gender TEXT,

        city TEXT,

        state TEXT,

        country TEXT,

        profile_photo TEXT,

        school_name TEXT,

        class_name TEXT,

        board TEXT,

        medium TEXT,

        college_name TEXT,

        university TEXT,

        course TEXT,

        branch TEXT,

        semester TEXT,

        cgpa REAL,

        graduation_year TEXT,

        company_name TEXT,

        job_role TEXT,

        experience TEXT,

        current_salary TEXT,

        industry TEXT,

        dream_career TEXT,

        dream_company TEXT,

        short_goal TEXT,

        long_goal TEXT,

        preferred_location TEXT,

        technical_skills TEXT,

        interests TEXT,

        communication INTEGER,

        leadership INTEGER,

        problem_solving INTEGER,

        creativity INTEGER,

        teamwork INTEGER,

        time_management INTEGER,

        critical_thinking INTEGER,

        public_speaking INTEGER,

        learning_style TEXT,

        study_hours TEXT,

        preferred_language TEXT,

        certifications TEXT,

        internships TEXT,

        projects TEXT,

        hackathons TEXT,

        awards TEXT,

        research_papers TEXT,

        resume_path TEXT,

        interested_career TEXT,

        favourite_subject TEXT,

        strongest_skill TEXT,

        improve_skill TEXT,

        placement_preparation TEXT,

        higher_studies TEXT,

        government_job TEXT,

        ai_recommendation TEXT

    )
    """)

    # =====================================================
    # DASHBOARD METRICS
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dashboard_metrics(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        email TEXT UNIQUE,

        career_readiness INTEGER DEFAULT 0,

        skill_score INTEGER DEFAULT 0,

        resume_score INTEGER DEFAULT 0,

        learning_progress INTEGER DEFAULT 0,

        placement_readiness INTEGER DEFAULT 0,

        ai_career_match INTEGER DEFAULT 0,

        skill_gap_analysis TEXT,

        learning_roadmap TEXT

    )
    """)

    # =====================================================
    # CHAT HISTORY
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        email TEXT,

        question TEXT,

        answer TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()


# =====================================================
# Initialize Database
# =====================================================
def initialize_database():
    create_tables()

    from utils.placement_db import create_placement_table
    create_placement_table()

    from utils.coding_db import (
        create_coding_tables,
        create_saved_code_table,
        insert_questions
    )

    create_coding_tables()
    create_saved_code_table()
    insert_questions()


if __name__ == "__main__":
    initialize_database()
    print("✅ TalentSphere Database Created Successfully")
    # =====================================================
# REGISTER USER
# =====================================================

def register_user(full_name, email, password, role):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO users(full_name, email, password, role)
        VALUES (?, ?, ?, ?)
        """, (full_name, email, password, role))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


# =====================================================
# LOGIN USER
# =====================================================

def login_user(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM users
    WHERE email=? AND password=?
    """, (email, password))

    user = cursor.fetchone()

    conn.close()

    return user


# =====================================================
# SAVE STUDENT PROFILE
# =====================================================

def save_profile(data):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    INSERT OR REPLACE INTO student_profile(

        email,
        parent_email,
        full_name,
        phone,
        dob,
        age,
        gender,
        city,
        state,
        country,
        profile_photo,

        school_name,
        class_name,
        board,
        medium,

        college_name,
        university,
        course,
        branch,
        semester,
        cgpa,
        graduation_year,

        company_name,
        job_role,
        experience,
        current_salary,
        industry,

        dream_career,
        dream_company,
        short_goal,
        long_goal,
        preferred_location,

        technical_skills,
        interests,

        communication,
        leadership,
        problem_solving,
        creativity,
        teamwork,
        time_management,
        critical_thinking,
        public_speaking,

        learning_style,
        study_hours,
        preferred_language,

        certifications,
        internships,
        projects,
        hackathons,
        awards,
        research_papers,

        resume_path,

        interested_career,
        favourite_subject,
        strongest_skill,
        improve_skill,
        placement_preparation,
        higher_studies,
        government_job,
        ai_recommendation

    )

    VALUES(

        ?,?,?,?,?,?,?,?,?,?,
        ?,?,?,?,
        ?,?,?,?,?,?,?,
        ?,?,?,?,?,
        ?,?,?,?,?,
        ?,?,
        ?,?,?,?,?,?,?,?,
        ?,?,?,
        ?,?,?,?,?,?,
        ?,
        ?,?,?,?,?,?,?,?

    )

    """, (

        data["email"],
        data["parent_email"],
        data["full_name"],
        data["phone"],
        data["dob"],
        data["age"],
        data["gender"],
        data["city"],
        data["state"],
        data["country"],
        data["profile_photo"],

        data["school_name"],
        data["class_name"],
        data["board"],
        data["medium"],

        data["college_name"],
        data["university"],
        data["course"],
        data["branch"],
        data["semester"],
        data["cgpa"],
        data["graduation_year"],

        data["company_name"],
        data["job_role"],
        data["experience"],
        data["current_salary"],
        data["industry"],

        data["dream_career"],
        data["dream_company"],
        data["short_goal"],
        data["long_goal"],
        data["preferred_location"],

        data["technical_skills"],
        data["interests"],

        data["communication"],
        data["leadership"],
        data["problem_solving"],
        data["creativity"],
        data["teamwork"],
        data["time_management"],
        data["critical_thinking"],
        data["public_speaking"],

        data["learning_style"],
        data["study_hours"],
        data["preferred_language"],

        data["certifications"],
        data["internships"],
        data["projects"],
        data["hackathons"],
        data["awards"],
        data["research_papers"],

        data["resume_path"],

        data["interested_career"],
        data["favourite_subject"],
        data["strongest_skill"],
        data["improve_skill"],
        data["placement_preparation"],
        data["higher_studies"],
        data["government_job"],
        data["ai_recommendation"]

    ))

    conn.commit()
    conn.close()


# =====================================================
# GET PROFILE
# =====================================================

def get_profile(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    SELECT *
    FROM student_profile
    WHERE email=?

    """, (email,))

    profile = cursor.fetchone()

    conn.close()

    return profile


# =====================================================
# UPDATE PROFILE
# =====================================================

def update_profile(data):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    UPDATE student_profile

    SET          
        parent_email=?,
        full_name=?,
        phone=?,
        dob=?,
        age=?,
        gender=?,
        city=?,
        state=?,
        country=?,
        profile_photo=?,

        school_name=?,
        class_name=?,
        board=?,
        medium=?,

        college_name=?,
        university=?,
        course=?,
        branch=?,
        semester=?,
        cgpa=?,
        graduation_year=?,

        company_name=?,
        job_role=?,
        experience=?,
        current_salary=?,
        industry=?,

        dream_career=?,
        dream_company=?,
        short_goal=?,
        long_goal=?,
        preferred_location=?,

        technical_skills=?,
        interests=?,

        communication=?,
        leadership=?,
        problem_solving=?,
        creativity=?,
        teamwork=?,
        time_management=?,
        critical_thinking=?,
        public_speaking=?,

        learning_style=?,
        study_hours=?,
        preferred_language=?,

        certifications=?,
        internships=?,
        projects=?,
        hackathons=?,
        awards=?,
        research_papers=?,

        resume_path=?,

        interested_career=?,
        favourite_subject=?,
        strongest_skill=?,
        improve_skill=?,
        placement_preparation=?,
        higher_studies=?,
        government_job=?,
        ai_recommendation=?

    WHERE email=?

    """, (
        data["parent_email"],
        data["full_name"],
        data["phone"],
        data["dob"],
        data["age"],
        data["gender"],
        data["city"],
        data["state"],
        data["country"],
        data["profile_photo"],

        data["school_name"],
        data["class_name"],
        data["board"],
        data["medium"],

        data["college_name"],
        data["university"],
        data["course"],
        data["branch"],
        data["semester"],
        data["cgpa"],
        data["graduation_year"],

        data["company_name"],
        data["job_role"],
        data["experience"],
        data["current_salary"],
        data["industry"],

        data["dream_career"],
        data["dream_company"],
        data["short_goal"],
        data["long_goal"],
        data["preferred_location"],

        data["technical_skills"],
        data["interests"],

        data["communication"],
        data["leadership"],
        data["problem_solving"],
        data["creativity"],
        data["teamwork"],
        data["time_management"],
        data["critical_thinking"],
        data["public_speaking"],

        data["learning_style"],
        data["study_hours"],
        data["preferred_language"],

        data["certifications"],
        data["internships"],
        data["projects"],
        data["hackathons"],
        data["awards"],
        data["research_papers"],

        data["resume_path"],

        data["interested_career"],
        data["favourite_subject"],
        data["strongest_skill"],
        data["improve_skill"],
        data["placement_preparation"],
        data["higher_studies"],
        data["government_job"],
        data["ai_recommendation"],

        data["email"]

    ))

    conn.commit()
    conn.close()
    # =====================================================
# SAVE DASHBOARD METRICS
# =====================================================

def save_dashboard_metrics(
    email,
    career_readiness,
    skill_score,
    resume_score,
    learning_progress,
    placement_readiness,
    ai_career_match,
    skill_gap_analysis,
    learning_roadmap
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    INSERT OR REPLACE INTO dashboard_metrics(

        email,
        career_readiness,
        skill_score,
        resume_score,
        learning_progress,
        placement_readiness,
        ai_career_match,
        skill_gap_analysis,
        learning_roadmap

    )

    VALUES(?,?,?,?,?,?,?,?,?)

    """, (

        email,
        career_readiness,
        skill_score,
        resume_score,
        learning_progress,
        placement_readiness,
        ai_career_match,
        skill_gap_analysis,
        learning_roadmap

    ))

    conn.commit()
    conn.close()


# =====================================================
# GET DASHBOARD METRICS
# =====================================================

def get_dashboard(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM dashboard_metrics

    WHERE email=?

    """, (email,))

    data = cursor.fetchone()

    conn.close()

    return data


# =====================================================
# SAVE CHAT HISTORY
# =====================================================

def save_chat(email, question, answer):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO chat_history(

        email,
        question,
        answer

    )

    VALUES(?,?,?)

    """, (

        email,
        question,
        answer

    ))

    conn.commit()
    conn.close()


# =====================================================
# GET CHAT HISTORY
# =====================================================

def get_chat_history(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM chat_history

    WHERE email=?

    ORDER BY id DESC

    """, (email,))

    chats = cursor.fetchall()

    conn.close()

    return chats


# =====================================================
# DELETE CHAT HISTORY
# =====================================================

def delete_chat_history(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    DELETE FROM chat_history

    WHERE email=?

    """, (email,))

    conn.commit()
    conn.close()


# =====================================================
# DELETE PROFILE
# =====================================================

def delete_profile(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    DELETE FROM student_profile

    WHERE email=?

    """, (email,))

    conn.commit()
    conn.close()


# =====================================================
# DELETE USER
# =====================================================

def delete_user(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    DELETE FROM users

    WHERE email=?

    """, (email,))

    conn.commit()
    conn.close()


# =====================================================
# DELETE DASHBOARD
# =====================================================

def delete_dashboard(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    DELETE FROM dashboard_metrics

    WHERE email=?

    """, (email,))

    conn.commit()
    conn.close()


# =====================================================
# COMPLETE ACCOUNT DELETE
# =====================================================

def delete_account(email):

    delete_chat_history(email)
    delete_dashboard(email)
    delete_profile(email)
    delete_user(email)