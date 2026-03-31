import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id SERIAL PRIMARY KEY,
            date TEXT NOT NULL,
            merchant TEXT,
            category TEXT,
            total REAL NOT NULL,
            items TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id SERIAL PRIMARY KEY,
            category TEXT UNIQUE NOT NULL,
            monthly_limit REAL NOT NULL
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

init_db()

