import sqlite3

DB_NAME = "talentsphere.db"


def get_connection():

    conn = sqlite3.connect(DB_NAME)

    conn.row_factory = sqlite3.Row

    create_college_table(conn)

    return conn



# ---------------------------------------
# Create College Profile Table
# ---------------------------------------

def create_college_table(conn):

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS college_profile(

        email TEXT PRIMARY KEY,
        full_name TEXT,
        college TEXT,
        degree TEXT,
        department TEXT,
        year TEXT,
        phone TEXT,
        location TEXT,
        skills TEXT,
        about TEXT,
        cgpa TEXT,
        projects TEXT,
        certifications TEXT,
        career_goals TEXT,
        ai_insights TEXT,
        resume_score INTEGER DEFAULT 0,
        career_match INTEGER DEFAULT 0,
        placement_readiness INTEGER DEFAULT 0

    )
    """)

    conn.commit()
# ---------------------------------------
# Save Profile
# ---------------------------------------

def save_profile(
    email,
    full_name,
    college,
    degree,
    department,
    year,
    phone,
    location,
    skills,
    about,
    cgpa,
    projects,
    certifications,
    career_goals,
    ai_insights
):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
    INSERT OR REPLACE INTO college_profile
    (
        email,
        full_name,
        college,
        degree,
        department,
        year,
        phone,
        location,
        skills,
        about,
        cgpa,
        projects,
        certifications,
        career_goals,
        ai_insights
    )

    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)

    """,
    (
        email,
        full_name,
        college,
        degree,
        department,
        year,
        phone,
        location,
        skills,
        about,
        cgpa,
        projects,
        certifications,
        career_goals,
        ai_insights
    ))


    conn.commit()

    conn.close()



# ---------------------------------------
# Get Profile
# ---------------------------------------

def get_profile(email):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM college_profile
        WHERE LOWER(email)=LOWER(?)
        """,
        (email,)
    )


    profile = cursor.fetchone()


    conn.close()

    return profile
# ==========================================================
# PROJECT SCORE
# ==========================================================

def get_project_score(email):

    profile = get_profile(email)

    if not profile:
        return 0

    projects = profile["projects"]

    if not projects:
        return 0

    project_list = [p.strip() for p in projects.split(",") if p.strip()]

    score = len(project_list) * 20

    return min(score, 100)
# ==========================================================
# GET ALL COLLEGE STUDENTS (ADMIN)
# ==========================================================

def get_all_college_students():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM college_profile
        """
    )

    students = cursor.fetchall()

    conn.close()

    return [dict(student) for student in students]