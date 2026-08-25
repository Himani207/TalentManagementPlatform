from database import get_connection


# ==========================================================
# CREATE TABLE
# ==========================================================

def create_salary_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS salary_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        email TEXT NOT NULL,

        current_salary REAL,

        market_salary REAL,

        expected_salary REAL,

        skill_score INTEGER,

        promotion_score INTEGER,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()


# ==========================================================
# SAVE SALARY HISTORY
# ==========================================================

def save_salary_history(

    email,
    current_salary,
    market_salary,
    expected_salary,
    skill_score,
    promotion_score

):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    INSERT INTO salary_history(

        email,
        current_salary,
        market_salary,
        expected_salary,
        skill_score,
        promotion_score

    )

    VALUES(?,?,?,?,?,?)
    """,
    (

        email,
        current_salary,
        market_salary,
        expected_salary,
        skill_score,
        promotion_score

    )
    )

    conn.commit()
    conn.close()


# ==========================================================
# GET SALARY HISTORY
# ==========================================================

def get_salary_history(email):

    conn = get_connection()
    conn.row_factory = lambda cursor, row: {
        col[0]: row[idx]
        for idx, col in enumerate(cursor.description)
    }

    cursor = conn.cursor()

    cursor.execute(
    """
    SELECT

        current_salary,
        market_salary,
        expected_salary,
        skill_score,
        promotion_score,
        created_at

    FROM salary_history

    WHERE email=?

    ORDER BY created_at DESC
    """,
    (email,)
    )

    history = cursor.fetchall()

    conn.close()

    return history


# ==========================================================
# GET LATEST SALARY RECORD
# ==========================================================

def get_latest_salary(email):

    conn = get_connection()
    conn.row_factory = lambda cursor, row: {
        col[0]: row[idx]
        for idx, col in enumerate(cursor.description)
    }

    cursor = conn.cursor()

    cursor.execute(
    """
    SELECT *

    FROM salary_history

    WHERE email=?

    ORDER BY created_at DESC

    LIMIT 1
    """,
    (email,)
    )

    data = cursor.fetchone()

    conn.close()

    return data


# ==========================================================
# DELETE SALARY HISTORY
# ==========================================================

def delete_salary_history(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    DELETE FROM salary_history
    WHERE email=?
    """,
    (email,)
    )

    conn.commit()
    conn.close()


# ==========================================================
# TOTAL RECORDS
# ==========================================================

def get_total_records(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    SELECT COUNT(*)

    FROM salary_history

    WHERE email=?
    """,
    (email,)
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total