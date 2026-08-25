import sqlite3

DB_NAME = "talentsphere.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_chat_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            question TEXT,
            answer TEXT
        )
    """)

    conn.commit()
    conn.close()


# Create the table when this file is imported
create_chat_table()


def save_chat(email, question, answer):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO chat_history (email, question, answer)
        VALUES (?, ?, ?)
    """, (email, question, answer))

    conn.commit()
    conn.close()


def get_chat_history(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT question, answer
        FROM chat_history
        WHERE email=?
        ORDER BY id DESC
    """, (email,))

    chats = cursor.fetchall()

    conn.close()
    return chats


def delete_chat_history(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM chat_history
        WHERE email=?
    """, (email,))

    conn.commit()
    conn.close()