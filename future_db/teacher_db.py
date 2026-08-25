import sqlite3
from pathlib import Path

DB = Path(__file__).parent.parent / "talentsphere.db"


def get_connection():
    return sqlite3.connect(DB)


# -----------------------------------
# CREATE TABLES
# -----------------------------------

def create_teacher_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teacher_feedback (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_email TEXT,
        teacher_name TEXT,
        feedback TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assignments (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        due_date TEXT

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assessments (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_email TEXT,
        quiz TEXT,
        score INTEGER

    )
    """)

    conn.commit()
    conn.close()

# -----------------------------------
# ADD TEACHER FEEDBACK
# -----------------------------------
def add_feedback(email, teacher, feedback):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO teacher_feedback
        (student_email, teacher_name, feedback)
        VALUES (?, ?, ?)
        """,
        (email, teacher, feedback)
    )

    conn.commit()
    conn.close()


# -----------------------------------
# ADD ASSIGNMENT
# -----------------------------------

def add_assignment(title, description, due):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO assignments
        (title, description, due_date)
        VALUES (?, ?, ?)
        """,
        (title, description, due)
    )

    conn.commit()
    conn.close()


# -----------------------------------
# GET ASSESSMENTS
# -----------------------------------

def get_assessments():

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            quiz,
            AVG(score) AS score
        FROM assessments
        GROUP BY quiz
    """)

    data = cursor.fetchall()

    conn.close()

    return [dict(row) for row in data]
# -----------------------------------
# GET ALL ASSIGNMENTS
# -----------------------------------

def get_assignments():

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            description,
            due_date
        FROM assignments
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return [dict(row) for row in data]
# -----------------------------------
# GET STUDENT FEEDBACK
# -----------------------------------

def get_feedback(student_email):

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            teacher_name,
            feedback,
            created_at
        FROM teacher_feedback
        WHERE student_email=?
        ORDER BY id DESC
    """, (student_email,))

    data = cursor.fetchall()

    conn.close()

    return [dict(row) for row in data]
# -----------------------------------
# SAVE ASSESSMENT SCORE
# -----------------------------------

def add_assessment(student_email, quiz, score):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO assessments
        (
            student_email,
            quiz,
            score
        )
        VALUES (?, ?, ?)
    """, (
        student_email,
        quiz,
        score
    ))

    conn.commit()
    conn.close()
    # -----------------------------------
# GET ALL TEACHERS
# -----------------------------------

def get_all_teachers():

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            full_name,
            email,
            role
        FROM users
        WHERE role='Teacher'
        ORDER BY full_name
    """)

    data = cursor.fetchall()

    conn.close()

    return [dict(row) for row in data]
# Create tables when module loads
create_teacher_tables()