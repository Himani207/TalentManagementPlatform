from utils.coding_db import get_connection

conn = get_connection()

print("Coding tables created successfully!")

conn.close()