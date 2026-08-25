import sqlite3

conn = sqlite3.connect("talentsphere.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(coding_questions)")

for row in cursor.fetchall():
    print(row)

conn.close()