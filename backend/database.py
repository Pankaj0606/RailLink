# import psycopg2
# from psycopg2.extras import RealDictCursor
import psycopg2
import psycopg2.extras
# Database connection details
DB_NAME = "raillink_db"  # Updated database name
DB_USER = "pankajyadav"
DB_PASSWORD = ""  # Keep empty if no password is set
DB_HOST = "localhost"
DB_PORT = "5432"

# def get_db_connection():
#     try:
#         conn = psycopg2.connect(
#             dbname="raillink_db",
#             user="pankajyadav",  # ✅ Correct username
#             password="",  # ✅ Keep empty if no password is set
#             host="localhost",
#             port="5432",
#             cursor_factory=RealDictCursor  # ✅ Use RealDictCursor
#         )
#         return conn
#     except Exception as e:
#         print("Database connection failed:", str(e))
#         return None




def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None
