import sqlite3

conn = sqlite3.connect("talentsphere.db")
cursor = conn.cursor()

cursor.execute("SELECT email,parent_email,school_name FROM student_profile")

rows = cursor.fetchall()

print(rows)

conn.close()