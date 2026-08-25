import sqlite3
from pathlib import Path


DB = Path(__file__).parent.parent / "talentsphere.db"


def get_connection():

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    return conn



# ---------------------------------
# Create Resume Table
# ---------------------------------

def create_resume_table():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resume_scores(

        email TEXT PRIMARY KEY,

        ats_score INTEGER DEFAULT 0,

        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


    conn.commit()

    conn.close()



# Run automatically
create_resume_table()



# ---------------------------------
# Save Resume Score
# ---------------------------------

def save_resume_score(email, score):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
    INSERT INTO resume_scores
    (
        email,
        ats_score
    )

    VALUES(?,?)

    ON CONFLICT(email)

    DO UPDATE SET

        ats_score=excluded.ats_score,

        updated_at=CURRENT_TIMESTAMP

    """,
    (
        email,
        score
    ))


    conn.commit()

    conn.close()



# ---------------------------------
# Get Resume Score
# ---------------------------------

def get_resume_score(email):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
    SELECT ats_score

    FROM resume_scores

    WHERE email=?

    """,
    (email,))


    row = cursor.fetchone()


    conn.close()


    if row:

        return row["ats_score"]


    return 0