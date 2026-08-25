import sqlite3

conn = sqlite3.connect("talentsphere.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM users")

conn.commit()
conn.close()

print("All users deleted successfully.")