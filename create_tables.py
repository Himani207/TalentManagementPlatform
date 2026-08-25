import sqlite3

conn = sqlite3.connect("talentsphere.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS placement_scores (

    email TEXT PRIMARY KEY,

    resume_score INTEGER DEFAULT 0,

    coding_score INTEGER DEFAULT 0,

    project_score INTEGER DEFAULT 0,

    communication_score INTEGER DEFAULT 0,

    internship_score INTEGER DEFAULT 0,

    placement_score INTEGER DEFAULT 0,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

conn.commit()
conn.close()

print("placement_scores table created successfully.")