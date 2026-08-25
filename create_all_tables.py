from database import get_connection


conn = get_connection()
cursor = conn.cursor()


# =========================
# USERS TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    full_name TEXT,

    email TEXT UNIQUE,

    password TEXT,

    role TEXT

)
""")


# =========================
# PLACEMENT TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS placement_scores(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    email TEXT UNIQUE,

    score INTEGER DEFAULT 0

)
""")


# =========================
# CODING PROGRESS TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS coding_progress(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    email TEXT,

    question_id INTEGER,

    status TEXT DEFAULT 'Not Solved',

    score INTEGER DEFAULT 0,

    xp INTEGER DEFAULT 0

)
""")


# =========================
# RESUME SCORE TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS resume_scores(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    email TEXT,

    score INTEGER

)
""")


# =========================
# PROFESSIONAL PROFILE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS professional_profile(

    email TEXT PRIMARY KEY,

    full_name TEXT,

    phone TEXT,

    location TEXT,

    company TEXT,

    current_role TEXT,

    experience INTEGER,

    technical_skills TEXT,

    soft_skills TEXT,

    leadership INTEGER,

    achievements TEXT,

    certifications TEXT,

    career_goal TEXT

)
""")


conn.commit()
conn.close()


print("All tables created successfully")