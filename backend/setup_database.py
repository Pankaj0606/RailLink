# /backend/setup_database.py

import pandas as pd
from sqlalchemy import create_engine
import psycopg2
from database import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def setup_database():
    """
    Connects to PostgreSQL, creates the 'trains' table, and populates it
    from the dataset.csv file.
    """
    try:
        # Connect to the default 'postgres' database to create a new database
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Check if the database exists
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
        if cur.fetchone() is None:
            print(f"Database '{DB_NAME}' not found. Creating it...")
            cur.execute(f"CREATE DATABASE {DB_NAME}")
            print(f"Database '{DB_NAME}' created successfully.")
        else:
            print(f"Database '{DB_NAME}' already exists.")

        cur.close()
        conn.close()

        # Connect to the new database to create the table
        db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(db_url)

        print("Reading dataset.csv...")
        df = pd.read_csv('dataset.csv')

        # Clean up column names (remove spaces and convert to lowercase)
        df.columns = [c.strip().replace(' ', '_') for c in df.columns]

        print("Creating 'trains' table and importing data...")
        # This will create the table and insert the data.
        # 'if_exists='replace'' will drop the table if it already exists and create a new one.
        # You can change it to 'append' if you want to add data without dropping the table.
        df.to_sql('trains', engine, if_exists='replace', index=False)

        print("✅ Database setup is complete. Data has been imported into the 'trains' table.")

    except Exception as e:
        print(f"❌ An error occurred during database setup: {e}")

if __name__ == "__main__":
    setup_database()