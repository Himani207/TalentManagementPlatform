import sqlite3
from pathlib import Path

# Database path
DB = Path(__file__).resolve().parent.parent / "talentsphere.db"


# -------------------------
# Database Connection
# -------------------------
def get_connection():
    conn = sqlite3.connect(str(DB), timeout=30)
    conn.row_factory = sqlite3.Row
    return conn


# -------------------------
# Create Placement Table
# -------------------------
def create_placement_table():
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS placement_scores (
                email TEXT UNIQUE NOT NULL,
                resume_score REAL DEFAULT 0,
                coding_score REAL DEFAULT 0,
                project_score REAL DEFAULT 0,
                communication_score REAL DEFAULT 0,
                internship_score REAL DEFAULT 0,
                placement_score REAL DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()

    finally:
        conn.close()


# -------------------------
# Save or Update Placement Score
# -------------------------
def save_placement_score(
    email,
    resume,
    coding,
    projects,
    communication,
    internship,
    placement
):
    create_placement_table()

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO placement_scores (
                email,
                resume_score,
                coding_score,
                project_score,
                communication_score,
                internship_score,
                placement_score
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)

            ON CONFLICT(email)
            DO UPDATE SET
                resume_score = excluded.resume_score,
                coding_score = excluded.coding_score,
                project_score = excluded.project_score,
                communication_score = excluded.communication_score,
                internship_score = excluded.internship_score,
                placement_score = excluded.placement_score,
                updated_at = CURRENT_TIMESTAMP
        """, (
            email,
            resume,
            coding,
            projects,
            communication,
            internship,
            placement
        ))

        conn.commit()

    finally:
        conn.close()


# -------------------------
# Get Placement Score
# -------------------------
def get_placement(email):
    create_placement_table()

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM placement_scores
            WHERE email = ?
        """, (email,))

        row = cursor.fetchone()

        if row:
            return dict(row)

        return None

    finally:
        conn.close()
