import sqlite3

DB_NAME = "talentsphere.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mock_interview_scores(

        email TEXT PRIMARY KEY,

        score INTEGER DEFAULT 0,

        feedback TEXT,

        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()


create_table()


def save_mock_interview_score(email, score, feedback):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO mock_interview_scores
    (
        email,
        score,
        feedback
    )
    VALUES(?,?,?)
    """,
    (
        email,
        score,
        feedback
    ))

    conn.commit()
    conn.close()


def get_mock_interview_score(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT score
    FROM mock_interview_scores
    WHERE email=?
    """, (email,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row["score"]

    return 0


def get_mock_feedback(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT feedback
    FROM mock_interview_scores
    WHERE email=?
    """, (email,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row["feedback"]

    return ""