import sqlite3
import bcrypt
from pathlib import Path

# -------------------------
# Database Configuration
# -------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "talentsphere.db"


def get_connection():
    return sqlite3.connect(str(DB_PATH))


# -------------------------
# Create Users Table
# -------------------------

def initialize_database():
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)

        conn.commit()

    finally:
        conn.close()


initialize_database()


# -------------------------
# Password Hashing
# -------------------------

def hash_password(password):
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def verify_password(password, hashed):
    return bcrypt.checkpw(
        password.encode(),
        hashed.encode()
    )


# -------------------------
# Update Existing Password
# -------------------------

def update_password(email, new_password):
    conn = get_connection()

    try:
        cursor = conn.cursor()
        hashed_password = hash_password(new_password)

        cursor.execute(
            """
            UPDATE users
            SET password = ?
            WHERE email = ?
            """,
            (hashed_password, email)
        )

        conn.commit()

        return cursor.rowcount > 0

    finally:
        conn.close()


# -------------------------
# Register User
# -------------------------

def register_user(full_name, email, password, role):
    conn = get_connection()

    try:
        cursor = conn.cursor()
        hashed_password = hash_password(password)

        cursor.execute(
            """
            INSERT INTO users (full_name, email, password, role)
            VALUES (?, ?, ?, ?)
            """,
            (full_name, email, hashed_password, role)
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


# -------------------------
# Login User
# -------------------------

def login_user(email, password):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT full_name, email, password, role
            FROM users
            WHERE email = ?
            """,
            (email,)
        )

        user = cursor.fetchone()

    finally:
        conn.close()

    if user:
        full_name = user[0]
        user_email = user[1]
        stored_password = user[2]
        role = user[3]

        if verify_password(password, stored_password):
            return {
                "name": full_name,
                "email": user_email,
                "role": role,
                "category": role
            }

    return None