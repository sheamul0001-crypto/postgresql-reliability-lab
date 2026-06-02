import psycopg2
import sqlalchemy
from dotenv import load_dotenv

load_dotenv()

DB_HOST = "34.13.49.13"
DB_USER = "labuser"
DB_PASS = "Lab@12345"
DB_NAME = "reliability_lab"
DB_PORT = "5432"

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        dbname=DB_NAME,
        port=DB_PORT
    )

def setup_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                )
            """)
        conn.commit()
        print("Table created successfully")

def insert_event(name):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO events (name) VALUES (%s)", (name,)
            )
        conn.commit()
        print(f"Inserted event: {name}")

def list_events():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, created_at FROM events ORDER BY created_at DESC"
            )
            rows = cur.fetchall()
    print(f"\n--- {len(rows)} events in Cloud SQL ---")
    for row in rows:
        print(f"  {row[0]} | {row[1]} | {row[2]}")

if __name__ == "__main__":
    print("Connecting to Cloud SQL...")
    setup_table()
    insert_event("app_started")
    insert_event("health_check_passed")
    insert_event("backup_completed")
    list_events()
    print("\nDone.")