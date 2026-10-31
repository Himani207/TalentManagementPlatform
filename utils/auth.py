import sqlite3
import bcrypt


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
    conn = sqlite3.connect("talentsphere.db")
    cursor = conn.cursor()

    hashed_password = hash_password(new_password)

    cursor.execute(
        """
        UPDATE users
        SET password=?
        WHERE email=?
        """,
        (hashed_password, email)
    )

    conn.commit()

    updated = cursor.rowcount > 0

    conn.close()

    return updated


# -------------------------
# Register User
# -------------------------

def register_user(full_name, email, password, role):
    conn = sqlite3.connect("talentsphere.db")
    cursor = conn.cursor()
    hashed_password = hash_password(password)

    try:
        cursor.execute(
            """
            INSERT INTO users(full_name, email, password, role)
            VALUES(?,?,?,?)
            """,
            (
                full_name,
                email,
                hashed_password,
                role
            )
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

    conn = sqlite3.connect("talentsphere.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT full_name, email, password, role
        FROM users
        WHERE email=?
        """,
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    if user:

        full_name = user[0]
        email = user[1]
        stored_password = user[2]
        role = user[3]

        if verify_password(password, stored_password):

            return {
                "name": full_name,
                "email": email,
                "role": role,
                "category": role
                
            }

    return None