import sqlite3

conn = sqlite3.connect("talentsphere.db")
cursor = conn.cursor()

columns = [
    ("overall_percentage", "REAL DEFAULT 0"),
    ("recent_exam_score", "REAL DEFAULT 0"),
    ("strong_subjects", "TEXT"),
    ("weak_subjects", "TEXT"),
    ("academic_achievements", "TEXT"),
    ("attendance_percentage", "REAL DEFAULT 0"),
    ("academic_goal", "TEXT")
]

for column, datatype in columns:

    try:
        cursor.execute(
            f"ALTER TABLE student_profile ADD COLUMN {column} {datatype}"
        )
    except sqlite3.OperationalError:
        pass

conn.commit()
conn.close()

print("Academic columns added successfully.")