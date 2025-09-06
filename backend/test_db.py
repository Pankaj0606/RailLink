from database import get_db_connection

conn = get_db_connection()
if conn:
    print("✅ Database Connected!")
else:
    print("❌ Database Connection Failed!")
