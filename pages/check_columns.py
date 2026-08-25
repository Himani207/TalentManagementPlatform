import sqlite3
from pathlib import Path

DB = Path(__file__).parent.parent / "talentsphere.db"

conn = sqlite3.connect(DB)

print(conn.execute(
    "PRAGMA table_info(student_profile)"
).fetchall())

conn.close()