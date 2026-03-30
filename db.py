import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'expenses.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            merchant TEXT,
            category TEXT,
            total REAL NOT NULL,
            items TEXT,
            created_at TEXT DEFAULT (datetime('now'))
            )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT UNIQUE NOT NULL,
            monthly_limit REAL NOT NULL
            )
    ''')

    conn.commit()
    conn.close()

init_db()

