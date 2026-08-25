from database import get_connection


# ==========================================================
# CREATE TABLE
# ==========================================================

def create_interview_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interview_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        email TEXT,

        interview_type TEXT,

        difficulty TEXT,

        score INTEGER,

        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()


# ==========================================================
# SAVE INTERVIEW
# ==========================================================

def save_interview(

    email,
    interview_type,
    difficulty,
    score

):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO interview_history(

        email,
        interview_type,
        difficulty,
        score

    )

    VALUES(?,?,?,?)

    """,

    (

        email,
        interview_type,
        difficulty,
        score

    )

    )

    conn.commit()
    conn.close()


# ==========================================================
# GET HISTORY
# ==========================================================

def get_history(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    SELECT

    interview_type,
    difficulty,
    score,
    date

    FROM interview_history

    WHERE email=?

    ORDER BY id DESC

    """,(email,))

    data = cursor.fetchall()

    conn.close()

    return data
