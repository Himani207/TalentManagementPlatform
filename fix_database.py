import sqlite3
import os

DB_PATH = r"C:\Users\acer\Desktop\Talent Management Platform\talentsphere.db"

print("Database:")
print(DB_PATH)

if not os.path.exists(DB_PATH):
    print("ERROR: Database file not found!")
    exit()

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Check existing columns
cursor.execute("PRAGMA table_info(professional_profile)")
columns = [row[1] for row in cursor.fetchall()]

print("\nExisting columns:")
for column in columns:
    print("-", column)

# Add missing work_experience column
if "work_experience" not in columns:
    print("\nAdding work_experience...")
    cursor.execute("""
        ALTER TABLE professional_profile
        ADD COLUMN work_experience TEXT
    """)
    print("work_experience added successfully.")
else:
    print("\nwork_experience already exists.")

# Add other potentially missing columns
missing_columns = {
    "achievements": "TEXT",
    "certifications": "TEXT",
    "career_goal": "TEXT",
    "preferred_role": "TEXT",
    "current_salary": "INTEGER DEFAULT 0",
    "linkedin": "TEXT",
    "github": "TEXT"
}

for column, column_type in missing_columns.items():

    if column not in columns:
        print(f"Adding {column}...")
        cursor.execute(
            f"ALTER TABLE professional_profile ADD COLUMN {column} {column_type}"
        )

conn.commit()

# Verify
cursor.execute("PRAGMA table_info(professional_profile)")
columns_after = [row[1] for row in cursor.fetchall()]

print("\n================================")
print("FINAL COLUMNS")
print("================================")

for column in columns_after:
    print("-", column)

conn.close()

print("\nDatabase fix completed successfully.")