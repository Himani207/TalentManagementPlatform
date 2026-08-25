import sqlite3
from pathlib import Path

DB = Path(__file__).parent.parent / "talentsphere.db"


def get_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def save_placement_score(
        email,
        resume,
        coding,
        projects,
        communication,
        internship,
        placement):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO placement_scores(

        email,
        resume_score,
        coding_score,
        project_score,
        communication_score,
        internship_score,
        placement_score

    )

    VALUES(?,?,?,?,?,?,?)

    ON CONFLICT(email)

    DO UPDATE SET

        resume_score=excluded.resume_score,
        coding_score=excluded.coding_score,
        project_score=excluded.project_score,
        communication_score=excluded.communication_score,
        internship_score=excluded.internship_score,
        placement_score=excluded.placement_score,
        updated_at=CURRENT_TIMESTAMP

    """,

    (

        email,
        resume,
        coding,
        projects,
        communication,
        internship,
        placement

    ))

    conn.commit()

    conn.close()


def get_placement(email):

    conn=get_connection()

    cursor=conn.cursor()

    cursor.execute("""

    SELECT *

    FROM placement_scores

    WHERE email=?

    """,(email,))

    row=cursor.fetchone()

    conn.close()

    if row:

        return dict(row)

    return None